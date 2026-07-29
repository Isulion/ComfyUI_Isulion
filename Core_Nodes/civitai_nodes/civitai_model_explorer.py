import json
import os
from typing import Dict, List, Tuple, Optional
import requests
import traceback
import logging

logger = logging.getLogger(__name__)

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

        logger.info("\n=== Starting Civitai API Search ===")
        logger.debug(f"Debug - Search params:")
        logger.debug(f"  Query: {search_query}")
        logger.debug(f"  Sort: {sort_by}")
        logger.debug(f"  NSFW Filter: {nsfw_filter}")
        logger.debug(f"  Model Type: {model_type}")
        logger.debug(f"  Page: {page}")
        logger.debug(f"  API Key provided: {'Yes' if api_key else 'No'}")

        api_key = api_key.strip() or self.api_key
        logger.debug(f"Debug - Final API key present: {'Yes' if api_key else 'No'}")

        if not api_key:
            logger.error("Debug - Error: No API key available")
            return (
                ["Error: No API key provided. Please provide a Civitai API token."],
            )

        logger.debug(f"Debug - Final page number: {page}")

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
        logger.debug(f"Debug - Final API parameters: {json.dumps(params, indent=2)}")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        logger.debug("Debug - Headers set (excluding auth token)")

        try:
            cache_key = f"{search_query}_{sort_by}_{nsfw_filter}_{model_type}_{page}"
            logger.debug(f"Debug - Cache key: {cache_key}")

            if cache_key in self.results_cache:
                logger.debug("Debug - Returning cached results")
                return self.results_cache[cache_key]

            logger.debug(f"Debug - Making API request to: {self.api_base}/models")
            response = requests.get(
                f"{self.api_base}/models",
                params=params,
                headers=headers,
                timeout=10
            )

            logger.debug(f"Debug - API Response Status: {response.status_code}")
            logger.debug(f"Debug - API Response Headers: {dict(response.headers)}")
            logger.debug(f"Debug - API Response Content: {response.text[:500]}...")

            response.raise_for_status()
            data = response.json()
            logger.debug(f"Debug - Successfully parsed JSON response")
            logger.debug(f"API Response Body: {data}")


            model_infos = []

            items = data.get("items", [])

            if not items:
                logger.warning("Debug - API returned empty items list.")
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
            logger.error(f"Debug - Request Exception Details:")
            logger.error(f"  Error Type: {type(e).__name__}")
            logger.error(f"  Error Message: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"  Response Status: {e.response.status_code}")
                logger.error(f"  Response Headers: {dict(e.response.headers)}")
                logger.error(f"  Response Content: {e.response.text[:500]}...")
            logger.error("Debug - Full traceback:")
            traceback.print_exc()
            return ["Error: Failed to connect to Civitai API"]
        except Exception as e:
            logger.error(f"Debug - Unexpected Error Details:")
            logger.error(f"  Error Type: {type(e).__name__}")
            logger.error(f"  Error Message: {str(e)}")
            logger.error("Debug - Full traceback:")
            traceback.print_exc()
            return ["Error: Unexpected error occurred"]
