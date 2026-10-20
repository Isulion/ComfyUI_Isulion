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
        """Resolve user input strictly inside ComfyUI's input directory sandbox."""
        directory = directory.strip()
        if os.path.isabs(directory):
            raise ValueError(f"Directory escapes input sandbox: {directory} (move the folder into ComfyUI/input and give a relative path)")
        base = os.path.realpath(folder_paths.get_input_directory())
        candidate = os.path.realpath(os.path.join(base, directory.lstrip("/\\")))
        if candidate != base and not candidate.startswith(base + os.sep):
            raise ValueError(f"Directory escapes input sandbox: {directory} (move the folder into ComfyUI/input and give a relative path)")
        return candidate

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
    # Output a LIST of variable-size tensors so downstream nodes (e.g.
    # IsuCollage) receive every image at its own native size instead of a
    # uniform batch distorted by padding.
    OUTPUT_IS_LIST = (True,)

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
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Convert to numpy array and normalize
                img_array = np.array(resized_img).astype(np.float32) / 255.0

            # Convert to tensor
            img_tensor = torch.from_numpy(img_array)

            processed_images.append(img_tensor)

        # Return the list as-is: each image keeps its own size (no padding),
        # preserving native aspect ratios for downstream collage layout.
        return (processed_images,)

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
        except (OSError, ValueError):
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
