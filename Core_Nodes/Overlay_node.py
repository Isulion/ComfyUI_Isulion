# Core_Nodes/overlay_node.py
import math
import logging
import traceback

import numpy as np
import torch
import torch.nn.functional as F # For affine_grid and grid_sample

logger = logging.getLogger(__name__)

class OverlayQRCodeNode:
    """
    Overlays a QR Code image onto a base image.
    Supports single placement with alignment/margin/rotation options OR
    repeating the QR code as a tiled pattern (rotation applied to the overall pattern).
    Handles RGBA inputs; the output preserves the BASE image channel count
    (RGB in -> RGB out, RGBA in -> RGBA out). Full batches are processed.
    """

    ALIGN_VERT = ["top", "bottom", "center"]
    ALIGN_HORIZ = ["left", "right", "center"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "qr_code_image": ("IMAGE",),
                "size_percent": ("FLOAT", {"default": 20.0, "min": 1.0, "max": 100.0, "step": 0.5, "display": "slider"}),
                "opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01, "display": "slider"}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1, "display": "number"}),
                "repeat_pattern": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "vertical_align": (cls.ALIGN_VERT, {"default": "bottom"}),
                "horizontal_align": (cls.ALIGN_HORIZ, {"default": "right"}),
                "margin_percent": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 50.0, "step": 0.1, "display": "slider"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "overlay_qr"
    CATEGORY = "image/postprocessing"

    def overlay_qr(self, base_image, qr_code_image,
                   size_percent, opacity, rotation_angle, repeat_pattern,
                   vertical_align="bottom", horizontal_align="right", margin_percent=2.0
                   ):
        if base_image is None or qr_code_image is None:
            logger.error("OverlayQRCodeNode - Missing base_image or qr_code_image input.")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)
        if base_image.dim() != 4 or qr_code_image.dim() != 4:
            logger.error("OverlayQRCodeNode - Inputs must be 4D tensors (B, H, W, C).")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        batch_size = base_image.shape[0]
        qr_batch_size = max(1, qr_code_image.shape[0])

        outputs = []
        for i in range(batch_size):
            base_item = base_image[i:i + 1]
            qr_index = min(i, qr_batch_size - 1)  # broadcast single QR over batch
            qr_item = qr_code_image[qr_index:qr_index + 1]
            try:
                outputs.append(self._overlay_single(
                    base_item, qr_item,
                    size_percent, opacity, rotation_angle, repeat_pattern,
                    vertical_align, horizontal_align, margin_percent,
                ))
            except Exception:
                logger.error(
                    "OverlayQRCodeNode - Failed on batch item %d, passing base image through.\n%s",
                    i, traceback.format_exc(),
                )
                outputs.append(base_item)

        return (torch.cat(outputs, dim=0),)

    def _overlay_single(self, base_image, qr_code_image,
                        size_percent, opacity, rotation_angle, repeat_pattern,
                        vertical_align, horizontal_align, margin_percent):
        """Overlay one QR image onto one base image. Raises on internal errors."""
        base_img_tensor = base_image[0]
        qr_img_tensor = qr_code_image[0]
        base_h, base_w, base_c = base_img_tensor.shape
        qr_h, qr_w, qr_c = qr_img_tensor.shape

        # --- Ensure RGBA format internally (float32, 0-1 range) ---
        base_img_np = base_img_tensor.cpu().numpy()
        if base_c == 3:
            base_img_np_rgba = np.concatenate((base_img_np, np.ones((base_h, base_w, 1), dtype=np.float32)), axis=2)
        elif base_c == 4:
            base_img_np_rgba = base_img_np
        else:
            raise ValueError(f"Base image unsupported channel count: {base_c}")

        # QR Code
        qr_img_np = qr_img_tensor.cpu().numpy()
        if qr_c == 3:
             qr_img_np_rgba = np.concatenate((qr_img_np, np.ones((qr_h, qr_w, 1), dtype=np.float32)), axis=2)
        elif qr_c == 4:
            qr_img_np_rgba = qr_img_np
        else:
            raise ValueError(f"QR Code image unsupported channel count: {qr_c}")

        # --- Calculate Target QR Tile Size (Always based on UNROTATED size_percent) ---
        base_ref_dim = min(base_h, base_w)
        target_qr_dim_unrot = max(1, int(base_ref_dim * (size_percent / 100.0)))
        qr_aspect_ratio = qr_w / qr_h if qr_h > 0 else 1
        if qr_w >= qr_h:
            target_qr_w_unrot = target_qr_dim_unrot
            target_qr_h_unrot = max(1, int(target_qr_w_unrot / qr_aspect_ratio))
        else:
            target_qr_h_unrot = target_qr_dim_unrot
            target_qr_w_unrot = max(1, int(target_qr_h_unrot * qr_aspect_ratio))

        # --- Resize QR Code (single tile) ---
        try:
            qr_tensor_nchw = torch.from_numpy(qr_img_np_rgba).permute(2, 0, 1).unsqueeze(0).cpu()
            resized_qr_tensor_nchw = F.interpolate(
                qr_tensor_nchw, size=(target_qr_h_unrot, target_qr_w_unrot), mode='bicubic', align_corners=False
            )
        except Exception:
            logger.error("OverlayQRCodeNode - Failed to resize QR Code:\n%s", traceback.format_exc())
            raise

        clamped_opacity = max(0.0, min(1.0, opacity))

        # --- Prepare Output Image ---
        output_img_np = base_img_np_rgba.copy()

        # --- Perform Overlay ---
        try:
            if repeat_pattern:
                self._overlay_repeat_pattern(
                    output_img_np, resized_qr_tensor_nchw,
                    base_h, base_w,
                    target_qr_h_unrot, target_qr_w_unrot,
                    rotation_angle, clamped_opacity,
                )
            else:
                self._overlay_single_placement(
                    output_img_np, base_img_np_rgba, resized_qr_tensor_nchw,
                    base_h, base_w,
                    target_qr_h_unrot, target_qr_w_unrot,
                    rotation_angle, clamped_opacity,
                    vertical_align, horizontal_align, margin_percent,
                )
        except Exception:
            logger.error("OverlayQRCodeNode - Error during overlay process:\n%s", traceback.format_exc())
            raise

        # --- Preserve base image channel count (RGB in -> RGB out) ---
        final_np = output_img_np[:, :, :base_c]

        return torch.from_numpy(final_np).unsqueeze(0).cpu()

    @staticmethod
    def _alpha_composite(fg_area, bg_area):
        """Standard 'over' alpha compositing of two HWC float arrays (RGB+A)."""
        fg_rgb, fg_alpha = fg_area[:, :, :3], fg_area[:, :, 3:4]
        bg_rgb, bg_alpha = bg_area[:, :, :3], bg_area[:, :, 3:4]
        out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)
        numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))
        epsilon = 1e-7
        safe_alpha_mask = out_alpha > epsilon
        divided_rgb = numerator / (out_alpha + epsilon)
        out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)
        return np.concatenate((out_rgb, out_alpha), axis=2)

    def _overlay_repeat_pattern(self, output_img_np, resized_qr_tensor_nchw,
                                base_h, base_w,
                                target_qr_h_unrot, target_qr_w_unrot,
                                rotation_angle, clamped_opacity):
        """Tile the QR across a rotated canvas, then center-crop onto the base."""
        logger.debug("OverlayQRCodeNode - Repeat pattern mode enabled.")

        angle_rad = math.radians(rotation_angle)
        cos_a = abs(math.cos(angle_rad))
        sin_a = abs(math.sin(angle_rad))
        rotated_canvas_w = max(base_w, int(base_w * cos_a + base_h * sin_a))
        rotated_canvas_h = max(base_h, int(base_w * sin_a + base_h * cos_a))

        tile_h, tile_w = target_qr_h_unrot, target_qr_w_unrot
        if tile_h <= 0 or tile_w <= 0:
            logger.warning("OverlayQRCodeNode - Resized QR tile has zero dimension for tiling. Skipping overlay.")
            return

        reps_h = max(1, math.ceil(rotated_canvas_h / tile_h))
        reps_w = max(1, math.ceil(rotated_canvas_w / tile_w))

        resized_qr_np_unrot = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
        tiled_layer_unrot = np.tile(resized_qr_np_unrot, (reps_h, reps_w, 1))
        tiled_layer_cropped_unrot = tiled_layer_unrot[:rotated_canvas_h, :rotated_canvas_w, :]

        tiled_tensor_nchw = torch.from_numpy(tiled_layer_cropped_unrot).permute(2, 0, 1).unsqueeze(0).cpu()

        if abs(rotation_angle % 360) > 1e-3:
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            rotation_matrix = torch.tensor([
                [cos_a, sin_a, 0],
                [-sin_a, cos_a, 0]
            ], dtype=torch.float32, device=tiled_tensor_nchw.device).unsqueeze(0)

            target_size = torch.Size([1, 4, rotated_canvas_h, rotated_canvas_w])
            grid = F.affine_grid(rotation_matrix, target_size, align_corners=False)
            rotated_tiled_tensor_nchw = F.grid_sample(
                tiled_tensor_nchw, grid, mode='bicubic', padding_mode='zeros', align_corners=False
            )
        else:
            rotated_tiled_tensor_nchw = tiled_tensor_nchw

        rotated_tiled_np = rotated_tiled_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()

        # --- Crop the CENTER of the rotated tiled layer to base image size ---
        center_y = rotated_canvas_h // 2
        center_x = rotated_canvas_w // 2
        crop_y_start = max(0, center_y - base_h // 2)
        crop_y_end = min(rotated_canvas_h, center_y + base_h // 2 + (base_h % 2))
        crop_x_start = max(0, center_x - base_w // 2)
        crop_x_end = min(rotated_canvas_w, center_x + base_w // 2 + (base_w % 2))

        final_fg_layer_np = rotated_tiled_np[crop_y_start:crop_y_end, crop_x_start:crop_x_end, :]

        if final_fg_layer_np.shape[:2] != (base_h, base_w):
            logger.warning(
                "OverlayQRCodeNode - Final tiled layer crop size (%s) mismatch with base image size (%s,%s). Resizing.",
                final_fg_layer_np.shape[:2], base_h, base_w,
            )
            fg_tensor_nchw = torch.from_numpy(final_fg_layer_np).permute(2, 0, 1).unsqueeze(0).cpu()
            resized_fg_tensor_nchw = F.interpolate(
                fg_tensor_nchw, size=(base_h, base_w), mode='bilinear', align_corners=False
            )
            final_fg_layer_np = resized_fg_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()

        final_fg_layer_np[:, :, 3] *= clamped_opacity

        blended_area = self._alpha_composite(final_fg_layer_np, output_img_np)
        output_img_np[:] = np.clip(blended_area, 0.0, 1.0)

    def _overlay_single_placement(self, output_img_np, base_img_np_rgba, resized_qr_tensor_nchw,
                                  base_h, base_w,
                                  target_qr_h_unrot, target_qr_w_unrot,
                                  rotation_angle, clamped_opacity,
                                  vertical_align, horizontal_align, margin_percent):
        """Rotate (optional) a single QR tile and place it with alignment/margin."""
        logger.debug("OverlayQRCodeNode - Single placement mode enabled.")

        final_qr_h, final_qr_w = target_qr_h_unrot, target_qr_w_unrot

        if abs(rotation_angle % 360) > 1e-3:
            logger.debug("OverlayQRCodeNode - Rotating single QR code by %s degrees.", rotation_angle)
            angle_rad = math.radians(rotation_angle)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            final_qr_w = max(1, int(abs(target_qr_w_unrot * cos_a) + abs(target_qr_h_unrot * sin_a)))
            final_qr_h = max(1, int(abs(target_qr_w_unrot * sin_a) + abs(target_qr_h_unrot * cos_a)))

            rotation_matrix = torch.tensor([
                [cos_a, sin_a, 0],
                [-sin_a, cos_a, 0]
            ], dtype=torch.float32, device=resized_qr_tensor_nchw.device).unsqueeze(0)

            target_size = torch.Size([1, 4, final_qr_h, final_qr_w])
            grid = F.affine_grid(rotation_matrix, target_size, align_corners=False)
            rotated_qr_tensor_nchw = F.grid_sample(
                resized_qr_tensor_nchw, grid, mode='bicubic', padding_mode='zeros', align_corners=False
            )
            rotated_qr_np = rotated_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
        else:
            rotated_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()

        rotated_qr_np[:, :, 3] *= clamped_opacity

        target_qr_h_final, target_qr_w_final = final_qr_h, final_qr_w

        margin_px_h = int(base_h * (margin_percent / 100.0))
        margin_px_w = int(base_w * (margin_percent / 100.0))

        if vertical_align == "top":
            y_start = margin_px_h
        elif vertical_align == "bottom":
            y_start = base_h - target_qr_h_final - margin_px_h
        else:
            y_start = (base_h - target_qr_h_final) // 2

        if horizontal_align == "left":
            x_start = margin_px_w
        elif horizontal_align == "right":
            x_start = base_w - target_qr_w_final - margin_px_w
        else:
            x_start = (base_w - target_qr_w_final) // 2

        y_end = y_start + target_qr_h_final
        x_end = x_start + target_qr_w_final

        base_slice_y_start = max(0, y_start)
        base_slice_y_end = min(base_h, y_end)
        base_slice_x_start = max(0, x_start)
        base_slice_x_end = min(base_w, x_end)

        qr_slice_y_start = base_slice_y_start - y_start
        qr_slice_x_start = base_slice_x_start - x_start
        qr_slice_y_end = base_slice_y_end - y_start
        qr_slice_x_end = base_slice_x_end - x_start

        overlap_h = base_slice_y_end - base_slice_y_start
        overlap_w = base_slice_x_end - base_slice_x_start
        qr_overlap_h = qr_slice_y_end - qr_slice_y_start
        qr_overlap_w = qr_slice_x_end - qr_slice_x_start

        if overlap_h <= 0 or overlap_w <= 0 or qr_overlap_h <= 0 or qr_overlap_w <= 0 or \
           overlap_h != qr_overlap_h or overlap_w != qr_overlap_w:
            logger.warning("OverlayQRCodeNode - Single placement results in no valid overlap area.")
            return

        bg_area = base_img_np_rgba[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :]
        fg_area = rotated_qr_np[qr_slice_y_start:qr_slice_y_end, qr_slice_x_start:qr_slice_x_end, :]

        if bg_area.shape[:2] != fg_area.shape[:2]:
            logger.error("OverlayQRCodeNode - Slice shape mismatch! BG: %s, FG: %s. Skipping blend.",
                         bg_area.shape[:2], fg_area.shape[:2])
            return

        blended_area = np.clip(self._alpha_composite(fg_area, bg_area), 0.0, 1.0)
        output_img_np[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :] = blended_area
