import os
import hashlib
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}

class IsulionLoadImagesNode:
    """
    A flexible image loading node that preserves image characteristics 
    and prepares images for dynamic collage generation.
    """

    @staticmethod
    def _resolve_directory(directory: str) -> str:
        """Resolve user input against ComfyUI's input directory sandbox."""
        directory = directory.strip()
        if os.path.isabs(directory):
            return os.path.abspath(os.path.expanduser(directory))
        return os.path.join(folder_paths.get_input_directory(), directory)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": "./input"}),
                "target_row_height": ("INT", {"default": 300, "min": 100, "max": 1024, "step": 50}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "load_images"
    CATEGORY = "Isulion/Image"

    def load_images(self, directory, target_row_height=300):
        """
        Load images from a directory with intelligent processing.
        
        :param directory: Path to directory containing images
        :param target_row_height: Target height for image rows
        :return: Tensor of processed images
        """
        # Resolve the full path (relative paths are sandboxed to ComfyUI's input dir)
        full_directory = self._resolve_directory(directory)
        
        # Validate directory exists
        if not os.path.isdir(full_directory):
            raise ValueError(f"Directory does not exist: {full_directory}")
        
        # Get all image files in the directory
        image_files = [
            os.path.join(full_directory, f) for f in os.listdir(full_directory)
            if os.path.isfile(os.path.join(full_directory, f)) and 
               os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
        ]
        
        # Sort files for consistent order
        image_files.sort()
        
        # Check if any images were found
        if not image_files:
            raise ValueError(f"No images found in directory: {full_directory}")
        
        # Process images
        processed_images = []
        
        for image_path in image_files:
            with Image.open(image_path) as img:
                # Correct orientation and convert to RGB
                img = ImageOps.exif_transpose(img)
                img = img.convert('RGB')

                # Calculate original aspect ratio
                original_width, original_height = img.size
                aspect_ratio = original_width / original_height

                # Intelligent scaling to target row height
                new_height = target_row_height
                new_width = int(new_height * aspect_ratio)

                # Resize maintaining aspect ratio
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Convert to numpy array and normalize
                img_array = np.array(resized_img).astype(np.float32) / 255.0

            # Convert to tensor
            img_tensor = torch.from_numpy(img_array)

            processed_images.append(img_tensor)
        
        # Pad all images to same dimensions and stack into batched 4D tensor (B, H, W, C)
        max_h = max(img.shape[0] for img in processed_images)
        max_w = max(img.shape[1] for img in processed_images)

        batch = []
        for img in processed_images:
            h, w = img.shape[:2]
            if h == max_h and w == max_w:
                batch.append(img)
            else:
                pad_h = max_h - h
                pad_w = max_w - w
                padded = torch.nn.functional.pad(img, (0, 0, 0, pad_w, 0, pad_h), mode='constant', value=0.0)
                batch.append(padded)

        images_tensor = torch.stack(batch, dim=0)

        return (images_tensor,)

    @classmethod
    def IS_CHANGED(cls, directory, **kwargs):
        """
        Check if the directory contents have changed (deterministic across runs).
        """
        try:
            full_directory = cls._resolve_directory(directory)
            entries = []
            for f in sorted(os.listdir(full_directory)):
                path = os.path.join(full_directory, f)
                if os.path.isfile(path) and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS:
                    stat = os.stat(path)
                    entries.append((f, stat.st_mtime_ns, stat.st_size))
            return hashlib.sha1(repr(entries).encode()).hexdigest()
        except OSError:
            # Missing/unreadable directory: force re-execution so the node
            # raises a proper validation error instead.
            return float("NaN")

    @classmethod
    def VALIDATE_INPUTS(cls, directory, **kwargs):
        """
        Validate the input directory.
        
        :param directory: Directory to validate
        :return: True if valid, error message if not
        """
        try:
            full_directory = cls._resolve_directory(directory)

            # Check if directory exists
            if not os.path.isdir(full_directory):
                return f"Directory '{directory}' cannot be found."

            # Check if directory has any image files
            image_files = [
                f for f in os.listdir(full_directory)
                if os.path.isfile(os.path.join(full_directory, f)) and 
                   os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
            ]

            if not image_files:
                return f"No image files in directory '{directory}'."

            return True
        except Exception as e:
            return f"Error validating directory: {str(e)}"
