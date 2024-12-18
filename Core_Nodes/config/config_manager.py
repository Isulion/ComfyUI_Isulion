import os
import random
from typing import Any, Dict, List, Optional

class ConfigManager:
    """Manages configuration loading and access for theme handlers."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the configuration manager.
        
        Args:
            seed (Optional[int]): Random seed for consistent generation
        """
        self.configs: Dict[str, Any] = {}
        self.random = random.Random(seed) if seed is not None else random.Random()
        self._load_configs()
    
    def _load_configs(self):
        for filename in self.config_files:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    logger.debug(f"Loading config file: {filename}")
                    contents = f.read().strip() # Read the entire file content and remove leading/trailing whitespace
                    if not contents:
                        logger.warning(f"Config file '{filename}' is empty!")
                        continue # Skip if the file is empty
                    configs = json.loads(contents) # Use json.loads for debugging purposes to see the string
                    logger.debug(f"Loaded config: {configs}")
                    self.configs.update(configs)
            except json.JSONDecodeError as e:
                logger.exception(f"JSON decoding error in {filename}: {e}")
                # Consider more robust error handling (e.g., using a default config)
            except FileNotFoundError:
                logger.warning(f"Configuration file not found: {filename}")
            except Exception as e:
                logger.exception(f"Unexpected error loading {filename}: {e}")
        
        # Load text-based config files
        config_files = {
            'mega': 'config_mega.txt',
            'enhancements': 'enhancements.txt',
            'lightings': 'lightings.txt',
            'styles': 'styles.txt',
            'subjects': 'subjects.txt',
            'color_palettes': 'color_palettes.txt'
        }
        
        for config_key, filename in config_files.items():
            file_path = os.path.join(current_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.configs[config_key] = [line.strip() for line in f if line.strip()]
    
    def get_config(self, key: str) -> Any:
        """Get configuration value by key.
        
        Args:
            key (str): Configuration key (e.g., 'anime.characters')
            
        Returns:
            Any: Configuration value
            
        Raises:
            KeyError: If the configuration key is not found
        """
        try:
            # Handle nested keys (e.g., 'anime.characters')
            keys = key.split('.')
            value = self.configs
            
            # Special handling for common configurations
            if keys[0] == "common":
                common_defaults = {
                    "times": [
                        "sunrise", "noon", "sunset", "night", "golden hour",
                        "dawn", "dusk", "midnight", "afternoon", "morning"
                    ],
                    "weather": [
                        "clear sky", "light rain", "cloudy", "starry night", "misty",
                        "sunny", "stormy", "foggy", "snowy", "windy"
                    ]
                }
                if len(keys) > 1 and keys[1] in common_defaults:
                    return common_defaults[keys[1]]
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    raise KeyError(f"Configuration key not found: {key}")
            return value
        except Exception as e:
            print(f"Error accessing configuration {key}: {str(e)}")
            raise  # Re-raise the exception to be handled by the caller
    
    def set_seed(self, seed: int):
        """Set random seed for consistent generation.
        
        Args:
            seed (int): Random seed
        """
        self.random.seed(seed) 