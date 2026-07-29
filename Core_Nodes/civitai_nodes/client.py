"""
Civitai API Client - Shared client for Civitai nodes.
Provides CivitaiClient for API calls and ImageDownloader for parallel image downloads.
"""
import os
import requests
import logging
from typing import Dict, List, Tuple, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO
import numpy as np
import torch

logger = logging.getLogger(__name__)


# Global client instances (singleton pattern for connection pooling)
_CLIENT_INSTANCE: Optional["CivitaiClient"] = None
_DOWNLOADER_INSTANCE: Optional["ImageDownloader"] = None


class CivitaiClient:
    """Client for Civitai REST API v1."""
    
    def __init__(self, api_key: str = "", base_url: str = "https://civitai.com/api/v1"):
        self.api_key = api_key or os.getenv("CIVITAI_API_TOKEN", "")
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "ComfyUI-Isulion/1.0"
        })
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def _get(self, endpoint: str, params: Dict) -> Dict[str, Any]:
        """Make GET request to API."""
        url = f"{self.base_url}{endpoint}"
        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    
    def search_models(self, query: str = "", sort: str = "Highest Rated",
                      nsfw: str = "None", model_type: Optional[str] = None,
                      page: int = 1, limit: int = 10) -> List[Dict]:
        """Search for models."""
        params = {
            "query": query,
            "limit": limit,
            "page": page,
            "sort": sort,
            "nsfw": nsfw,
        }
        if model_type:
            params["type"] = model_type.upper()
        
        data = self._get("/models", params)
        return data.get("items", [])
    
    def get_trending_images(self, limit: int = 10, period: str = "Day",
                            sort: str = "Most Reactions", nsfw: str = "false",
                            nsfw_level: Optional[str] = None, model_id: Optional[int] = None) -> List[Dict]:
        """Get trending images."""
        params = {
            "limit": limit,
            "period": period,
            "sort": sort,
            "nsfw": nsfw,
        }
        if nsfw_level:
            params["nsfwLevel"] = nsfw_level
        if model_id:
            params["modelId"] = model_id
        
        data = self._get("/images", params)
        return data.get("items", [])


class ImageDownloader:
    """Parallel image downloader with tensor conversion."""
    
    def __init__(self, max_workers: int = 4, timeout: int = 10):
        self.max_workers = max_workers
        self.timeout = timeout
    
    def download_and_convert(self, url: str, target_size: int = 512) -> torch.Tensor:
        """Download single image and convert to tensor."""
        resp = requests.get(url, timeout=self.timeout, stream=True)
        resp.raise_for_status()
        
        # Validate content type
        content_type = resp.headers.get('content-type', '').lower()
        if not content_type.startswith('image/') or 'video' in content_type:
            raise ValueError(f"Invalid content type: {content_type}")
        
        image_data = resp.content
        if not image_data:
            raise ValueError("Empty response")
        
        image = Image.open(BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize with padding to target_size
        image = self._resize_with_padding(image, target_size)
        
        tensor = torch.from_numpy(np.array(image)).float() / 255.0
        return tensor.unsqueeze(0)
    
    def _resize_with_padding(self, image: Image.Image, target_size: int) -> Image.Image:
        """Resize image to target_size with padding to maintain aspect ratio."""
        new_image = Image.new('RGB', (target_size, target_size), (0, 0, 0))
        
        aspect = image.width / image.height
        if aspect > 1:
            new_width = target_size
            new_height = int(target_size / aspect)
        else:
            new_height = target_size
            new_width = int(target_size * aspect)
        
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        paste_x = (target_size - new_width) // 2
        paste_y = (target_size - new_height) // 2
        new_image.paste(resized, (paste_x, paste_y))
        
        return new_image
    
    def download_batch(self, urls: List[str], target_size: int = 512,
                       max_workers: Optional[int] = None) -> List[Tuple[Optional[torch.Tensor], Dict]]:
        """
        Download multiple images in parallel.
        
        Returns:
            List of (tensor_or_None, metadata_dict) tuples.
        """
        workers = max_workers or self.max_workers
        results = [None] * len(urls)
        
        def download_one(idx: int, url: str) -> Tuple[int, Optional[torch.Tensor], Dict]:
            meta = {"url": url}
            try:
                tensor = self.download_and_convert(url, target_size)
                return idx, tensor, meta
            except Exception as e:
                logger.warning(f"Failed to download {url}: {e}")
                return idx, None, meta
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(download_one, i, url) for i, url in enumerate(urls)]
            for future in as_completed(futures):
                idx, tensor, meta = future.result()
                results[idx] = (tensor, meta)
        
        return results


def get_client(api_key: str = "") -> CivitaiClient:
    """Get or create shared CivitaiClient instance."""
    global _CLIENT_INSTANCE
    if _CLIENT_INSTANCE is None or (_CLIENT_INSTANCE.api_key != (api_key or os.getenv("CIVITAI_API_TOKEN", ""))):
        _CLIENT_INSTANCE = CivitaiClient(api_key)
    return _CLIENT_INSTANCE


def get_downloader(max_workers: int = 4) -> ImageDownloader:
    """Get or create shared ImageDownloader instance."""
    global _DOWNLOADER_INSTANCE
    if _DOWNLOADER_INSTANCE is None:
        _DOWNLOADER_INSTANCE = ImageDownloader(max_workers=max_workers)
    return _DOWNLOADER_INSTANCE


def clear_clients() -> None:
    """Clear global client instances (for testing or reconfiguration)."""
    global _CLIENT_INSTANCE, _DOWNLOADER_INSTANCE
    _CLIENT_INSTANCE = None
    _DOWNLOADER_INSTANCE = None