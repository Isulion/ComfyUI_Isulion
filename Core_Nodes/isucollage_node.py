import math
import random

import torch
import torch.nn.functional as F

# Port of the layout algorithm from react-IsuCollage
# (https://github.com/Isulion/react-IsuCollage, src/utils/imageProcessor.ts,
# ImageProcessor.calculateLayout). Row grouping, per-row scaling factor and
# float rect geometry are kept identical; rasterization snaps floats to an
# exact integer grid so tiles fill the canvas without gaps or overlaps.

TARGET_ROW_HEIGHT = 150.0          # reference default from imageProcessor.ts
BACKGROUND = 245.0 / 255.0         # #f5f5f5


def plan_rows(aspects, width):
    """Faithful port of ImageProcessor.calculateLayout.

    Args:
        aspects: iterable of image aspect ratios (width / height).
        width: target collage canvas width in pixels.

    Returns:
        (rows, total_height) where rows is a list of
        ([(index, w_float), ...], row_height_float) preserving input order.
    """
    n = len(aspects)
    if n == 0:
        return [], 0.0

    num_rows = math.ceil(math.sqrt(n))
    max_images_per_row = math.ceil(n / num_rows)

    rows = []
    current_row = []
    current_row_width = 0.0
    y = 0.0

    for index, aspect_ratio in enumerate(aspects):
        current_row.append((index, aspect_ratio))
        current_row_width += TARGET_ROW_HEIGHT * aspect_ratio

        if (current_row_width >= width or index == n - 1
                or len(current_row) == max_images_per_row):
            scaling_factor = width / current_row_width
            row_height = TARGET_ROW_HEIGHT * scaling_factor
            laid_out = []
            for idx, ar in current_row:
                laid_out.append((idx, TARGET_ROW_HEIGHT * ar * scaling_factor))
            rows.append((laid_out, row_height))
            y += row_height
            current_row = []
            current_row_width = 0.0

    return rows, y


def rows_to_pixels(rows, width):
    """Snap float rects to integer pixels while keeping the tiling exact.

    Pixel boundaries are computed by cumulative rounding of the float x
    positions, so the <=1px rounding error is spread across every tile
    (like the sub-pixel canvas rendering) instead of accumulating on the
    last tile. Row boundaries are handled the same way vertically.

    Returns a list of (index, x, y, w, h) integer tuples covering the
    canvas [0, width) x [0, total_height) without gaps or overlaps.
    """
    pixel_rects = []
    y_px = 0
    for laid_out, row_height in rows:
        rh = max(1, round(row_height))
        bounds = [0]
        x_float = 0.0
        for _, w in laid_out:
            x_float += w
            b = round(x_float)
            if b <= bounds[-1]:
                b = bounds[-1] + 1  # keep strictly increasing
            bounds.append(b)
        bounds[-1] = width  # the row fills the canvas width exactly
        for (idx, _), x0, x1 in zip(laid_out, bounds, bounds[1:]):
            if x1 > x0:
                pixel_rects.append((idx, x0, y_px, x1 - x0, rh))
        y_px += rh
    return pixel_rects, y_px


class IsuCollageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "width": ("INT", {"default": 1024, "min": 256, "max": 8192, "step": 64}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("collage_image",)
    FUNCTION = "create_collage"
    CATEGORY = "Isulion/Image"
    # Receive the whole list of variable-size images in a single call so
    # every aspect ratio stays native (mirrors the react-IsuCollage app).
    INPUT_IS_LIST = True

    def create_collage(self, images, seed=0, width=1024):
        # With INPUT_IS_LIST, ComfyUI wraps EVERY input (widgets included)
        # in a list; unwrap the scalar widgets before use.
        if isinstance(seed, (list, tuple)):
            seed = seed[0] if len(seed) else 0
        if isinstance(width, (list, tuple)):
            width = width[0] if len(width) else 1024
        try:
            seed = int(seed)
        except (TypeError, ValueError):
            seed = 0

        frames = []
        for item in images:
            shape = tuple(item.shape)
            if len(shape) == 4:
                # Batched element inside the list: flatten its frames
                frames.extend(item[i] for i in range(shape[0]))
            elif len(shape) == 3:
                frames.append(item)
            else:
                raise ValueError(f"Unsupported image shape: {shape}")

        if not frames:
            raise ValueError("No images provided")

        if seed:
            rng = random.Random(seed)
            rng.shuffle(frames)

        n = len(frames)
        if n == 1:
            return (frames[0].unsqueeze(0).float(),)

        # Native per-image aspect ratios (no padding anywhere in the chain)
        aspects = [f.shape[1] / f.shape[0] for f in frames]
        rows, _total_h = plan_rows(aspects, width)
        pixel_rects, canvas_h = rows_to_pixels(rows, width)

        imgs = [f.float() for f in frames]

        device = imgs[0].device
        canvas = torch.full((canvas_h, width, 3), BACKGROUND,
                            dtype=torch.float32, device=device)

        for idx, x, y, iw, ih in pixel_rects:
            if iw < 1 or ih < 1:
                continue
            img = imgs[idx]
            if img.shape[0] != ih or img.shape[1] != iw:
                t = img.unsqueeze(0).permute(0, 3, 1, 2)
                t = F.interpolate(t, size=(ih, iw), mode='bilinear', align_corners=False)
                r = t.permute(0, 2, 3, 1).squeeze(0)
            else:
                r = img
            canvas[y:y + ih, x:x + iw] = r

        return (canvas.unsqueeze(0),)
