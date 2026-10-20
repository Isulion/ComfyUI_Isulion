import logging
from io import BytesIO

import numpy as np
import torch
from PIL import Image

from .net_utils import safe_download, DownloadError

logger = logging.getLogger(__name__)

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
            # Hardened download: http(s) only + size cap
            content = safe_download(image_url, timeout=15)

            # Open the image using PIL
            image = Image.open(BytesIO(content))

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Convert PIL image to tensor
            image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0)

            return (image_tensor,)

        except DownloadError as e:
            logger.error("Rejected URL %r: %s", image_url, e)
            raise Exception(f"Failed to load image from URL: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading image from URL: {str(e)}")
            raise Exception(f"Failed to load image from URL: {str(e)}")
