# Core_Nodes/overlay_node.py
import torch
import numpy as np
import math
import traceback # For detailed error printing

class OverlayQRCodeNode:
    """
    Overlays a QR Code image (or any image with potential transparency)
    onto a base image with options for alignment, size, opacity, and margin.
    Handles RGBA inputs and outputs an RGBA image.
    """

    # Define alignment options
    ALIGN_VERT = ["top", "bottom", "center"]
    ALIGN_HORIZ = ["left", "right", "center"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE",), # Expects B, H, W, C tensor
                "qr_code_image": ("IMAGE",), # Expects B, H, W, C tensor (RGBA preferred)
                "vertical_align": (cls.ALIGN_VERT, {"default": "bottom"}),
                "horizontal_align": (cls.ALIGN_HORIZ, {"default": "right"}),
                "size_percent": ("FLOAT", {"default": 20.0, "min": 1.0, "max": 100.0, "step": 0.5, "display": "slider"}),
                "opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01, "display": "slider"}),
                "margin_percent": ("FLOAT", {"default": 2.0, "min": 0.0, "max": 50.0, "step": 0.1, "display": "slider"}), # Margin from edge
            }
        }

    RETURN_TYPES = ("IMAGE",) # Output is always RGBA IMAGE
    FUNCTION = "overlay_qr"
    CATEGORY = "image/postprocessing" # Or your preferred category
    OUTPUT_NODE = True

    def overlay_qr(self, base_image, qr_code_image,
                   vertical_align, horizontal_align,
                   size_percent, opacity, margin_percent):

        # --- Input Validation and Preparation ---
        # Create a dummy RGBA tensor for error returns first
        dummy_tensor = torch.zeros((1, 64, 64, 4), dtype=torch.float32)

        if base_image is None or qr_code_image is None:
            print("ERROR: OverlayQRCodeNode - Missing base_image or qr_code_image input.")
            return (dummy_tensor,)

        if base_image.dim() != 4 or qr_code_image.dim() != 4:
             print("ERROR: OverlayQRCodeNode - Inputs must be 4D tensors (B, H, W, C).")
             return (dummy_tensor,)

        # Work with the first image in the batch
        base_img_tensor = base_image[0] # H, W, C
        qr_img_tensor = qr_code_image[0]   # H, W, C

        base_h, base_w, base_c = base_img_tensor.shape
        qr_h, qr_w, qr_c = qr_img_tensor.shape

        # --- Ensure RGBA format internally (float32, 0-1 range) ---
        # Convert Base Image to RGBA float32 numpy
        base_img_np = base_img_tensor.cpu().numpy()
        if base_c == 3: # RGB to RGBA (add opaque alpha)
            alpha_channel = np.ones((base_h, base_w, 1), dtype=np.float32)
            base_img_np_rgba = np.concatenate((base_img_np, alpha_channel), axis=2)
        elif base_c == 4: # Already RGBA
            base_img_np_rgba = base_img_np
        else:
            print(f"ERROR: OverlayQRCodeNode - Base image has unsupported channel count: {base_c}")
            return (dummy_tensor,)

        # Convert QR Code Image to RGBA float32 numpy
        qr_img_np = qr_img_tensor.cpu().numpy()
        if qr_c == 3: # RGB to RGBA (assume opaque overlay)
            alpha_channel = np.ones((qr_h, qr_w, 1), dtype=np.float32)
            qr_img_np_rgba = np.concatenate((qr_img_np, alpha_channel), axis=2)
        elif qr_c == 4: # Already RGBA
             qr_img_np_rgba = qr_img_np
        else:
            print(f"ERROR: OverlayQRCodeNode - QR Code image has unsupported channel count: {qr_c}")
            return (dummy_tensor,)

        # --- Calculate Target QR Size ---
        base_ref_dim = min(base_h, base_w)
        target_qr_dim = max(1, int(base_ref_dim * (size_percent / 100.0)))
        qr_aspect_ratio = qr_w / qr_h if qr_h > 0 else 1
        if qr_w >= qr_h:
            target_qr_w = target_qr_dim
            target_qr_h = max(1, int(target_qr_w / qr_aspect_ratio))
        else:
            target_qr_h = target_qr_dim
            target_qr_w = max(1, int(target_qr_h * qr_aspect_ratio))

        # --- Resize QR Code ---
        if target_qr_h <= 0 or target_qr_w <= 0:
             print(f"ERROR: OverlayQRCodeNode - Calculated target QR size is invalid ({target_qr_h}x{target_qr_w}).")
             # Return original base RGBA wrapped in batch dim
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        try:
            qr_tensor_nchw = torch.from_numpy(qr_img_np_rgba).permute(2, 0, 1).unsqueeze(0).cpu()
            resized_qr_tensor_nchw = torch.nn.functional.interpolate(
                qr_tensor_nchw, size=(target_qr_h, target_qr_w), mode='bicubic', align_corners=False
            )
            resized_qr_np = resized_qr_tensor_nchw.squeeze(0).permute(1, 2, 0).numpy() # H, W, 4 float32
        except Exception as e:
             print(f"ERROR: OverlayQRCodeNode - Failed to resize QR Code: {e}\n{traceback.format_exc()}")
             return (torch.from_numpy(base_img_np_rgba).unsqueeze(0).cpu(),)

        # --- Apply Opacity to Resized QR Code Alpha ---
        clamped_opacity = max(0.0, min(1.0, opacity))
        resized_qr_np[:, :, 3] *= clamped_opacity

        # --- Calculate Position and Slices ---
        margin_px_h = int(base_h * (margin_percent / 100.0))
        margin_px_w = int(base_w * (margin_percent / 100.0))

        if vertical_align == "top": y_start = margin_px_h
        elif vertical_align == "bottom": y_start = base_h - target_qr_h - margin_px_h
        else: y_start = (base_h - target_qr_h) // 2

        if horizontal_align == "left": x_start = margin_px_w
        elif horizontal_align == "right": x_start = base_w - target_qr_w - margin_px_w
        else: x_start = (base_w - target_qr_w) // 2

        y_end = y_start + target_qr_h
        x_end = x_start + target_qr_w

        base_slice_y_start = max(0, y_start)
        base_slice_y_end = min(base_h, y_end)
        base_slice_x_start = max(0, x_start)
        base_slice_x_end = min(base_w, x_end)

        qr_slice_y_start = max(0, -y_start)
        qr_slice_x_start = max(0, -x_start)
        qr_slice_y_end = min(target_qr_h, base_h - y_start)
        qr_slice_x_end = min(target_qr_w, base_w - x_start)

        # --- Perform Alpha Compositing ("Over" operation) ---
        output_img_np = base_img_np_rgba.copy() # Start with a copy of the base image

        try:
            # Check for valid overlap dimensions
            if base_slice_y_start >= base_slice_y_end or base_slice_x_start >= base_slice_x_end or \
               qr_slice_y_start >= qr_slice_y_end or qr_slice_x_start >= qr_slice_x_end:
                print("Warning: OverlayQRCodeNode - QR code placement results in no overlap or invalid slice.")
                # No overlap or invalid slice, return the base image (already copied to output_img_np)
            else:
                # Extract the overlapping background area (RGBA float 0-1)
                bg_area = base_img_np_rgba[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :]

                # Extract the corresponding foreground QR area (RGBA float 0-1)
                fg_area = resized_qr_np[qr_slice_y_start:qr_slice_y_end, qr_slice_x_start:qr_slice_x_end, :]

                # Ensure shapes match after slicing
                if bg_area.shape[:2] != fg_area.shape[:2]:
                    print(f"ERROR: OverlayQRCodeNode - Slice shape mismatch after slicing! BG: {bg_area.shape}, FG: {fg_area.shape}. Cropping FG.")
                    # Attempt to crop fg_area to bg_area size
                    fg_area = fg_area[:bg_area.shape[0], :bg_area.shape[1], :]
                    if bg_area.shape[:2] != fg_area.shape[:2]: # Check again
                        print("ERROR: OverlayQRCodeNode - Fallback crop failed. Skipping blending.")
                        # Return the unmodified base image copy
                        return (torch.from_numpy(output_img_np).unsqueeze(0).cpu(),)

                # Separate FG and BG channels (RGBA)
                fg_rgb = fg_area[:, :, :3]
                fg_alpha = fg_area[:, :, 3:4] # Keep dimensions H, W, 1
                bg_rgb = bg_area[:, :, :3]
                bg_alpha = bg_area[:, :, 3:4] # Keep dimensions H, W, 1

                # Calculate output alpha: Ao = αf + αb * (1 - αf)
                out_alpha = fg_alpha + bg_alpha * (1.0 - fg_alpha)

                # --- FIX START ---
                # Calculate output RGB numerator: C_num = Cf * αf + Cb * αb * (1 - αf)
                numerator = (fg_rgb * fg_alpha) + (bg_rgb * bg_alpha * (1.0 - fg_alpha))

                # Calculate final RGB: Co = C_num / Ao
                # Avoid division by zero where out_alpha is zero using a small epsilon
                # Use np.where for safe division and selection based on alpha
                epsilon = 1e-7
                safe_alpha_mask = out_alpha > epsilon # Shape (H, W, 1)

                # Calculate division result safely (result is zero where mask is false)
                # The division broadcasting works correctly here numerator(H,W,3)/out_alpha(H,W,1)
                # We add epsilon to denominator to prevent true zero division warnings/errors
                divided_rgb = numerator / (out_alpha + epsilon)

                # Use np.where to select the blended color or the original background color
                # np.where broadcasts the (H, W, 1) mask correctly against the (H, W, 3) arrays
                out_rgb = np.where(safe_alpha_mask, divided_rgb, bg_rgb)
                # --- FIX END ---

                # Combine RGB and Alpha
                blended_area = np.concatenate((out_rgb, out_alpha), axis=2)

                # Clip results to ensure they are in [0, 1] range
                blended_area = np.clip(blended_area, 0.0, 1.0)

                # Place the blended area back into the output image copy
                output_img_np[base_slice_y_start:base_slice_y_end, base_slice_x_start:base_slice_x_end, :] = blended_area

        except Exception as e:
             print(f"ERROR: OverlayQRCodeNode - Error during alpha blending: {e}\n{traceback.format_exc()}")
             # Return original base image copy on error during blending

        # --- Convert Final Image to Torch Tensor ---
        try:
            # Output tensor should be B, H, W, 4 (RGBA)
            output_tensor = torch.from_numpy(output_img_np).unsqueeze(0).cpu()
        except Exception as e:
            print(f"ERROR: OverlayQRCodeNode - Failed to convert final numpy array to tensor: {e}")
            return (dummy_tensor,) # Return dummy on final conversion error

        return (output_tensor,)

# --- ComfyUI Mappings ---
NODE_CLASS_MAPPINGS = {
    "⧉ IsulionOverlay": OverlayQRCodeNode 
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "⧉ IsulionOverlay": "⧉ IsulionOverlay" 
}