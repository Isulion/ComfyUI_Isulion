import torch
import requests
from PIL import Image
from io import BytesIO
import numpy as np

class DisplayImageFromURL:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "display_image"
    CATEGORY = "image"

    def display_image(self, image_url):
        try:
            # Download the image from URL
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Open the image using PIL
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL image to tensor
            image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0)
            
            return (image_tensor,)
            
        except Exception as e:
            print(f"Error loading image from URL: {str(e)}")
            raise Exception(f"Failed to load image from URL: {str(e)}") 