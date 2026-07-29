import json
import os
from typing import Dict, List, Tuple, Optional
import requests
import traceback
import logging

#Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
                    "max": 100,  # Increased max to allow for more retries
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

        logging.info("\n=== Starting Civitai Trending Images Search ===")
        logging.debug(f"Debug - Search params:")
        logging.debug(f"  NSFW Filter: {nsfw_filter}")

        api_key = api_key.strip() or self.api_key

        if not api_key:
            return (["Error: No API key provided. Please provide a Civitai API token."],)

        nsfw_params = {
            "Hide NSFW": {"nsfw": "false", "nsfwLevel": ["None", "Soft"]},
            "Only NSFW": {"nsfw": "true", "nsfwLevel": ["Mature", "X"]}
        }

        period_map = {
            "Day": "Day", "Week": "Week", "Month": "Month", "Year": "Year", "All Time": "AllTime"
        }

        model_map = {
            "All": None, "SDXL": 1, "FLUXX": 2, "Other": 3  # Replace with actual IDs if needed
        }

        params = {
            "limit": 50,  # Fetch more results per page for more retries. Adjust as needed.
            "period": period_map[period],
            "sort": sort_by,
            "modelId": model_map[model]
        }

        current_nsfw_params = nsfw_params[nsfw_filter]
        params["nsfw"] = current_nsfw_params["nsfw"]
        if current_nsfw_params["nsfwLevel"]:
            params["nsfwLevel"] = ",".join(current_nsfw_params["nsfwLevel"])

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        try:
            image_infos = []
            page = 1
            while len(image_infos) < number_of_images:
                params["page"] = page
                response = requests.get(f"{self.api_base}/images", params=params, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])

                for item in items:
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
                    if len(image_infos) >= number_of_images:
                        break
                page += 1

            if not image_infos:
                return (["No images found in the current selection."],)
            result = (image_infos,)
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
