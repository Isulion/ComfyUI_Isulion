import torch
import requests
from PIL import Image
from io import BytesIO
import numpy as np
from urllib.parse import urlparse

# Security configuration
ALLOWED_DOMAINS = {
    "civitai.com",
    "image.civitai.com",  # Civitai image CDN subdomain
    "images.unsplash.com",
    "localhost",
    "127.0.0.1",
}
MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB
REQUEST_TIMEOUT = 10  # seconds


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

    def _validate_url(self, url: str) -> None:
        """Validate URL against security policy."""
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise ValueError(f"Only HTTPS URLs are allowed, got: {parsed.scheme}")
        if parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Domain not allowed: {parsed.netloc}. Allowed: {', '.join(sorted(ALLOWED_DOMAINS))}")

    def _download_image(self, url: str) -> bytes:
        """Download image with timeout and size limit."""
        with requests.get(url, stream=True, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            
            # Check content length if available
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_IMAGE_SIZE:
                raise ValueError(f"Image too large: {content_length} bytes (max {MAX_IMAGE_SIZE})")
            
            # Stream download with size limit
            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > MAX_IMAGE_SIZE:
                    raise ValueError(f"Image exceeds maximum size of {MAX_IMAGE_SIZE} bytes")
            return content

    def display_image(self, image_url):
        try:
            # Validate URL
            self._validate_url(image_url)
            
            # Download with security limits
            image_data = self._download_image(image_url)
            
            # Open and validate image
            image = Image.open(BytesIO(image_data))
            image.load()  # Force load to detect corruption
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert PIL image to tensor (BHWC format for ComfyUI)
            image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0)
            
            return (image_tensor,)
            
        except requests.Timeout:
            raise Exception(f"Request timeout after {REQUEST_TIMEOUT} seconds")
        except requests.RequestException as e:
            raise Exception(f"Failed to download image: {str(e)}")
        except ValueError as e:
            raise Exception(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to load image from URL: {str(e)}") 