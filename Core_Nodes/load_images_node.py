import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

class IsulionLoadImagesNode:
    """
    A flexible image loading node that preserves image characteristics 
    and prepares images for dynamic collage generation.
    """

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
        # Resolve the full path
        try:
            full_directory = folder_paths.get_input_directory(directory)
        except:
            full_directory = os.path.abspath(os.path.expanduser(directory))
        
        # Validate directory exists
        if not os.path.isdir(full_directory):
            raise ValueError(f"Directory does not exist: {full_directory}")
        
        # Supported image extensions
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
        
        # Get all image files in the directory
        image_files = [
            os.path.join(full_directory, f) for f in os.listdir(full_directory)
            if os.path.isfile(os.path.join(full_directory, f)) and 
               os.path.splitext(f)[1].lower() in image_extensions
        ]
        
        # Sort files for consistent order
        image_files.sort()
        
        # Check if any images were found
        if not image_files:
            raise ValueError(f"No images found in directory: {full_directory}")
        
        # Process images
        processed_images = []
        
        for image_path in image_files:
            # Open image
            img = Image.open(image_path)
            
            # Correct orientation
            img = ImageOps.exif_transpose(img)
            
            # Convert to RGB
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
        
        # Convert to tensor without forcing same size
        images_tensor = processed_images
        
        return (images_tensor,)

    @classmethod
    def IS_CHANGED(cls, directory, **kwargs):
        """
        Check if the directory contents have changed.
        """
        image_files = [
            f for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f)) and 
               os.path.splitext(f)[1].lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
        ]
        return hash(tuple(sorted(image_files)))

    @classmethod
    def VALIDATE_INPUTS(cls, directory, **kwargs):
        """
        Validate the input directory.
        
        :param directory: Directory to validate
        :return: True if valid, error message if not
        """
        try:
            # Resolve the full path
            try:
                full_directory = folder_paths.get_input_directory(directory)
            except:
                full_directory = os.path.abspath(os.path.expanduser(directory))
            
            # Check if directory exists
            if not os.path.isdir(full_directory):
                return f"Directory '{directory}' cannot be found."
            
            # Supported image extensions
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp']
            
            # Check if directory has any image files
            image_files = [
                f for f in os.listdir(full_directory)
                if os.path.isfile(os.path.join(full_directory, f)) and 
                   os.path.splitext(f)[1].lower() in image_extensions
            ]
            
            if not image_files:
                return f"No image files in directory '{directory}'."
            
            return True
        except Exception as e:
            return f"Error validating directory: {str(e)}"
