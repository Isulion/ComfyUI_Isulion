import json
import os
from typing import Dict, List, Tuple, Optional
import requests
import traceback
from PIL import Image
from io import BytesIO
import numpy as np
import torch
import comfy.utils as comfy_utils
import logging
from PIL import ImageOps
import PIL

#Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class IsulionCivitaiImageDisplay:
    """Node that displays Civitai images directly from URLs."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_info": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Paste Civitai image information here..."
                }),
                "mode": (["Single", "All"], {
                    "default": "Single"
                }),
                "image_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "step": 1,
                }),
                "target_size": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 2048,
                    "step": 64
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "title", "prompt", "image_url", "model")
    FUNCTION = "display_image"
    CATEGORY = "Isulion/Prompt Tools"

    def resize_image(self, image, target_size):
        """Resize image to exact target size with padding."""
        # Create a new blank image with the target size
        new_image = Image.new('RGB', (target_size, target_size), (0, 0, 0))
        
        # Calculate scaling factor to fit within target size
        aspect_ratio = image.width / image.height
        if aspect_ratio > 1:
            new_width = target_size
            new_height = int(target_size / aspect_ratio)
        else:
            new_height = target_size
            new_width = int(target_size * aspect_ratio)
            
        # Resize the original image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate position to paste (center)
        paste_x = (target_size - new_width) // 2
        paste_y = (target_size - new_height) // 2
        
        # Paste the resized image onto the new image
        new_image.paste(resized, (paste_x, paste_y))
        
        return new_image

    def create_error_image(self, target_size: int, message: str = "No valid images found"):
        """Create a black image with error message."""
        # Create a black image
        error_image = Image.new('RGB', (target_size, target_size), (0, 0, 0))
        image_tensor = torch.from_numpy(np.array(error_image)).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0)
        return image_tensor

    def display_image(self, image_info: str, mode: str, image_index: int, target_size: int):
        try:
            # Parse image info to get URL
            if isinstance(image_info, list):
                entries = image_info
            else:
                entries = image_info.split("-------------------")
                entries = [entry.strip() for entry in entries if entry.strip()]

            if not entries:
                return (self.create_error_image(target_size), 
                       "No images found", 
                       "No prompt available", 
                       "", 
                       "No model available")

            # Handle "All" mode
            if mode == "All":
                all_tensors = []
                all_titles = []
                all_prompts = []
                all_urls = []
                all_models = []

                for entry in entries:
                    image_data = {}
                    for line in entry.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            image_data[key] = value

                    image_url = image_data.get('URL', '')
                    model = image_data.get('Model', 'Unknown')
                    if not image_url:
                        continue

                    try:
                        response = requests.get(image_url, timeout=10)
                        response.raise_for_status()
                        
                        # Silently skip non-image content
                        content_type = response.headers.get('content-type', '').lower()
                        if not content_type.startswith('image/') or 'video' in content_type:
                            continue

                        image_data = response.content
                        if not image_data:
                            continue

                        image = Image.open(BytesIO(image_data))
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        
                        image = self.resize_image(image, target_size)
                        
                        image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
                        image_tensor = image_tensor.unsqueeze(0)
                        
                        all_tensors.append(image_tensor)
                        all_titles.append(image_data.get('Image', 'Untitled'))
                        all_prompts.append(image_data.get('Prompt', 'No prompt available'))
                        all_urls.append(image_url)
                        all_models.append(model)

                    except:
                        # Silently skip any errors
                        continue

                if not all_tensors:
                    return (self.create_error_image(target_size), 
                           "No valid images found", 
                           "No prompt available", 
                           "", 
                           "No model available")

                final_tensor = torch.cat(all_tensors, dim=0)
 
                return (final_tensor, 
                       " | ".join(all_titles), 
                       " | ".join(all_prompts), 
                       " | ".join(all_urls),
                       " | ".join(all_models))

            else:  # Single mode
                if image_index >= len(entries):
                    return (self.create_error_image(target_size),
                           f"Image index {image_index} out of range (total: {len(entries)})",
                           "No prompt available",
                           "",
                           "No model available")

                # Try each entry starting from image_index until we find a valid image
                for current_index in range(image_index, len(entries)):
                    entry = entries[current_index]
                    image_data = {}
                    for line in entry.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            image_data[key] = value

                    image_url = image_data.get('URL', '')
                    title = image_data.get('Image', 'Untitled')
                    prompt = image_data.get('Prompt', 'No prompt available')
                    model = image_data.get('Model', 'Unknown')

                    if not image_url:
                        continue

                    try:
                        response = requests.get(image_url, timeout=10)
                        response.raise_for_status()
                        
                        # Check if content is an image
                        content_type = response.headers.get('content-type', '').lower()
                        if not content_type.startswith('image/') or 'video' in content_type:
                            continue

                        image_data = response.content
                        if not image_data:
                            continue

                        image = Image.open(BytesIO(image_data))
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        
                        image = self.resize_image(image, target_size)
                        
                        image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
                        image_tensor = image_tensor.unsqueeze(0)
                        
                        return (image_tensor, title, prompt, image_url, model)
                        
                    except:
                        # Silently skip any errors and continue to next entry
                        continue

                # If we get here, no valid images were found
                return (self.create_error_image(target_size),
                       "No valid images found",
                       "No prompt available",
                       "",
                       "No model available")
            
        except Exception as e:
            print(f"Error loading image from URL: {str(e)}")
            return (self.create_error_image(target_size),
                   f"Error: {str(e)}",
                   "No prompt available",
                   "",
                   "No model available")
