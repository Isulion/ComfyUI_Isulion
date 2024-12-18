import os
import random
import json
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
        """Load all configuration files from the config directory."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load each JSON config file in the configs directory
        for filename in os.listdir(current_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(current_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Merge the config into the main configs dictionary
                    self.configs.update(json.load(f))
        
        # Add default configuration for SpectralMist if not present
        if "SpectralMist" not in self.configs:
            self.configs["SpectralMist"] = {
                "default_color": "azure",
                "available_colors": ["azure", "violet", "emerald", "ruby", "gold", "sapphire", "amber", "jade"]
            }
    
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
