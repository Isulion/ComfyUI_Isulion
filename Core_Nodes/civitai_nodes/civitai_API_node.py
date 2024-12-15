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


class IsulionCivitaiModelExplorer:
    """Node that searches and displays model information and previews from Civitai."""

    def __init__(self):
        self.api_base = "https://civitai.com/api/v1"
        self.results_cache = {}
        self.current_page = 1
        self.items_per_page = 10
        self.api_key = os.getenv('CIVITAI_API_TOKEN')
        print(f"Debug - Init: API base URL: {self.api_base}")

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

        logging.info("\n=== Starting Civitai API Search ===")
        logging.debug(f"Debug - Search params:")
        logging.debug(f"  Query: {search_query}")
        logging.debug(f"  Sort: {sort_by}")
        logging.debug(f"  NSFW Filter: {nsfw_filter}")
        logging.debug(f"  Model Type: {model_type}")
        logging.debug(f"  Page: {page}")
        logging.debug(f"  API Key provided: {'Yes' if api_key else 'No'}")

        api_key = api_key.strip() or self.api_key
        logging.debug(f"Debug - Final API key present: {'Yes' if api_key else 'No'}")

        if not api_key:
            logging.error("Debug - Error: No API key available")
            return (
                ["Error: No API key provided. Please provide a Civitai API token."],
            )

        logging.debug(f"Debug - Final page number: {page}")

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

        params = {
            "query": search_query,
            "limit": self.items_per_page,
            "page": page,
            "sort": sort_map[sort_by],
            "nsfw": nsfw_map[nsfw_filter],
            "type": model_type.upper() if model_type != "All" else None
        }

        params = {k: v for k, v in params.items() if v is not None}
        logging.debug(f"Debug - Final API parameters: {json.dumps(params, indent=2)}")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        logging.debug("Debug - Headers set (excluding auth token)")

        try:
            cache_key = f"{search_query}_{sort_by}_{nsfw_filter}_{model_type}_{page}"
            logging.debug(f"Debug - Cache key: {cache_key}")

            if cache_key in self.results_cache:
                logging.debug("Debug - Returning cached results")
                return self.results_cache[cache_key]

            logging.debug(f"Debug - Making API request to: {self.api_base}/models")
            response = requests.get(
                f"{self.api_base}/models",
                params=params,
                headers=headers,
                timeout=10
            )

            logging.debug(f"Debug - API Response Status: {response.status_code}")
            logging.debug(f"Debug - API Response Headers: {dict(response.headers)}")
            logging.debug(f"Debug - API Response Content: {response.text[:500]}...")

            response.raise_for_status()
            data = response.json()
            logging.debug(f"Debug - Successfully parsed JSON response")
            logging.debug(f"API Response Body: {data}")


            model_infos = []

            items = data.get("items", [])

            if not items:
                logging.warning("Debug - API returned empty items list.")
                return ["Warning: No results found for the given query."]

            for item in items:
                versions = item.get("modelVersions", [])
                version = versions[0] if versions else {}

                model_info = (
                    f"Model: {item.get('name', 'Unknown')}\n"
                    f"Type: {item.get('type', 'Unknown')}\n"
                    f"Hash: {version.get('hash', 'Unknown')}\n"
                    f"Base Model: {version.get('baseModel', 'Unknown')}"
                )

                model_infos.append(model_info)
            result = (model_infos,)
            self.results_cache[cache_key] = result
            return result

        except requests.RequestException as e:
            logging.error(f"Debug - Request Exception Details:")
            logging.error(f"  Error Type: {type(e).__name__}")
            logging.error(f"  Error Message: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"  Response Status: {e.response.status_code}")
                logging.error(f"  Response Headers: {dict(e.response.headers)}")
                logging.error(f"  Response Content: {e.response.text[:500]}...")
            logging.error("Debug - Full traceback:")
            traceback.print_exc()
            return ["Error: Failed to connect to Civitai API"]
        except Exception as e:
            logging.error(f"Debug - Unexpected Error Details:")
            logging.error(f"  Error Type: {type(e).__name__}")
            logging.error(f"  Error Message: {str(e)}")
            logging.error("Debug - Full traceback:")
            traceback.print_exc()
            return ["Error: Unexpected error occurred"]


class IsulionCivitaiTrending:
    """Node that retrieves trending images from Civitai."""

    def __init__(self):
        self.api_base = "https://civitai.com/api/v1"
        self.results_cache = {}
        self.api_key = os.getenv('CIVITAI_API_TOKEN')

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
                    api_key: str = "") -> Tuple[List[str]]:
        """Retrieve trending images for the specified period."""

        logging.info("\n=== Starting Civitai Trending Images Search ===")
        logging.debug(f"Debug - Search params:")
        logging.debug(f"  NSFW Filter: {nsfw_filter}")

        api_key = api_key.strip() or self.api_key

        if not api_key:
            return (["Error: No API key provided. Please provide a Civitai API token."],)

        # Updated NSFW mapping with correct API parameters
        nsfw_params = {
            "Hide NSFW": {
                "nsfw": "false",
                "nsfwLevel": ["None", "Soft"]  # Only show Safe and Soft content
            },
            "Only NSFW": {
                "nsfw": "true",
                "nsfwLevel": ["Mature", "X"]  # Only show Mature and X content
            }
        }

        period_map = {
            "Day": "Day",
            "Week": "Week",
            "Month": "Month",
            "Year": "Year",
            "All Time": "AllTime"
        }

        # Base parameters
        params = {
            "limit": number_of_images,
            "period": period_map[period],
            "sort": sort_by,
        }

        # Add NSFW parameters
        current_nsfw_params = nsfw_params[nsfw_filter]
        params["nsfw"] = current_nsfw_params["nsfw"]
        
        # Handle nsfwLevel as a comma-separated string
        if current_nsfw_params["nsfwLevel"]:
            params["nsfwLevel"] = ",".join(current_nsfw_params["nsfwLevel"])

        logging.debug(f"Debug - Final API parameters: {params}")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        try:
            cache_key = f"trending_{nsfw_filter}_{sort_by}_{period}_{number_of_images}"
            if cache_key in self.results_cache:
                logging.debug("Debug - Returning cached results")
                return self.results_cache[cache_key]

            logging.debug(f"Debug - Making API request to: {self.api_base}/images")
            response = requests.get(
                f"{self.api_base}/images",
                params=params,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()
            logging.debug(f"Debug - Successfully parsed JSON response")

            image_infos = []
            items = data.get("items", [])

            if not items:
                logging.warning("Debug - API returned empty items list.")
                return (["Warning: No trending images found."],)

            for item in items:
                # Silently skip videos
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

            result = (image_infos,)
            self.results_cache[cache_key] = result
            return result

        except requests.RequestException as e:
            logging.error(f"Debug - Request Exception: {str(e)}")
            if hasattr(e, 'response'):
                logging.error(f"Response Status: {e.response.status_code}")
                logging.error(f"Response Text: {e.response.text}")
            return (["Error: Failed to connect to Civitai API"],)
        except Exception as e:
            logging.error(f"Debug - Unexpected Error: {str(e)}")
            traceback.print_exc()
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

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "title", "prompt", "image_url")
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
                       "")

            # Handle "All" mode
            if mode == "All":
                all_tensors = []
                all_titles = []
                all_prompts = []
                all_urls = []

                for entry in entries:
                    image_data = {}
                    for line in entry.split('\n'):
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            image_data[key] = value

                    image_url = image_data.get('URL', '')
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

                    except:
                        # Silently skip any errors
                        continue

                if not all_tensors:
                    return (self.create_error_image(target_size), 
                           "No valid images found", 
                           "No prompt available", 
                           "")

                final_tensor = torch.cat(all_tensors, dim=0)
 
                return (final_tensor, 
                       " | ".join(all_titles), 
                       " | ".join(all_prompts), 
                       " | ".join(all_urls))

            else:  # Single mode
                if image_index >= len(entries):
                    return (self.create_error_image(target_size),
                           f"Image index {image_index} out of range (total: {len(entries)})",
                           "No prompt available",
                           "")

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
                        
                        return (image_tensor, title, prompt, image_url)
                    
                    except:
                        # Silently skip any errors and continue to next entry
                        continue

                # If we get here, no valid images were found
                return (self.create_error_image(target_size),
                       "No valid images found",
                       "No prompt available",
                       "")
            
        except Exception as e:
            print(f"Error loading image from URL: {str(e)}")
            return (self.create_error_image(target_size),
                   f"Error: {str(e)}",
                   "No prompt available",
                   "")


# Register the nodes with ComfyUI
NODE_CLASS_MAPPINGS = {
    "Isulion Civitai Model Explorer": IsulionCivitaiModelExplorer,
    "Isulion Civitai Trending": IsulionCivitaiTrending,
    "Isulion Civitai Image Display": IsulionCivitaiImageDisplay
}