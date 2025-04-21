# Core_Nodes/overlay_node.py
import torch
import torch.nn.functional as F # For affine_grid and grid_sample
import numpy as np
import math # Needed for ceil, sin, cos, radians
import traceback # For detailed error printing

class OverlayQRCodeNode:
    """
    Overlays a QR Code image onto a base image.
    Supports single placement with alignment/margin/rotation options OR
    repeating the QR code as a tiled watermark pattern (rotation applied to each tile).
    Handles RGBA inputs and outputs an RGBA image.
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
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1, "display": "number"}), # New Rotation
                "repeat_qr": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "vertical_align": (cls.ALIGN_VERT, {"default": "bottom"}), # Only used if repeat_qr is False
                "horizontal_align": (cls.ALIGN_HORIZ, {"default": "right"}), # Only used if repeat_qr is False
                "margin_percent": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 50.0, "step": 0.1, "display": "slider"}), # Only used if repeat_qr is False
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "overlay_qr"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def overlay_qr(self, base_image, qr_code_image,
                   size_percent, opacity, rotation_angle, repeat_qr,
                   vertical_align="bottom", horizontal_align="right", margin_percent=2.0
                   ):

        dummy_tensor = torch.zeros((1, 64, 64, 4), dtype=torch.float32) # RGBA dummy

        if base_image is None or qr_code_image is None:
            print("ERROR: OverlayQRCodeNode - Missing base_image or qr_code_image input.")
            return (dummy_tensor,)
        if base_image.dim() != 4 or qr_code_image.dim() != 4:
             print("ERROR: OverlayQRCodeNode - Inputs must be 4D tensors (B, H, W, C).")
             return (dummy_tensor,)

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
            print(f"ERROR: OverlayQRCodeNode - Base image unsupported channel count: {base_c}")
            return (dummy_tensor,)

        qr_img_np = qr_img_tensor.cpu().numpy()
        if qr_c == 3:
             qr_img_np_rgba = np.concatenate((qr_img_np, np.ones((qr_h, qr_w, 1), dtype=np.float32)), axis=2)
        elif qr_c == 4:
             qr_img_np_rgba = qr_img_np
        else:
            print(f"ERROR: OverlayQRCodeNode - QR Code image unsupported channel count: {qr_c}")
            return (dummy_tensor,)

        # --- Calculate Target QR Size (Pre-rotation) ---
        base_ref_dim = min(base_h, base_w)
        target_qr_dim = max(1, int(base_ref_dim * (size_percent / 100.0)))
        qr_aspect_ratio = qr_w / qr_h if qr_h > 0 else 1
        if qr_w >= qr_h:
            target_qr_w_unrot = target_qr_dim
            target_qr_h_unrot = max(1, int(target_qr_w_unrot / qr_aspect_ratio))
        else:
            target_qr_h_unrot = target_qr_dim
            target_qr_w_unrot = max(1, int(target_qr_h_unrot * qr_aspect_ratio))

        # --- Resize QR Code ---
        if target_qr_h_unrot <= 0 or target_qr_w_unrot <= 0:
             print(f"ERROR: OverlayQRCodeNode - Invalid pre-rotation target size ({target_qr_h_unrot}x{target_qr_w_unrot}).")
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        try:
            qr_tensor_nchw = torch.from_numpy(qr_img_np_rgba).permute(2, 0, 1).unsqueeze(0).cpu()
            resized_qr_tensor_nchw = F.interpolate(
                qr_tensor_nchw, size=(target_qr_h_unrot, target_qr_w_unrot), mode='bicubic', align_corners=False
            )
            # Keep resized tensor as NCHW float for potential rotation
        except Exception as e:
             print(f"ERROR: OverlayQRCodeNode - Failed to resize QR Code: {e}\n{traceback.format_exc()}")
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        # --- Rotate Resized QR Code ---
        final_qr_h = target_qr_h_unrot
        final_qr_w = target_qr_w_unrot
        rotated_qr_np = None # Initialize

        if abs(rotation_angle % 360) > 1e-3: # Only rotate if angle is significant
             print(f"INFO: OverlayQRCodeNode - Rotating QR code by {rotation_angle} degrees.")
             try:
                  angle_rad = math.radians(rotation_angle)
                  cos_a = math.cos(angle_rad)
                  sin_a = math.sin(angle_rad)

                  # Calculate new bounding box size
                  # Note: Using absolute values for sin/cos
                  final_qr_w = int(abs(target_qr_w_unrot * cos_a) + abs(target_qr_h_unrot * sin_a))
                  final_qr_h = int(abs(target_qr_w_unrot * sin_a) + abs(target_qr_h_unrot * cos_a))
                  final_qr_w = max(1, final_qr_w) # Ensure min size 1
                  final_qr_h = max(1, final_qr_h)

                  # Create affine matrix for rotation (inverse rotation for grid_sample)
                  # Rotation around center (0,0) in normalized space
                  rotation_matrix = torch.tensor([
                      [cos_a, sin_a, 0],
                      [-sin_a, cos_a, 0]
                  ], dtype=torch.float32, device=resized_qr_tensor_nchw.device).unsqueeze(0) # Add batch dim

                  # Create sampling grid
                  target_size = torch.Size([1, 4, final_qr_h, final_qr_w]) # Batch, Channels, H, W
                  grid = F.affine_grid(rotation_matrix, target_size, align_corners=False)

                  # Perform grid sampling
                  rotated_qr_tensor_nchw = F.grid_sample(
                      resized_qr_tensor_nchw, grid, mode='bicubic', padding_mode='zeros', align_corners=False
                  ) # padding_mode='zeros' makes outside area transparent black

                  # Convert rotated tensor back to HWC numpy float32
                  rotated_qr_np = rotated_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()

             except Exception as e:
                  print(f"ERROR: OverlayQRCodeNode - Failed during rotation: {e}\n{traceback.format_exc()}")
                  # Fallback: use unrotated resized image
                  rotated_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
                  final_qr_h = target_qr_h_unrot
                  final_qr_w = target_qr_w_unrot
        else:
             # No rotation needed, just convert the resized tensor to numpy
             rotated_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
             # final_qr_h and final_qr_w remain the unrotated dimensions


        # --- Apply Opacity to Rotated/Resized QR Code Alpha ---
        clamped_opacity = max(0.0, min(1.0, opacity))
        rotated_qr_np[:, :, 3] *= clamped_opacity # Apply opacity to the final QR alpha


        # --- Prepare Output Image ---
        output_img_np = base_img_np_rgba.copy()

        # --- Perform Overlay ---
        try:
            if repeat_qr:
                # --- Repeat Mode (Watermark) ---
                print("INFO: OverlayQRCodeNode - Repeat mode enabled.")
                tile_h, tile_w = final_qr_h, final_qr_w # Use dimensions of the (potentially rotated) QR

                if tile_h <= 0 or tile_w <= 0:
                    print("Warning: OverlayQRCodeNode - Rotated QR tile has zero dimension in repeat mode. Skipping overlay.")
                else:
                    reps_h = math.ceil(base_h / tile_h)
                    reps_w = math.ceil(base_w / tile_w)
                    reps_h = max(1, reps_h); reps_w = max(1, reps_w)

                    tiled_layer = np.tile(rotated_qr_np, (reps_h, reps_w, 1)) # Tile the rotated QR
                    tiled_fg_layer = tiled_layer[:base_h, :base_w, :] # Crop to base size

                    # Blend Full Layers
                    bg_area = base_img_np_rgba
                    fg_area = tiled_fg_layer

                    fg_rgb, fg_alpha = fg_area[:, :, :3], fg_area[:, :, 3:4]
                    bg_rgb, bg_alpha = bg_area[:, :, :3], bg_area[:, :, 3:4]
                    out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)
                    numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))
                    epsilon = 1e-7
                    safe_alpha_mask = out_alpha > epsilon
                    divided_rgb = numerator / (out_alpha + epsilon)
                    out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)
                    blended_area = np.concatenate((out_rgb, out_alpha), axis=2)
                    output_img_np = np.clip(blended_area, 0.0, 1.0)

            else:
                # --- Single Placement Mode ---
                # Use final (potentially rotated) dimensions for placement
                target_qr_h_final, target_qr_w_final = final_qr_h, final_qr_w

                margin_px_h = int(base_h * (margin_percent / 100.0))
                margin_px_w = int(base_w * (margin_percent / 100.0))

                if vertical_align == "top": y_start = margin_px_h
                elif vertical_align == "bottom": y_start = base_h - target_qr_h_final - margin_px_h
                else: y_start = (base_h - target_qr_h_final) // 2

                if horizontal_align == "left": x_start = margin_px_w
                elif horizontal_align == "right": x_start = base_w - target_qr_w_final - margin_px_w
                else: x_start = (base_w - target_qr_w_final) // 2

                y_end = y_start + target_qr_h_final
                x_end = x_start + target_qr_w_final

                base_slice_y_start = max(0, y_start)
                base_slice_y_end = min(base_h, y_end)
                base_slice_x_start = max(0, x_start)
                base_slice_x_end = min(base_w, x_end)

                qr_slice_y_start = max(0, -y_start)
                qr_slice_x_start = max(0, -x_start)
                # Ensure qr end slices relate to the *rotated* dimensions
                qr_slice_y_end = min(target_qr_h_final, base_h - y_start)
                qr_slice_x_end = min(target_qr_w_final, base_w - x_start)


                if base_slice_y_start >= base_slice_y_end or base_slice_x_start >= base_slice_x_end or \
                   qr_slice_y_start >= qr_slice_y_end or qr_slice_x_start >= qr_slice_x_end:
                    print("Warning: OverlayQRCodeNode - Single placement results in no overlap or invalid slice.")
                else:
                    bg_area = base_img_np_rgba[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :]
                    # Use the rotated_qr_np for the foreground slice
                    fg_area = rotated_qr_np[qr_slice_y_start:qr_slice_y_end, qr_slice_x_start:qr_slice_x_end, :]

                    if bg_area.shape[:2] != fg_area.shape[:2]:
                        print(f"ERROR: OverlayQRCodeNode - Slice shape mismatch after slicing! BG: {bg_area.shape}, FG: {fg_area.shape}. Cropping FG.")
                        fg_area = fg_area[:bg_area.shape[0], :bg_area.shape[1], :]
                        if bg_area.shape[:2] != fg_area.shape[:2]:
                            print("ERROR: OverlayQRCodeNode - Fallback crop failed. Skipping blending for this area.")
                            # Blending skipped, output_img_np already contains base image
                        else:
                           # Blend after successful crop
                           fg_rgb, fg_alpha = fg_area[:, :, :3], fg_area[:, :, 3:4]
                           bg_rgb, bg_alpha = bg_area[:, :, :3], bg_area[:, :, 3:4]
                           out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)
                           numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))
                           epsilon = 1e-7
                           safe_alpha_mask = out_alpha > epsilon
                           divided_rgb = numerator / (out_alpha + epsilon)
                           out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)
                           blended_area = np.concatenate((out_rgb, out_alpha), axis=2)
                           blended_area = np.clip(blended_area, 0.0, 1.0)
                           output_img_np[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :] = blended_area
                    else:
                       # Blend directly (shapes matched)
                       fg_rgb, fg_alpha = fg_area[:, :, :3], fg_area[:, :, 3:4]
                       bg_rgb, bg_alpha = bg_area[:, :, :3], bg_area[:, :, 3:4]
                       out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)
                       numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))
                       epsilon = 1e-7
                       safe_alpha_mask = out_alpha > epsilon
                       divided_rgb = numerator / (out_alpha + epsilon)
                       out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)
                       blended_area = np.concatenate((out_rgb, out_alpha), axis=2)
                       blended_area = np.clip(blended_area, 0.0, 1.0)
                       output_img_np[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :] = blended_area


        except Exception as e:
             print(f"ERROR: OverlayQRCodeNode - Error during overlay process: {e}\n{traceback.format_exc()}")
             # Return original base image copy on error

        # --- Convert Final Image to Torch Tensor ---
        try:
            output_tensor = torch.from_numpy(output_img_np).unsqueeze(0).cpu()
        except Exception as e:
            print(f"ERROR: OverlayQRCodeNode - Failed to convert final numpy array to tensor: {e}")
            return (dummy_tensor,)

        return (output_tensor,)


# --- ComfyUI Mappings ---
NODE_CLASS_MAPPINGS = {
    "ImageOverlayQRCode": OverlayQRCodeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOverlayQRCode": "Overlay QR Code on Image"
}