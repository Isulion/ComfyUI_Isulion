"""Isulion Censored Part node for ComfyUI."""

import logging
import math
import traceback

import torch
import torch.nn.functional as F

logger = logging.getLogger(__name__)

MAX_KERNEL_HALF = 100
MAX_SEED = 0xFFFFFFFFFFFFFFFF


class IsulionCensoredPart:
    """
    Censors part of an image with an irreversible or obfuscating effect.

    Region selection, in order of combination (union):
      1. ``mask`` input - paint it with ComfyUI's MaskEditor (right-click a
         Load Image node -> "Open in MaskEditor") and connect its output.
         Works on any batch; a single mask is broadcast over every image.
      2. Built-in rectangle - enable ``use_region_rect`` and set
         ``region_x/y/width/height`` in percent. Unlike the MaskEditor this
         also works on generated images (KSampler, video frames, ...).

    If neither source defines a selection, the whole image is censored.

    Effects:
      - ``blur``          Gaussian blur, radius driven by ``blur_strength``.
      - ``pixelate``      Mosaic, block size driven by ``pixel_size``.
      - ``pixelate+blur`` Both combined, much harder to reverse.
      - ``black_bar``     Solid black fill, fully irreversible.
      - ``noise``         Seeded TV-static fill, fully irreversible.

    Extras: ``grow_region`` (enlarge/shrink the selection in %),
    ``invert_region`` (censor everything EXCEPT the selection),
    ``feather_edge`` (% of edge softness). Outputs the censored image plus
    the final censor mask for downstream inpainting.
    """

    CENSOR_MODES = ["blur", "pixelate", "pixelate+blur", "black_bar", "noise"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "censor_mode": (cls.CENSOR_MODES,),
                "blur_strength": ("FLOAT", {
                    "default": 15.0,
                    "min": 0.0,
                    "max": 100.0,
                    "step": 0.5,
                    "display": "slider",
                }),
                "pixel_size": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.5,
                    "max": 50.0,
                    "step": 0.5,
                    "display": "slider",
                }),
                "use_region_rect": ("BOOLEAN", {"default": False}),
                "region_x": ("FLOAT", {
                    "default": 25.0, "min": 0.0, "max": 100.0,
                    "step": 0.5, "display": "slider",
                }),
                "region_y": ("FLOAT", {
                    "default": 25.0, "min": 0.0, "max": 100.0,
                    "step": 0.5, "display": "slider",
                }),
                "region_width": ("FLOAT", {
                    "default": 50.0, "min": 0.0, "max": 100.0,
                    "step": 0.5, "display": "slider",
                }),
                "region_height": ("FLOAT", {
                    "default": 50.0, "min": 0.0, "max": 100.0,
                    "step": 0.5, "display": "slider",
                }),
                "grow_region": ("FLOAT", {
                    "default": 0.0, "min": -50.0, "max": 50.0,
                    "step": 0.5, "display": "slider",
                }),
                "invert_region": ("BOOLEAN", {"default": False}),
                "feather_edge": ("FLOAT", {
                    "default": 4.0, "min": 0.0, "max": 100.0,
                    "step": 0.5, "display": "slider",
                }),
                "noise_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "censor_mask")
    FUNCTION = "censor_region"
    CATEGORY = "Isulion/Image"

    def censor_region(self, image, censor_mode="blur", blur_strength=15.0,
                      pixel_size=5.0, use_region_rect=False, region_x=25.0,
                      region_y=25.0, region_width=50.0, region_height=50.0,
                      grow_region=0.0, invert_region=False, feather_edge=4.0,
                      noise_seed=0, mask=None):
        if image is None or image.dim() != 4:
            logger.error("IsulionCensoredPart - 'image' must be a 4D tensor (B, H, W, C).")
            blank = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            return (blank, torch.zeros((1, 64, 64), dtype=torch.float32))

        batch_size = image.shape[0]
        mask = self._normalize_mask(mask)
        mask_batch = mask.shape[0] if mask is not None else 1

        outputs = []
        masks_out = []
        for i in range(batch_size):
            item = image[i:i + 1]
            item_mask = None
            if mask is not None:
                item_mask = mask[min(i, mask_batch - 1)]
            try:
                censored_item, alpha = self._censor_single(
                    item, item_mask, censor_mode, blur_strength, pixel_size,
                    bool(use_region_rect), float(region_x), float(region_y),
                    float(region_width), float(region_height),
                    float(grow_region), bool(invert_region),
                    float(feather_edge), (int(noise_seed) + i) & MAX_SEED,
                )
                outputs.append(censored_item)
                masks_out.append(alpha)
            except Exception:
                # Fail closed: a censoring node must never leak the original image.
                logger.error(
                    "IsulionCensoredPart - Failed on batch item %d, blacking it out entirely.\n%s",
                    i, traceback.format_exc(),
                )
                outputs.append(torch.zeros_like(item))
                h, w = int(item.shape[1]), int(item.shape[2])
                masks_out.append(torch.ones((h, w), dtype=item.dtype, device=item.device))

        censor_masks = torch.stack(masks_out, dim=0).to(dtype=torch.float32)
        return (torch.cat(outputs, dim=0), censor_masks)

    @staticmethod
    def _normalize_mask(mask):
        """Coerce any common ComfyUI mask layout to (B, H, W), or None."""
        if mask is None:
            return None
        if mask.dim() == 2:
            return mask.unsqueeze(0)
        if mask.dim() == 4:
            if mask.shape[1] == 1:
                return mask[:, 0]
            if mask.shape[-1] == 1:
                return mask[..., 0]
            return mask.reshape(-1, *mask.shape[-2:])
        if mask.dim() == 3:
            return mask
        raise ValueError(f"Unsupported mask shape: {tuple(mask.shape)}")

    def _censor_single(self, img, mask, censor_mode, blur_strength, pixel_size,
                       use_rect, rx, ry, rw, rh, grow, invert, feather, seed):
        h, w = int(img.shape[1]), int(img.shape[2])

        alpha = self._build_alpha(img, mask, h, w, use_rect, rx, ry, rw, rh,
                                  grow, invert, feather)

        if censor_mode == "pixelate":
            censored = self._pixelate(img, pixel_size)
        elif censor_mode == "pixelate+blur":
            sigma = self._sigma_for(h, w, blur_strength)
            censored = self._gaussian_blur_hwc(self._pixelate(img, pixel_size), sigma)
        elif censor_mode == "black_bar":
            censored = torch.zeros_like(img)
        elif censor_mode == "noise":
            generator = torch.Generator("cpu").manual_seed(seed)
            noise = torch.rand((h, w, img.shape[3]), generator=generator)
            censored = noise.to(dtype=img.dtype, device=img.device)
        else:
            sigma = self._sigma_for(h, w, blur_strength)
            censored = self._gaussian_blur_hwc(img, sigma)

        out = img * (1.0 - alpha.unsqueeze(-1)) + censored * alpha.unsqueeze(-1)
        return out, alpha

    def _build_alpha(self, img, mask, h, w, use_rect, rx, ry, rw, rh,
                     grow, invert, feather):
        """Combine mask + rectangle, grow/invert/feather -> final (H, W) alpha."""
        sources = []
        if mask is not None:
            m = mask.detach().to(dtype=img.dtype, device=img.device)
            while m.dim() > 2:
                m = m.squeeze(0)
            if m.dim() != 2:
                raise ValueError(f"Unsupported mask shape: {tuple(mask.shape)}")
            if m.shape[0] != h or m.shape[1] != w:
                m = F.interpolate(
                    m.unsqueeze(0).unsqueeze(0), size=(h, w),
                    mode="bilinear", align_corners=False,
                )[0, 0]
            sources.append(torch.clamp(m, 0.0, 1.0))

        if use_rect:
            sources.append(self._rectangle(h, w, rx, ry, rw, rh,
                                           img.dtype, img.device))

        if not sources:
            alpha = torch.ones((h, w), dtype=img.dtype, device=img.device)
        else:
            alpha = sources[0]
            for src in sources[1:]:
                alpha = torch.maximum(alpha, src)

        alpha = self._morph(alpha.unsqueeze(0).unsqueeze(0), grow, h, w)[0, 0]

        if invert:
            alpha = 1.0 - alpha

        if feather > 0.0:
            sigma = max(min(h, w) * feather / 200.0, 0.05)
            alpha = self._gaussian_blur_nchw(
                alpha.unsqueeze(0).unsqueeze(0), sigma)[0, 0]

        return torch.clamp(alpha, 0.0, 1.0)

    @staticmethod
    def _rectangle(h, w, rx, ry, rw, rh, dtype, device):
        ys = torch.arange(h, device=device)
        xs = torch.arange(w, device=device)
        row_hit = (ys >= h * ry / 100.0) & (ys < h * (ry + rh) / 100.0)
        col_hit = (xs >= w * rx / 100.0) & (xs < w * (rx + rw) / 100.0)
        rect = row_hit.unsqueeze(1) & col_hit.unsqueeze(0)
        return rect.to(dtype=dtype)

    def _morph(self, alpha_nchw, grow_percent, h, w):
        """Grow (>0) or shrink (<0) the selection by square structuring elements."""
        grow_px = int(round(min(h, w) * grow_percent / 100.0))
        if grow_px == 0:
            return alpha_nchw
        radius = abs(grow_px)
        kernel = 2 * radius + 1
        pad = kernel // 2

        def dilate(x):
            x = F.pad(x, (pad, pad, pad, pad), mode="replicate")
            return F.max_pool2d(x, kernel_size=kernel, stride=1)

        if grow_px > 0:
            return dilate(alpha_nchw)
        return 1.0 - dilate(1.0 - alpha_nchw)

    @staticmethod
    def _sigma_for(h, w, strength_percent):
        return max(min(h, w) * strength_percent / 200.0, 0.0)

    def _pixelate(self, img, percent):
        h, w = int(img.shape[1]), int(img.shape[2])
        block = max(min(h, w) * percent / 100.0, 1.0)
        small_h = max(1, int(round(h / block)))
        small_w = max(1, int(round(w / block)))
        nchw = img.permute(0, 3, 1, 2)
        small = F.interpolate(nchw, size=(small_h, small_w), mode="area")
        out = F.interpolate(small, size=(h, w), mode="nearest")
        return out.permute(0, 2, 3, 1).contiguous().to(dtype=img.dtype)

    def _gaussian_blur_hwc(self, img, sigma):
        if sigma < 0.05:
            return img
        nchw = img.permute(0, 3, 1, 2)
        blurred = self._gaussian_blur_nchw(nchw, sigma)
        return blurred.permute(0, 2, 3, 1).contiguous().to(dtype=img.dtype)

    def _gaussian_blur_nchw(self, x, sigma):
        """Separable Gaussian blur on an NCHW tensor.

        Large sigmas are split into several identical passes; the variances
        add up, so the combined result matches a single wide-kernel blur
        while keeping every convolution kernel small.
        """
        if sigma < 0.05:
            return x
        channels = x.shape[1]
        passes = max(1, int(math.ceil((3.0 * sigma) / MAX_KERNEL_HALF)))
        pass_sigma = sigma / math.sqrt(passes)

        half = max(int(math.ceil(3.0 * pass_sigma)), 1)
        xs = torch.arange(-half, half + 1, dtype=x.dtype, device=x.device)
        kernel = torch.exp(-(xs * xs) / (2.0 * pass_sigma * pass_sigma))
        kernel = kernel / kernel.sum()

        length = kernel.numel()
        pad = length // 2
        k_horizontal = kernel.view(1, 1, 1, length).expand(channels, 1, 1, length)
        k_vertical = kernel.view(1, 1, length, 1).expand(channels, 1, length, 1)
        for _ in range(passes):
            x = F.pad(x, (pad, pad, 0, 0), mode="replicate")
            x = F.conv2d(x, k_horizontal, groups=channels)
            x = F.pad(x, (0, 0, pad, pad), mode="replicate")
            x = F.conv2d(x, k_vertical, groups=channels)
        return x
