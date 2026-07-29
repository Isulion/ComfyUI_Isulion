import json
import os
from typing import Dict, List, Tuple, Optional
import logging

import torch

from .client import CivitaiClient, ImageDownloader, get_client, get_downloader


logger = logging.getLogger(__name__)


class IsulionCivitaiModelExplorer:
    """Node that searches and displays model information from Civitai."""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "search_query": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter search terms..."
                }),
                "sort_by": (["Highest Rated", "Most Downloaded", "Newest"], {
                    "default": "Highest Rated"
                }),
                "nsfw_filter": (["Hide NSFW", "Show All", "Only NSFW"], {
                    "default": "Hide NSFW"
                }),
                "model_type": (["Checkpoint", "LORA", "Embedding", "All"], {
                    "default": "All"
                }),
                "page": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter your Civitai API token..."
                })
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("model_info",)
    FUNCTION = "search_prompts"
    CATEGORY = "Isulion/Prompt Tools"

    def search_prompts(self,
                      search_query: str,
                      sort_by: str,
                      nsfw_filter: str,
                      model_type: str,
                      page: int = 1,
                      api_key: str = "") -> Tuple[List[str]]:
        """Search for models and return associated information."""

        logger.info("\n=== Starting Civitai API Search ===")
        logger.debug(f"Params: query={search_query}, sort={sort_by}, nsfw={nsfw_filter}, type={model_type}, page={page}")

        api_key = api_key.strip() or os.getenv('CIVITAI_API_TOKEN', '')
        
        if not api_key:
            logger.error("No API key available")
            return (["Error: No API key provided. Please provide a Civitai API token."],)

        try:
            client = get_client(api_key)
            
            sort_map = {
                "Highest Rated": "Highest Rated",
                "Most Downloaded": "Most Downloaded",
                "Newest": "Newest"
            }

            nsfw_map = {
                "Hide NSFW": "None",
                "Show All": "All",
                "Only NSFW": "NSFW"
            }

            models = client.search_models(
                query=search_query,
                sort=sort_map[sort_by],
                nsfw=nsfw_map[nsfw_filter],
                model_type=model_type if model_type != "All" else None,
                page=page,
                limit=10
            )

            if not models:
                logger.warning("API returned empty models list")
                return (["Warning: No results found for the given query."],)

            model_infos = []
            for model in models:
                versions = model.get("modelVersions", [])
                version = versions[0] if versions else {}

                model_info = (
                    f"Model: {model.get('name', 'Unknown')}\n"
                    f"Type: {model.get('type', 'Unknown')}\n"
                    f"Hash: {version.get('hash', 'Unknown')}\n"
                    f"Base Model: {version.get('baseModel', 'Unknown')}"
                )
                model_infos.append(model_info)

            logger.info(f"Found {len(model_infos)} models")
            return (model_infos,)

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.status_code} - {e.response.text[:500]}")
            return (["Error: Failed to connect to Civitai API"],)
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            return (["Error: Unexpected error occurred"],)


class IsulionCivitaiTrending:
    """Node that retrieves trending images from Civitai."""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "nsfw_filter": (["Hide NSFW", "Only NSFW"], {
                    "default": "Hide NSFW"
                }),
                "sort_by": (["Most Reactions", "Most Comments", "Newest"], {
                    "default": "Most Reactions"
                }),
                "period": (["Day", "Week", "Month", "Year", "All Time"], {
                    "default": "Day"
                }),
                "number_of_images": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter your Civitai API token..."
                }),
                "model": (["All", "SDXL", "FLUX", "Other"], {
                    "default": "FLUX"
                })
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_info",)
    FUNCTION = "get_trending"
    CATEGORY = "Isulion/Prompt Tools"

    def get_trending(self,
                    nsfw_filter: str,
                    sort_by: str,
                    period: str,
                    number_of_images: int,
                    api_key: str = "",
                    model: str = "") -> Tuple[List[str]]:
        """Retrieve trending images for the specified period."""

        logger.info("\n=== Starting Civitai Trending Images Search ===")
        logger.debug(f"Params: nsfw={nsfw_filter}, sort={sort_by}, period={period}, count={number_of_images}, model={model}")

        api_key = api_key.strip() or os.getenv('CIVITAI_API_TOKEN', '')

        if not api_key:
            return (["Error: No API key provided. Please provide a Civitai API token."],)

        try:
            client = get_client(api_key)

            nsfw_params = {
                "Hide NSFW": {
                    "nsfw": "false",
                    "nsfw_level": ["None", "Soft"]
                },
                "Only NSFW": {
                    "nsfw": "true",
                    "nsfw_level": ["Mature", "X"]
                }
            }

            period_map = {
                "Day": "Day",
                "Week": "Week",
                "Month": "Month",
                "Year": "Year",
                "All Time": "AllTime"
            }

            model_map = {
                "All": None,
                "SDXL": 1,
                "FLUX": 2,
                "Other": 3
            }

            params = {
                "limit": number_of_images,
                "period": period_map[period],
                "sort": sort_by,
                "modelId": model_map[model]
            }

            current_nsfw = nsfw_params[nsfw_filter]
            params["nsfw"] = current_nsfw["nsfw"]
            if current_nsfw["nsfw_level"]:
                params["nsfwLevel"] = ",".join(current_nsfw["nsfw_level"])

            logger.debug(f"Final API params: {params}")

            images = client.get_trending_images(**params)

            image_infos = []
            for item in images:
                if item.get('type', '').lower() == 'video':
                    continue

                stats = item.get("stats", {})
                meta = item.get("meta", {})
                
                image_info = (
                    f"Image: {item.get('name', 'Untitled')}\n"
                    f"URL: {item.get('url', 'No URL available')}\n"
                    f"Author: {item.get('username', 'Unknown')}\n"
                    f"Stats: ❤️ {stats.get('heartCount', 0)} 👍 {stats.get('likeCount', 0)} 💬 {stats.get('commentCount', 0)}\n"
                    f"Size: {item.get('width', 'Unknown')}x{item.get('height', 'Unknown')}\n"
                    f"Created: {item.get('createdAt', 'Unknown')}\n"
                    f"NSFW Level: {item.get('nsfwLevel', 'None')}\n"
                )

                if meta:
                    prompt = meta.get("prompt", "").strip()
                    negative_prompt = meta.get("negativePrompt", "").strip()
                    
                    if prompt:
                        image_info += f"\nPrompt: {prompt}\n"
                    if negative_prompt:
                        image_info += f"Negative Prompt: {negative_prompt}\n"
                    if meta.get("Model"):
                        image_info += f"Model: {meta.get('Model')}\n"
                    if meta.get("sampler"):
                        image_info += f"Sampler: {meta.get('sampler')}\n"
                    if meta.get("steps"):
                        image_info += f"Steps: {meta.get('steps')}\n"
                    if meta.get("cfg"):
                        image_info += f"CFG: {meta.get('cfg')}\n"

                image_info += "-------------------\n"
                image_infos.append(image_info)

            if not image_infos:
                return (["No images found in the current selection."],)

            return (image_infos,)

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.status_code} - {e.response.text}")
            return (["Error: Failed to connect to Civitai API"],)
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            return (["Error: Unexpected error occurred"],)


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

    def __init__(self):
        self.downloader = get_downloader()

    def create_error_tensor(self, target_size: int, message: str = "No valid images found") -> torch.Tensor:
        """Create a black tensor with error indication."""
        error_image = Image.new('RGB', (target_size, target_size), (0, 0, 0))
        tensor = torch.from_numpy(np.array(error_image)).float() / 255.0
        return tensor.unsqueeze(0)

    def display_image(self, image_info: str, mode: str, image_index: int, target_size: int):
        try:
            # Parse image info to get URLs
            if isinstance(image_info, list):
                entries = image_info
            else:
                entries = image_info.split("-------------------")
                entries = [entry.strip() for entry in entries if entry.strip()]

            if not entries:
                return (self.create_error_tensor(target_size), 
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

                urls = []
                for entry in entries:
                    image_data = {}
                    for line in entry.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            image_data[key] = value
                    
                    image_url = image_data.get('URL', '')
                    model = image_data.get('Model', 'Unknown')
                    if image_url:
                        urls.append((image_url, image_data, model))

                if not urls:
                    return (self.create_error_tensor(target_size), 
                           "No valid images found", 
                           "No prompt available", 
                           "", 
                           "No model available")

                # Download in parallel
                results = self.downloader.download_batch(
                    [u[0] for u in urls], 
                    target_size=target_size,
                    max_workers=4
                )

                for (tensor, meta), (url, image_data, model) in zip(results, urls):
                    if tensor is not None:
                        all_tensors.append(tensor)
                        all_titles.append(image_data.get('Image', 'Untitled'))
                        all_prompts.append(image_data.get('Prompt', 'No prompt available'))
                        all_urls.append(url)
                        all_models.append(model)

                if not all_tensors:
                    return (self.create_error_tensor(target_size), 
                           "No valid images found", 
                           "No prompt available", 
                           "", 
                           "No model available")

                final_tensor = torch.cat(all_tensors, dim=0)
                
                # Free VRAM cache after batch processing
                try:
                    import comfy.model_management as model_management
                    model_management.soft_empty_cache()
                except ImportError:
                    pass

                return (final_tensor, 
                       " | ".join(all_titles), 
                       " | ".join(all_prompts), 
                       " | ".join(all_urls),
                       " | ".join(all_models))

            else:  # Single mode
                if image_index >= len(entries):
                    return (self.create_error_tensor(target_size),
                           f"Image index {image_index} out of range (total: {len(entries)})",
                           "No prompt available",
                           "",
                           "No model available")

                # Try each entry starting from image_index
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
                        tensor = self.downloader.download_and_convert(image_url, target_size)
                        return (tensor, title, prompt, image_url, model)
                    except Exception as e:
                        logger.warning(f"Failed to load image {current_index}: {e}")
                        continue

                # No valid images found
                return (self.create_error_tensor(target_size),
                       "No valid images found",
                       "No prompt available",
                       "",
                       "No model available")
             
        except Exception as e:
            logger.error(f"Error in display_image: {e}")
            return (self.create_error_tensor(target_size),
                   f"Error: {str(e)}",
                   "No prompt available",
                   "",
                   "No model available")


# Register the nodes with ComfyUI
NODE_CLASS_MAPPINGS = {
    "Isulion Civitai Model Explorer": IsulionCivitaiModelExplorer,
    "Isulion Civitai Trending": IsulionCivitaiTrending,
    "Isulion Civitai Image Display": IsulionCivitaiImageDisplay
}