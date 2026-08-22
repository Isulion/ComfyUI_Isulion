import torch
import math
import random
import numpy


class IsuCollageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "seed": ("INT", {"optional": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("collage_image",)
    FUNCTION = "create_collage"
    CATEGORY = "Isulion/Image"

    def create_collage(self, images, seed=None):
        if seed is not None:
            torch.manual_seed(seed)
            random.seed(seed)
            numpy.random.seed(seed)

        imgs = list(images)
        if seed is not None:
            random.shuffle(imgs)

        if not imgs:
            raise ValueError("No images provided")

        imgs = [img.squeeze(0) if len(img.shape) == 4 else img for img in imgs]
        imgs = [img.float() for img in imgs]

        n = len(imgs)
        if n == 1:
            return (imgs[0].unsqueeze(0),)

        W = 1024

        numRows = math.ceil(math.sqrt(n))
        maxImagesPerRow = math.ceil(n / numRows)

        rows = []
        cur_i = []
        cur_r = []
        cur_w = 0.0

        for i in range(n):
            ar = imgs[i].shape[1] / imgs[i].shape[0]
            cur_i.append(i)
            cur_r.append(ar)
            cur_w += 150.0 * ar
            if cur_w >= W or i == n - 1 or len(cur_i) >= maxImagesPerRow:
                rows.append((cur_i[:], cur_r[:], cur_w))
                cur_i = []
                cur_r = []
                cur_w = 0.0

        rects = []
        y = 0
        for idxs, rats, rw in rows:
            scale = W / rw
            rh = max(1, int(round(150.0 * scale)))
            fws = [rh * r for r in rats]
            rem = W
            int_ws = []
            for j, fw in enumerate(fws):
                if j == len(fws) - 1:
                    int_ws.append(rem)
                else:
                    iw = max(1, int(round(fw)))
                    int_ws.append(iw)
                    rem -= iw
            x = 0
            for j, idx in enumerate(idxs):
                iw = int_ws[j]
                rects.append((idx, x, y, iw, rh))
                x += iw
            y += rh

        H = y

        canvas = torch.full((H, W, 3), 245.0 / 255.0, dtype=torch.float32, device=imgs[0].device)

        for idx, x, y, iw, ih in rects:
            if iw < 1 or ih < 1:
                continue
            img = imgs[idx]
            if img.shape[0] != ih or img.shape[1] != iw:
                t = img.unsqueeze(0).permute(0, 3, 1, 2)
                t = torch.nn.functional.interpolate(t, size=(ih, iw), mode='bilinear', align_corners=False)
                r = t.permute(0, 2, 3, 1).squeeze(0)
            else:
                r = img
            canvas[y:y+ih, x:x+iw] = r

        return (canvas.unsqueeze(0),)