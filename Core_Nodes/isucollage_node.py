import torch
import math
import random
import numpy

class IsuCollageNode:
    """
    Intelligent Image Collage Generator
    Preserving image characteristics, inspired by react-isucollage
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "seed": ("INT", {"optional": True})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("collage_image",)
    FUNCTION = "create_collage"
    CATEGORY = "Isulion/Image"

    def create_collage(self, images, seed=None):
        """
        Create a collage from input images with optional seed for randomization.
        
        :param images: List of input image tensors
        :param seed: Random seed for image placement
        :return: Tuple containing the collage tensor
        """
        # Set random seed if provided
        if seed is not None:
            torch.manual_seed(seed)
            random.seed(seed)
            numpy.random.seed(seed)
        
        # Shuffle images if seed is set
        shuffled_images = list(images)
        if seed is not None:
            random.shuffle(shuffled_images)
        
        # Handle edge cases
        if not shuffled_images:
            raise ValueError("No images provided")
        if len(shuffled_images) == 1:
            # Ensure the single image is in the correct 4D format
            single_image = shuffled_images[0]
            if len(single_image.shape) == 3:
                single_image = single_image.unsqueeze(0)
            return (single_image,)

        # Ensure all images are in the correct format (H, W, C)
        processed_images = []
        for img in shuffled_images:
            # Convert 4D tensor to 3D if needed
            if len(img.shape) == 4:
                img = img.squeeze(0)
            processed_images.append(img)
        
        # Distribute images into rows
        rows = self._distribute_images(processed_images)
        
        # Normalize rows
        normalized_rows = self._normalize_rows(rows, 300)
        
        # Stack rows to create final collage
        collage_tensor = self._stack_rows(normalized_rows)
        
        # Ensure output is a 4D tensor (B, H, W, C)
        if len(collage_tensor.shape) == 3:
            collage_tensor = collage_tensor.unsqueeze(0)
        
        # Return as a single-element tuple for ComfyUI
        return (collage_tensor,)

    def _distribute_images(self, images):
        """
        Distribute images across rows to maximize canvas utilization.
        
        :param images: List of image tensors
        :return: List of rows with distributed images
        """
        # Sort images by aspect ratio in descending order
        aspect_ratios = [
            img.shape[1] / img.shape[0]  # Width / Height 
            for img in images
        ]
        sorted_indices = sorted(
            range(len(aspect_ratios)), 
            key=lambda k: aspect_ratios[k], 
            reverse=True
        )
        
        # Compute optimal row configuration
        num_images = len(images)
        num_rows = max(1, math.ceil(math.sqrt(num_images)))
        
        # Initialize rows
        rows = [[] for _ in range(num_rows)]
        
        # Distribute images across rows
        for idx in sorted_indices:
            # Find row with least total width
            target_row = min(range(num_rows), key=lambda r: sum(
                img.shape[1] for img in rows[r]
            ))
            rows[target_row].append(images[idx])
        
        return rows

    def _normalize_rows(self, rows, target_height):
        """
        Normalize rows to completely fill the canvas with no empty spaces.
        
        :param rows: List of image rows
        :param target_height: Desired row height
        :return: Normalized rows of images
        """
        # Find the maximum total width across all rows
        max_total_width = max(
            sum(img.shape[1] for img in row) 
            for row in rows
        )
        
        normalized_rows = []
        for row in rows:
            # Skip empty rows
            if not row:
                continue
            
            # Compute consistent height for the row
            row_heights = [img.shape[0] for img in row]
            consistent_height = min(row_heights)
            
            # Resize images to consistent height and calculate total width
            resized_row = []
            for img in row:
                # Ensure tensor has 3 dimensions (H, W, C)
                if len(img.shape) == 4:
                    img = img.squeeze(0)
                
                # Calculate new width maintaining aspect ratio
                aspect_ratio = img.shape[1] / img.shape[0]
                new_width = int(consistent_height * aspect_ratio)
                
                # Resize image
                resized_img = self._resize_to_exact(
                    img, 
                    (consistent_height, new_width)
                )
                resized_row.append(resized_img)
            
            # Normalize row width precisely
            normalized_row = self._normalize_row_width(resized_row, max_total_width)
            normalized_rows.append(normalized_row)
        
        return normalized_rows

    def _normalize_row_width(self, row, target_width):
        """
        Normalize a single row to match the target width while preserving aspect ratios.
        
        :param row: List of image tensors in a row
        :param target_width: Desired total width for the row
        :return: Normalized row with images scaled to match target width
        """
        # Calculate total width and get scaling factor
        current_width = sum(img.shape[1] for img in row)
        scale_factor = target_width / current_width
        
        # Scale all images in the row proportionally
        normalized_row = []
        for img in row:
            # Calculate new dimensions while preserving aspect ratio
            new_height = int(img.shape[0] * scale_factor)
            new_width = int(img.shape[1] * scale_factor)
            
            # Resize image
            resized_img = self._resize_to_exact(
                img, 
                (new_height, new_width)
            )
            normalized_row.append(resized_img)
        
        return normalized_row

    def _stack_rows(self, rows):
        """
        Stack rows vertically to create the final collage.
        
        :param rows: List of rows, each row is a list of image tensors
        :return: Final collage tensor
        """
        # First concatenate each row horizontally
        row_tensors = []
        max_width = 0
        
        # First pass: concatenate rows and find max width
        for row in rows:
            row_tensor = torch.cat(row, dim=1)
            row_tensors.append(row_tensor)
            max_width = max(max_width, row_tensor.shape[1])
        
        # Second pass: ensure all rows have the same width
        normalized_rows = []
        for row_tensor in row_tensors:
            current_width = row_tensor.shape[1]
            if current_width != max_width:
                # Add batch dimension for interpolate
                tensor_4d = row_tensor.unsqueeze(0).permute(0, 3, 1, 2)
                # Resize to match max width
                resized = torch.nn.functional.interpolate(
                    tensor_4d,
                    size=(row_tensor.shape[0], max_width),
                    mode='bilinear',
                    align_corners=False
                )
                # Convert back to original format
                row_tensor = resized.permute(0, 2, 3, 1).squeeze(0)
            normalized_rows.append(row_tensor)
        
        # Stack rows vertically
        try:
            collage_tensor = torch.cat(normalized_rows, dim=0)
            return collage_tensor
        except Exception as e:
            # Add debug information
            widths = [row.shape[1] for row in normalized_rows]
            raise RuntimeError(f"Failed to stack rows. Row widths: {widths}") from e

    def _resize_to_exact(self, tensor, target_size):
        """
        Resize image tensor to exact size.
        
        :param tensor: Input image tensor
        :param target_size: (height, width) tuple
        :return: Resized tensor
        """
        # Efficient resizing with minimal memory overhead
        # Ensure tensor is 3D
        if len(tensor.shape) == 4:
            tensor = tensor.squeeze(0)
        
        # Add batch dimension for interpolate
        tensor_4d = tensor.unsqueeze(0).permute(0, 3, 1, 2)
        
        resized_tensor = torch.nn.functional.interpolate(
            tensor_4d,
            size=target_size,
            mode='bilinear',  # Better quality than nearest neighbor
            align_corners=False
        )
        
        # Convert back to original format
        return resized_tensor.permute(0, 2, 3, 1).squeeze(0)