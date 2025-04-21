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
    repeating the QR code as a tiled pattern (rotation applied to the overall pattern).
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
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1, "display": "number"}),
                "repeat_pattern": ("BOOLEAN", {"default": False}), # Renamed
            },
            "optional": {
                # These are primarily used if repeat_pattern is False, but margin could maybe apply to pattern?
                # Let's keep them optional and clarify usage. Vertical/Horizontal align definitely only for single.
                "vertical_align": (cls.ALIGN_VERT, {"default": "bottom"}),
                "horizontal_align": (cls.ALIGN_HORIZ, {"default": "right"}),
                "margin_percent": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 50.0, "step": 0.1, "display": "slider"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "overlay_qr"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def overlay_qr(self, base_image, qr_code_image,
                   size_percent, opacity, rotation_angle, repeat_pattern,
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
        # Base Image
        base_img_np = base_img_tensor.cpu().numpy()
        if base_c == 3:
            base_img_np_rgba = np.concatenate((base_img_np, np.ones((base_h, base_w, 1), dtype=np.float32)), axis=2)
        elif base_c == 4:
            base_img_np_rgba = base_img_np
        else:
            print(f"ERROR: OverlayQRCodeNode - Base image unsupported channel count: {base_c}")
            return (dummy_tensor,)

        # QR Code Image
        qr_img_np = qr_img_tensor.cpu().numpy()
        if qr_c == 3:
             qr_img_np_rgba = np.concatenate((qr_img_np, np.ones((qr_h, qr_w, 1), dtype=np.float32)), axis=2)
        elif qr_c == 4:
             qr_img_np_rgba = qr_img_np
        else:
            print(f"ERROR: OverlayQRCodeNode - QR Code image unsupported channel count: {qr_c}")
            return (dummy_tensor,)

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

        if target_qr_h_unrot <= 0 or target_qr_w_unrot <= 0:
             print(f"ERROR: OverlayQRCodeNode - Invalid target QR size ({target_qr_h_unrot}x{target_qr_w_unrot}).")
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        # --- Resize QR Code (single tile) ---
        try:
            qr_tensor_nchw = torch.from_numpy(qr_img_np_rgba).permute(2, 0, 1).unsqueeze(0).cpu()
            # Resize to the UNROTATED tile size
            resized_qr_tensor_nchw = F.interpolate(
                qr_tensor_nchw, size=(target_qr_h_unrot, target_qr_w_unrot), mode='bicubic', align_corners=False
            )
            # Keep resized tensor as NCHW float for further processing
        except Exception as e:
             print(f"ERROR: OverlayQRCodeNode - Failed to resize QR Code: {e}\n{traceback.format_exc()}")
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        # --- Calculate clamped_opacity ONCE ---
        clamped_opacity = max(0.0, min(1.0, opacity))


        # --- Prepare Output Image ---
        output_img_np = base_img_np_rgba.copy()

        # --- Perform Overlay ---
        try:
            if repeat_pattern:
                # --- Repeat Pattern Mode ---
                print("INFO: OverlayQRCodeNode - Repeat pattern mode enabled.")

                # Calculate size of canvas needed to rotate base image (this is the target size for the tiled pattern)
                angle_rad = math.radians(rotation_angle)
                cos_a = abs(math.cos(angle_rad))
                sin_a = abs(math.sin(angle_rad))
                # Size of the base image's bounding box after rotation
                rotated_canvas_w = int(base_w * cos_a + base_h * sin_a)
                rotated_canvas_h = int(base_w * sin_a + base_h * cos_a)

                # Ensure rotated canvas is at least base size (can happen near 0/90/180/270)
                rotated_canvas_w = max(base_w, rotated_canvas_w)
                rotated_canvas_h = max(base_h, rotated_canvas_h)

                # Calculate how many UNROTATED tiles fit into the ROTATED canvas size
                tile_h, tile_w = target_qr_h_unrot, target_qr_w_unrot
                if tile_h <= 0 or tile_w <= 0: # Safety check
                     print("Warning: OverlayQRCodeNode - Resized QR tile has zero dimension for tiling. Skipping overlay.")
                else:
                    # Calculate repetitions needed for the rotated canvas dimensions
                    reps_h = math.ceil(rotated_canvas_h / tile_h)
                    reps_w = math.ceil(rotated_canvas_w / tile_w)
                    reps_h = max(1, reps_h); reps_w = max(1, reps_w)

                    # Tile the UNROTATED resized QR code image
                    resized_qr_np_unrot = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy() # H, W, 4 float32
                    tiled_layer_unrot = np.tile(resized_qr_np_unrot, (reps_h, reps_w, 1)) # Create a large unrotated tiled image

                    # Crop the unrotated tiled image to the size of the rotated canvas
                    tiled_layer_cropped_unrot = tiled_layer_unrot[:rotated_canvas_h, :rotated_canvas_w, :]

                    # --- Rotate the Tiled Layer ---
                    tiled_tensor_nchw = torch.from_numpy(tiled_layer_cropped_unrot).permute(2, 0, 1).unsqueeze(0).cpu()

                    if abs(rotation_angle % 360) > 1e-3: # Rotate only if angle is significant
                         # Create affine matrix for rotation (inverse rotation for grid_sample)
                         cos_a = math.cos(angle_rad) # Use original sin/cos for matrix
                         sin_a = math.sin(angle_rad)
                         rotation_matrix = torch.tensor([
                             [cos_a, sin_a, 0],
                             [-sin_a, cos_a, 0]
                         ], dtype=torch.float32, device=tiled_tensor_nchw.device).unsqueeze(0) # Add batch dim

                         # Target size is the rotated canvas size
                         target_size = torch.Size([1, 4, rotated_canvas_h, rotated_canvas_w])
                         grid = F.affine_grid(rotation_matrix, target_size, align_corners=False)

                         # Perform grid sampling
                         rotated_tiled_tensor_nchw = F.grid_sample(
                             tiled_tensor_nchw, grid, mode='bicubic', padding_mode='zeros', align_corners=False
                         )
                    else:
                         # No rotation needed for the tiled layer
                         rotated_tiled_tensor_nchw = tiled_tensor_nchw

                    # Convert rotated tiled tensor back to HWC numpy float32
                    rotated_tiled_np = rotated_tiled_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy() # H, W, 4 float32

                    # --- Crop the CENTER of the rotated tiled layer to base image size ---
                    center_y = rotated_canvas_h // 2
                    center_x = rotated_canvas_w // 2

                    base_h_half = base_h // 2
                    base_w_half = base_w // 2

                    crop_y_start = center_y - base_h_half
                    crop_y_end = center_y + base_h_half + (base_h % 2) # Handle odd dimensions
                    crop_x_start = center_x - base_w_half
                    crop_x_end = center_x + base_w_half + (base_w % 2) # Handle odd dimensions

                    # Ensure crop is within bounds (should be if canvas was calculated correctly)
                    crop_y_start = max(0, crop_y_start)
                    crop_y_end = min(rotated_canvas_h, crop_y_end)
                    crop_x_start = max(0, crop_x_start)
                    crop_x_end = min(rotated_canvas_w, crop_x_end)

                    # The final foreground layer is this center crop
                    final_fg_layer_np = rotated_tiled_np[crop_y_start:crop_y_end, crop_x_start:crop_x_end, :]

                    # Ensure cropped size matches base image size (can be slightly off due to rounding/interpolation)
                    if final_fg_layer_np.shape[:2] != (base_h, base_w):
                         print(f"Warning: OverlayQRCodeNode - Final tiled layer crop size ({final_fg_layer_np.shape[:2]}) mismatch with base image size ({base_h},{base_w}). Resizing.")
                         fg_tensor_nchw = torch.from_numpy(final_fg_layer_np).permute(2, 0, 1).unsqueeze(0).cpu()
                         resized_fg_tensor_nchw = F.interpolate(
                              fg_tensor_nchw, size=(base_h, base_w), mode='bilinear', align_corners=False # Bilinear for speed/simplicity here
                         )
                         final_fg_layer_np = resized_fg_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()


                    # --- Apply Opacity to the FINAL tiled layer alpha ---
                    # Apply the pre-calculated clamped_opacity
                    final_fg_layer_np[:, :, 3] *= clamped_opacity


                    # --- Blend Full Layers (Tiled FG over Base BG) ---
                    bg_area = base_img_np_rgba # The whole base image
                    fg_area = final_fg_layer_np   # The whole final tiled layer

                    fg_rgb, fg_alpha = fg_area[:, :, :3], fg_area[:, :, 3:4]
                    bg_rgb, bg_alpha = bg_area[:, :, :3], bg_area[:, :, 3:4]

                    # Alpha Compositing (Fg over Bg)
                    out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)
                    numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))
                    epsilon = 1e-7
                    safe_alpha_mask = out_alpha > epsilon # Shape (H, W, 1)
                    divided_rgb = numerator / (out_alpha + epsilon)
                    out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)

                    blended_area = np.concatenate((out_rgb, out_alpha), axis=2)
                    output_img_np = np.clip(blended_area, 0.0, 1.0) # Assign blended result to output

            else:
                # --- Single Placement Mode ---
                print("INFO: OverlayQRCodeNode - Single placement mode enabled.")

                # In single mode, rotation is applied to the *individual* tile
                final_qr_h, final_qr_w = target_qr_h_unrot, target_qr_w_unrot
                rotated_qr_np = None # Initialize

                if abs(rotation_angle % 360) > 1e-3: # Rotate only if angle is significant
                     print(f"INFO: OverlayQRCodeNode - Rotating single QR code by {rotation_angle} degrees.")
                     try:
                          angle_rad = math.radians(rotation_angle)
                          cos_a = math.cos(angle_rad)
                          sin_a = math.sin(angle_rad)

                          # Calculate new bounding box size for the single rotated tile
                          final_qr_w = int(abs(target_qr_w_unrot * cos_a) + abs(target_qr_h_unrot * sin_a))
                          final_qr_h = int(abs(target_qr_w_unrot * sin_a) + abs(target_qr_h_unrot * cos_a))
                          final_qr_w = max(1, final_qr_w)
                          final_qr_h = max(1, final_qr_h)

                          # Create affine matrix for inverse rotation
                          rotation_matrix = torch.tensor([
                              [cos_a, sin_a, 0],
                              [-sin_a, cos_a, 0]
                          ], dtype=torch.float32, device=resized_qr_tensor_nchw.device).unsqueeze(0)

                          # Target size is the new rotated bounding box size
                          target_size = torch.Size([1, 4, final_qr_h, final_qr_w])
                          grid = F.affine_grid(rotation_matrix, target_size, align_corners=False)

                          # Perform grid sampling
                          rotated_qr_tensor_nchw = F.grid_sample(
                              resized_qr_tensor_nchw, grid, mode='bicubic', padding_mode='zeros', align_corners=False
                          )
                          rotated_qr_np = rotated_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()

                     except Exception as e:
                          print(f"ERROR: OverlayQRCodeNode - Failed during single tile rotation: {e}\n{traceback.format_exc()}")
                          # Fallback: use unrotated resized image
                          rotated_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
                          final_qr_h = target_qr_h_unrot
                          final_qr_w = target_qr_w_unrot
                else:
                     # No rotation needed, just convert the resized tensor to numpy
                     rotated_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy()
                     # final_qr_h and final_qr_w remain the unrotated dimensions


                # Apply Opacity to the SINGLE rotated tile alpha
                # Apply the pre-calculated clamped_opacity
                rotated_qr_np[:, :, 3] *= clamped_opacity


                # Calculate Position and Slices using FINAL (potentially rotated) dimensions
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

                # Recalculate QR slices relative to the part that overlaps the base image
                qr_slice_y_start = base_slice_y_start - y_start
                qr_slice_x_start = base_slice_x_start - x_start
                qr_slice_y_end = base_slice_y_end - y_start
                qr_slice_x_end = base_slice_x_end - x_start

                # Check for valid overlap dimensions by comparing slice sizes
                overlap_h = base_slice_y_end - base_slice_y_start
                overlap_w = base_slice_x_end - base_slice_x_start
                qr_overlap_h = qr_slice_y_end - qr_slice_y_start
                qr_overlap_w = qr_slice_x_end - qr_slice_x_start


                if overlap_h <= 0 or overlap_w <= 0 or qr_overlap_h <= 0 or qr_overlap_w <= 0 or \
                   overlap_h != qr_overlap_h or overlap_w != qr_overlap_w:
                    print("Warning: OverlayQRCodeNode - Single placement results in no valid overlap area.")
                else:
                    # Extract the overlapping background area
                    bg_area = base_img_np_rgba[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :]

                    # Extract the corresponding foreground QR area (single rotated tile)
                    # Use the calculated QR slices
                    fg_area = rotated_qr_np[qr_slice_y_start:qr_slice_y_end, qr_slice_x_start:qr_slice_x_end, :]

                    # Ensure shapes match after slicing (should be guaranteed now)
                    if bg_area.shape[:2] != fg_area.shape[:2]:
                         # Fallback/debug check - shouldn't be needed with fixed slicing
                        print(f"ERROR: OverlayQRCodeNode - Slice shape mismatch! BG: {bg_area.shape[:2]}, FG: {fg_area.shape[:2]}. Skipping blend.")
                    else:
                       # --- Blend Single Placement Area ---
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

                       # Place the blended area back into the output image copy
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