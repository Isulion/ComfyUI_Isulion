# Core_Nodes/qrcode_node.py
import torch # type: ignore
import numpy as np
import math
import re # Using built-in 're' for color parsing

# Try to import the bundled qrcodegen module
try:
    # Use relative import to get qrcodegen.py from the same directory
    from . import qrcodegen
    qrcodegen_available = True
except ImportError:
    print("Error: Could not import the bundled 'qrcodegen.py'.")
    print("Please ensure 'qrcodegen.py' is in the same directory as 'qrcode_node.py'.")
    print("Download it from: https://github.com/nayuki/QR-Code-generator/blob/master/python/qrcodegen.py")
    qrcodegen_available = False
except Exception as e:
    print(f"An unexpected error occurred importing qrcodegen: {e}")
    qrcodegen_available = False


# --- Helper Function for Color Parsing ---

def hex_to_rgb(hex_color):
    """Converts a hex color string (e.g., '#FF0000') to an RGB tuple (0-255)."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return None # Indicate error
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return None # Indicate error


# --- The Simplified Node Class ---

class QRCodeNode:
    """
    Generates a QR Code image from input text (e.g., URL).
    Allows customization of colors, scale, border, and an optional logo overlay.
    Uses the bundled 'qrcodegen.py' (no external pip installs needed besides numpy/torch).
    Requires 'qrcodegen.py' in the same directory.
    Place logo file in ComfyUI/input folder and use LoadImage node.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "https://github.com/comfyanonymous/ComfyUI"}),
                "error_correction": (["L", "M", "Q", "H"], {"default": "H"}), # Default High for logo safety
                "scale": ("INT", {"default": 10, "min": 1, "max": 100, "step": 1, "display": "number"}),
                "border": ("INT", {"default": 4, "min": 0, "max": 40, "step": 1, "display": "number"}),
                "foreground_color": ("STRING", {"default": "#000000", "multiline": False}),
                "background_color": ("STRING", {"default": "#FFFFFF", "multiline": False}),
            },
            "optional": {
                 # --- Logo Inputs ---
                 "logo": ("IMAGE",), # Optional input image from LoadImage etc.
                 "logo_scale_percent": ("FLOAT", {"default": 23.0, "min": 5.0, "max": 33.0, "step": 0.5, "display": "number"}), # % of QR Code size (Max ~33% for high ECL)
                 "clear_behind_logo": ("BOOLEAN", {"default": True}), # Recommended for readability
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_qr_code"
    CATEGORY = "image" # Or "utils" or your preferred category
    OUTPUT_NODE = True # Useful for utility nodes

    def generate_qr_code(self, text, error_correction, scale, border,
                         foreground_color, background_color,
                         # Optional inputs
                         logo=None, logo_scale_percent=23.0, clear_behind_logo=True):

        if not qrcodegen_available:
            print("ERROR: QRCodeNode - Bundled 'qrcodegen' module is not available.")
            # Return a dummy tensor to prevent workflow crash
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        data_to_encode = text # Directly use the input text

        if not data_to_encode:
            print("Warning: QRCodeNode - Input text is empty. Generating blank QR code area.")
            # Generate a blank image matching the potential size, or just a small one
            img_size = (border * 2 + 21) * scale # Min size QR (21x21) + border * scale
            img_size = max(64, img_size) # Ensure minimum size
            bg_rgb = hex_to_rgb(background_color) or (255, 255, 255)
            img_np = np.full((img_size, img_size, 3), bg_rgb, dtype=np.uint8)
            img_tensor_out = torch.from_numpy(img_np.astype(np.float32) / 255.0).unsqueeze(0).cpu()
            return (img_tensor_out,)

        # --- 1. Parse Colors ---
        fg_rgb = hex_to_rgb(foreground_color)
        if fg_rgb is None:
            print(f"Warning: QRCodeNode - Invalid foreground color '{foreground_color}'. Using black.")
            fg_rgb = (0, 0, 0)
        bg_rgb = hex_to_rgb(background_color)
        if bg_rgb is None:
            print(f"Warning: QRCodeNode - Invalid background color '{background_color}'. Using white.")
            bg_rgb = (255, 255, 255)

        # --- 2. Generate QR Code Structure ---
        ecl_map = { "L": qrcodegen.QrCode.Ecc.LOW, "M": qrcodegen.QrCode.Ecc.MEDIUM,
                    "Q": qrcodegen.QrCode.Ecc.QUARTILE, "H": qrcodegen.QrCode.Ecc.HIGH }
        ecl = ecl_map.get(error_correction, qrcodegen.QrCode.Ecc.HIGH) # Default H

        try:
            # Automatically select mask pattern (-1 lets library choose)
            qr = qrcodegen.QrCode.encode_text(data_to_encode, ecl)
        except qrcodegen.DataTooLongError as e:
            print(f"ERROR: QRCodeNode - Data too long for QR code capacity with selected Error Correction Level ('{error_correction}'). Try lower ECL or shorter text. Details: {str(e)}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)
        except ValueError as e:
             print(f"ERROR: QRCodeNode - Value error during encoding. May contain characters incompatible with QR standard? Details: {str(e)}")
             return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)
        except Exception as e:
            import traceback
            print(f"ERROR: QRCodeNode - Error generating QR code structure: {str(e)}")
            print(traceback.format_exc())
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        # --- 3. Draw QR Code Base Image ---
        qr_size = qr.get_size()
        if qr_size <= 0:
             print("ERROR: QRCodeNode - QR Code generation resulted in zero or negative size.")
             return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        module_size = qr_size + border * 2
        image_size = module_size * scale

        # Basic check to prevent massive images if scale/border are huge
        if image_size <= 0 or image_size > 16384: # Set a reasonable upper limit
             print(f"ERROR: QRCodeNode - Calculated image size ({image_size}x{image_size}) is invalid or exceeds limit (16384). Check scale/border.")
             return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)

        # Create background image (NumPy H, W, C) using uint8
        try:
            img_np = np.full((image_size, image_size, 3), bg_rgb, dtype=np.uint8)
        except MemoryError:
            print(f"ERROR: QRCodeNode - Not enough memory to create QR code image of size {image_size}x{image_size}.")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)
        except Exception as e:
            print(f"ERROR: QRCodeNode - Failed to create numpy array for QR code: {e}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32),)


        # Draw the QR code modules
        for y in range(qr_size):
            for x in range(qr_size):
                if qr.get_module(x, y): # True if foreground module
                    start_y = (y + border) * scale
                    start_x = (x + border) * scale
                    # Ensure slice coords are within bounds, especially with scale=1
                    end_y = min(start_y + scale, image_size)
                    end_x = min(start_x + scale, image_size)
                    # Check if slice is valid before assignment
                    if start_y < end_y and start_x < end_x:
                       img_np[start_y : end_y, start_x : end_x] = fg_rgb

        # --- 4. Handle Optional Logo ---
        if logo is not None and logo.numel() > 0:
            if ecl == qrcodegen.QrCode.Ecc.LOW:
                print("Warning: QRCodeNode - Using a logo with LOW error correction is not recommended and may make the QR code unscannable.")
            elif ecl == qrcodegen.QrCode.Ecc.MEDIUM and logo_scale_percent > 20:
                 print("Warning: QRCodeNode - Using a logo > 20% scale with MEDIUM error correction might impact scannability.")

            try:
                # --- Logo Processing ---
                logo_input_tensor = logo # Should be B, H, W, C float tensor from ComfyUI
                # Take first image in batch, move to CPU, convert to NumPy H, W, C
                logo_np = logo_input_tensor[0].cpu().numpy()

                # Handle potential greyscale input (H, W) or (H, W, 1)
                if logo_np.ndim == 2:
                    logo_np = np.stack((logo_np,) * 3, axis=-1)
                elif logo_np.ndim == 3 and logo_np.shape[2] == 1:
                     logo_np = np.concatenate((logo_np,) * 3, axis=-1)

                # Convert float [0,1] to uint8 [0,255] AFTER potential channel manipulation
                logo_np = np.clip(logo_np * 255.0, 0, 255).astype(np.uint8)
                logo_h, logo_w, logo_c = logo_np.shape # Should now have 3 or 4 channels

                # Calculate logo dimensions based on scale percentage relative to DATA area
                qr_data_area_size_pixels = qr_size * scale
                max_logo_dim = int(qr_data_area_size_pixels * (logo_scale_percent / 100.0))
                max_logo_dim = max(1, max_logo_dim) # Ensure at least 1 pixel

                # Determine target size, maintaining aspect ratio
                aspect_ratio = logo_w / logo_h if logo_h > 0 else 1
                if logo_w >= logo_h:
                    target_w = max_logo_dim
                    target_h = max(1, int(target_w / aspect_ratio))
                else:
                    target_h = max_logo_dim
                    target_w = max(1, int(target_h * aspect_ratio))

                if target_w > 0 and target_h > 0:
                    # --- Resize using torch interpolation ---
                    # Convert logo back to float tensor NCHW format for interpolate (on CPU)
                    logo_tensor_for_resize = torch.from_numpy(logo_np.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0).cpu()

                    resized_logo_tensor = torch.nn.functional.interpolate(
                        logo_tensor_for_resize, size=(target_h, target_w), mode='bicubic', align_corners=False
                    )
                    # Convert back to HWC uint8 NumPy array on CPU
                    resized_logo_np = (resized_logo_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
                    # --- End Resize ---

                    # Calculate top-left position to center the logo
                    offset_x = max(0, (image_size - target_w) // 2)
                    offset_y = max(0, (image_size - target_h) // 2)

                    # Define target slice in the main image, ensure it's within bounds
                    slice_y = slice(offset_y, min(offset_y + target_h, image_size))
                    slice_x = slice(offset_x, min(offset_x + target_w, image_size))

                    # Get actual dimensions of the slice in the target image
                    bg_slice_shape = img_np[slice_y, slice_x].shape
                    # Adjust logo if slice is smaller than logo (e.g., logo near edge)
                    logo_to_blend = resized_logo_np[:bg_slice_shape[0], :bg_slice_shape[1], :]

                    # Check if logo_to_blend is valid before proceeding
                    if logo_to_blend.size == 0:
                        print("Warning: QRCodeNode - Logo placement resulted in zero-sized area. Skipping overlay.")
                    else:
                        # Clear area behind logo if requested
                        if clear_behind_logo:
                            img_np[slice_y, slice_x] = bg_rgb

                        # Blend logo (handle transparency if alpha channel exists)
                        current_bg_area = img_np[slice_y, slice_x]

                        if logo_c == 4: # RGBA
                            alpha_channel = logo_to_blend[:, :, 3:4] / 255.0 # Keep shape (H, W, 1)
                            rgb_logo = logo_to_blend[:, :, :3]

                            bg_area_float = current_bg_area.astype(np.float32)
                            rgb_logo_float = rgb_logo.astype(np.float32)

                            blended_area = rgb_logo_float * alpha_channel + bg_area_float * (1.0 - alpha_channel)
                            img_np[slice_y, slice_x] = np.clip(blended_area, 0, 255).astype(np.uint8)

                        elif logo_c == 3: # RGB (or converted grayscale)
                            img_np[slice_y, slice_x] = logo_to_blend[:,:,:3] # Direct overwrite

                        else: # Should not happen after grayscale conversion, but check
                            print(f"Warning: QRCodeNode - Logo has unexpected channel count ({logo_c}) during blending. Skipping overlay.")
                else:
                    print("Warning: QRCodeNode - Calculated logo dimensions are zero or negative. Skipping overlay.")

            except Exception as e:
                import traceback
                print(f"ERROR: QRCodeNode - Error processing or overlaying logo: {str(e)}")
                print(traceback.format_exc()) # Print detailed traceback
                # Continue without logo if it fails

        # --- 5. Convert Final Image to Torch Tensor ---
        # Normalize to [0, 1] and ensure float32, add batch dim
        # Ensure output tensor is on CPU
        img_tensor_out = torch.from_numpy(img_np.astype(np.float32) / 255.0).unsqueeze(0).cpu()

        return (img_tensor_out,)


# --- ComfyUI Mappings ---
NODE_CLASS_MAPPINGS = {
    "🧩 IsulionQRCode": QRCodeNode  # Use the original name mapping
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "🧩 IsulionQRCode": "🧩 Isulion QRCode" # Use the original display name
}