# Core_Nodes/qrcode_node.py
import torch
import numpy as np
import math
import re # Using built-in 're' for color parsing
import traceback # For detailed error printing

# Try to import the bundled qrcodegen module
try:
    from . import qrcodegen
    qrcodegen_available = True
except ImportError:
    print("ERROR: QRCodeNode - Could not import the bundled 'qrcodegen.py'.")
    print("Please ensure 'qrcodegen.py' is in the same directory as 'qrcode_node.py'.")
    print("Download it from: https://github.com/nayuki/QR-Code-generator/blob/master/python/qrcodegen.py")
    qrcodegen_available = False
except Exception as e:
    print(f"ERROR: QRCodeNode - An unexpected error occurred importing qrcodegen: {e}")
    qrcodegen_available = False

# --- Helper Function for Color Parsing ---

def hex_to_rgb(hex_color):
    """Converts a hex color string (e.g., '#FF0000') to an RGB tuple (0-255). Returns None on error."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return None
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return None

# --- The Node Class ---

class QRCodeNode:
    """
    Generates a QR Code image from input text (e.g., URL).
    Allows customization of colors, scale, border, optional logo overlay,
    and optional transparent background. Supports RGBA input logos.
    Uses the bundled 'qrcodegen.py'. Requires 'qrcodegen.py' in the same directory.
    NOTE: ComfyUI preview might not display transparency correctly; verify with SaveImage (PNG).
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "https://civitai.com/user/Isulion"}),
                "error_correction": (["L", "M", "Q", "H"], {"default": "H"}),
                "scale": ("INT", {"default": 10, "min": 1, "max": 100, "step": 1, "display": "number"}),
                "border": ("INT", {"default": 4, "min": 0, "max": 40, "step": 1, "display": "number"}),
                "foreground_color": ("STRING", {"default": "#000000", "multiline": False}),
                "background_color": ("STRING", {"default": "#FFFFFF", "multiline": False}),
                "transparent_background": ("BOOLEAN", {"default": False}), # Option for transparency
            },
            "optional": {
                 "logo": ("IMAGE",), # Optional input image (expects B, H, W, C float tensor)
                 "logo_scale_percent": ("FLOAT", {"default": 23.0, "min": 5.0, "max": 33.0, "step": 0.5, "display": "number"}),
                 "clear_behind_logo": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",) # Output is IMAGE type, ComfyUI handles RGBA (B, H, W, 4)
    FUNCTION = "generate_qr_code"
    CATEGORY = "image"
    OUTPUT_NODE = True

    def generate_qr_code(self, text, error_correction, scale, border,
                         foreground_color, background_color, transparent_background,
                         logo=None, logo_scale_percent=23.0, clear_behind_logo=True):

        # Determine output channels and create a dummy tensor for error returns
        output_channels = 4 if transparent_background else 3
        # Create dummy tensor matching expected output channels
        dummy_tensor = torch.zeros((1, 64, 64, output_channels), dtype=torch.float32)

        if not qrcodegen_available:
            print("ERROR: QRCodeNode - Bundled 'qrcodegen' module is not available.")
            return (dummy_tensor,)

        data_to_encode = text

        # --- 1. Parse Colors and Define Final Color Tuples (RGB or RGBA) ---
        fg_rgb = hex_to_rgb(foreground_color) or (0, 0, 0)
        bg_rgb = hex_to_rgb(background_color) or (255, 255, 255)

        if transparent_background:
            print("INFO: QRCodeNode - Generating RGBA image with transparent background.")
            # Foreground is opaque black/color, Background is transparent white/color
            final_fg_color = fg_rgb + (255,) # RGBA, Alpha=255 (Opaque)
            final_bg_color = bg_rgb + (0,)   # RGBA, Alpha=0   (Transparent)
            final_channels = 4
        else:
            # Standard RGB
            final_fg_color = fg_rgb # RGB
            final_bg_color = bg_rgb # RGB
            final_channels = 3

        # Handle empty text input gracefully
        if not data_to_encode:
            print("Warning: QRCodeNode - Input text is empty. Generating blank QR code area.")
            img_size = max(64, (border * 2 + 21) * scale) # Estimate minimum size
            try:
                # Use the determined final background color and channels
                img_np = np.full((img_size, img_size, final_channels), final_bg_color, dtype=np.uint8)
                img_tensor_out = torch.from_numpy(img_np.astype(np.float32) / 255.0).unsqueeze(0).cpu()
                return (img_tensor_out,)
            except Exception as e:
                 print(f"ERROR: QRCodeNode - Failed to create blank image: {e}")
                 return (dummy_tensor,)

        # --- 2. Generate QR Code Structure ---
        ecl_map = { "L": qrcodegen.QrCode.Ecc.LOW, "M": qrcodegen.QrCode.Ecc.MEDIUM,
                    "Q": qrcodegen.QrCode.Ecc.QUARTILE, "H": qrcodegen.QrCode.Ecc.HIGH }
        ecl = ecl_map.get(error_correction, qrcodegen.QrCode.Ecc.HIGH)

        try:
            qr = qrcodegen.QrCode.encode_text(data_to_encode, ecl)
        except qrcodegen.DataTooLongError as e:
            print(f"ERROR: QRCodeNode - Data too long. Reduce text or lower Error Correction ('{error_correction}'). Details: {str(e)}")
            return (dummy_tensor,)
        except ValueError as e:
             print(f"ERROR: QRCodeNode - Value error during encoding (invalid chars?). Details: {str(e)}")
             return (dummy_tensor,)
        except Exception as e:
            print(f"ERROR: QRCodeNode - Error generating QR code structure: {str(e)}\n{traceback.format_exc()}")
            return (dummy_tensor,)

        # --- 3. Draw QR Code Base Image (RGB or RGBA) ---
        qr_size = qr.get_size()
        if qr_size <= 0:
             print("ERROR: QRCodeNode - QR Code generation resulted in zero size.")
             return (dummy_tensor,)

        module_size = qr_size + border * 2
        image_size = module_size * scale

        if image_size <= 0 or image_size > 16384: # Size check
             print(f"ERROR: QRCodeNode - Invalid calculated image size ({image_size}x{image_size}). Check scale/border.")
             return (dummy_tensor,)

        # Create base image with the correct number of channels and background color
        try:
            # Use final_channels and final_bg_color determined earlier
            img_np = np.full((image_size, image_size, final_channels), final_bg_color, dtype=np.uint8)
        except MemoryError:
            print(f"ERROR: QRCodeNode - Not enough memory for {image_size}x{image_size}x{final_channels} image.")
            return (dummy_tensor,)
        except Exception as e:
            print(f"ERROR: QRCodeNode - Failed to create numpy array for QR code: {e}")
            return (dummy_tensor,)

        # Draw the QR code modules using the final foreground color (RGB or RGBA)
        for y in range(qr_size):
            for x in range(qr_size):
                if qr.get_module(x, y): # True if foreground module
                    start_y, start_x = (y + border) * scale, (x + border) * scale
                    end_y, end_x = min(start_y + scale, image_size), min(start_x + scale, image_size)
                    if start_y < end_y and start_x < end_x:
                       img_np[start_y : end_y, start_x : end_x] = final_fg_color # Use final FG color

        # --- 4. Handle Optional Logo ---
        if logo is not None and logo.numel() > 0:
            # Warnings about ECL vs logo size
            if ecl == qrcodegen.QrCode.Ecc.LOW: print("Warning: QRCodeNode - Using logo with LOW ECL is not recommended.")
            elif ecl == qrcodegen.QrCode.Ecc.MEDIUM and logo_scale_percent > 20: print("Warning: QRCodeNode - Logo > 20% with MEDIUM ECL might impact scannability.")

            try:
                # --- 4a. Prepare Input Logo ---
                logo_input_tensor = logo # B, H, W, C float
                if logo_input_tensor.shape[0] > 1: print("Warning: QRCodeNode - Multiple logos in batch, using only the first one.")
                logo_np_float = logo_input_tensor[0].cpu().numpy() # H, W, C float [0, 1]

                # Check input logo channels and handle grayscale
                input_logo_channels = logo_np_float.shape[2] if logo_np_float.ndim == 3 else 1
                input_has_alpha = False
                if logo_np_float.ndim == 2: # Grayscale (H, W)
                    print("INFO: QRCodeNode - Input logo is grayscale, converting to RGB.")
                    logo_np_float = np.stack((logo_np_float,) * 3, axis=-1) # -> H, W, 3
                    input_logo_channels = 3
                elif input_logo_channels == 1: # Grayscale (H, W, 1)
                     print("INFO: QRCodeNode - Input logo is grayscale (1 channel), converting to RGB.")
                     logo_np_float = np.concatenate((logo_np_float,) * 3, axis=-1) # -> H, W, 3
                     input_logo_channels = 3
                elif input_logo_channels == 4: # RGBA
                    print("INFO: QRCodeNode - Input logo has alpha channel.")
                    input_has_alpha = True
                elif input_logo_channels != 3: # RGB
                     print(f"Warning: QRCodeNode - Input logo has unsupported channel count ({input_logo_channels}). Treating as RGB.")
                     logo_np_float = logo_np_float[:, :, :3] # Take first 3 channels if > 4? Risky. Better to just treat as RGB.
                     input_logo_channels = 3

                # Convert prepared logo (RGB or RGBA float) to uint8
                logo_np_uint8 = np.clip(logo_np_float * 255.0, 0, 255).astype(np.uint8)
                logo_h, logo_w = logo_np_uint8.shape[:2]

                # --- 4b. Calculate Logo Size and Position ---
                qr_data_area_size_pixels = qr_size * scale
                max_logo_dim = max(1, int(qr_data_area_size_pixels * (logo_scale_percent / 100.0)))
                aspect_ratio = logo_w / logo_h if logo_h > 0 else 1
                target_w = max_logo_dim if logo_w >= logo_h else max(1, int(max_logo_dim * aspect_ratio))
                target_h = max_logo_dim if logo_h > logo_w else max(1, int(max_logo_dim / aspect_ratio))

                if target_w <= 0 or target_h <= 0:
                    print("Warning: QRCodeNode - Calculated logo dimensions are zero/negative. Skipping overlay.")
                else:
                    # --- 4c. Resize Logo ---
                    # Resize using torch interpolation (requires float NCHW)
                    logo_tensor_for_resize = torch.from_numpy(logo_np_uint8.astype(np.float32) / 255.0).permute(2, 0, 1).unsqueeze(0).cpu()
                    resized_logo_tensor = torch.nn.functional.interpolate(
                        logo_tensor_for_resize, size=(target_h, target_w), mode='bicubic', align_corners=False
                    )
                    # Convert back to HWC uint8 NumPy array
                    resized_logo_np = (resized_logo_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
                    resized_logo_channels = resized_logo_np.shape[2]

                    # --- 4d. Calculate Placement ---
                    offset_x = max(0, (image_size - target_w) // 2)
                    offset_y = max(0, (image_size - target_h) // 2)
                    slice_y = slice(offset_y, min(offset_y + target_h, image_size))
                    slice_x = slice(offset_x, min(offset_x + target_w, image_size))

                    # Adjust logo size if placement goes out of bounds
                    bg_slice_shape = img_np[slice_y, slice_x].shape
                    logo_to_blend = resized_logo_np[:bg_slice_shape[0], :bg_slice_shape[1], :]

                    if logo_to_blend.size == 0:
                        print("Warning: QRCodeNode - Logo placement resulted in zero-sized area. Skipping overlay.")
                    else:
                        # --- 4e. Clear Background Area ---
                        if clear_behind_logo:
                            # Use the final background color (RGB or RGBA)
                            img_np[slice_y, slice_x] = final_bg_color

                        # --- 4f. Blend Logo onto QR Image ---
                        # Perform calculations using float32 for precision
                        current_bg_area_float = img_np[slice_y, slice_x].astype(np.float32) / 255.0
                        logo_to_blend_float = logo_to_blend.astype(np.float32) / 255.0

                        final_blended_area_float = current_bg_area_float # Initialize with background

                        # Extract logo alpha (assume 1.0 if logo is RGB)
                        logo_alpha = logo_to_blend_float[:, :, 3:4] if resized_logo_channels == 4 else np.ones_like(logo_to_blend_float[:, :, 0:1])

                        # Extract background alpha (use 1.0 if background is RGB)
                        bg_alpha = current_bg_area_float[:, :, 3:4] if final_channels == 4 else np.ones_like(current_bg_area_float[:, :, 0:1])

                        # Blend RGB channels using "over" compositing: Co = Fa*alpha_f + Ba*(1-alpha_f)
                        # Ensure logo has 3 channels for RGB blending
                        logo_rgb = logo_to_blend_float[:, :, :3]
                        bg_rgb = current_bg_area_float[:, :, :3]
                        blended_rgb = logo_rgb * logo_alpha + bg_rgb * (1.0 - logo_alpha)

                        # Calculate output alpha using "over" compositing: Ao = alpha_f + alpha_b*(1-alpha_f)
                        blended_alpha = logo_alpha + bg_alpha * (1.0 - logo_alpha)

                        if final_channels == 4: # RGBA Output
                            final_blended_area_float = np.concatenate((blended_rgb, blended_alpha), axis=2)
                        else: # RGB Output
                            final_blended_area_float = blended_rgb # Discard calculated alpha

                        # Convert back to uint8 and assign to the main image
                        blended_area_uint8 = np.clip(final_blended_area_float * 255.0, 0, 255).astype(np.uint8)
                        img_np[slice_y, slice_x] = blended_area_uint8

            except Exception as e:
                print(f"ERROR: QRCodeNode - Error processing or overlaying logo: {str(e)}\n{traceback.format_exc()}")
                # Continue without logo if processing fails

        # --- 5. Convert Final Image to Torch Tensor ---
        try:
            # Convert the final NumPy array (potentially RGBA) to tensor
            img_tensor_out = torch.from_numpy(img_np.astype(np.float32) / 255.0).unsqueeze(0).cpu()
            # Final check on tensor shape
            if img_tensor_out.shape[3] != final_channels:
                 print(f"ERROR: QRCodeNode - Final tensor channel mismatch! Expected {final_channels}, got {img_tensor_out.shape[3]}. Returning dummy.")
                 return (dummy_tensor,)
            # print(f"DEBUG: QRCodeNode - Output tensor shape: {img_tensor_out.shape}") # Optional debug
        except Exception as e:
            print(f"ERROR: QRCodeNode - Failed to convert final numpy array to tensor: {e}")
            return (dummy_tensor,)

        return (img_tensor_out,)


# --- ComfyUI Mappings ---
NODE_CLASS_MAPPINGS = {
    "🧩 IsulionQRCode": QRCodeNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "🧩 IsulionQRCode": "🧩 Isulion QRCode"
}