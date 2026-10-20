import logging
from abc import ABC, abstractmethod
from typing import Dict, List

logger = logging.getLogger(__name__)

class BaseThemeHandler(ABC):
    """Base class for all theme handlers."""

    # Human-facing dropdown label; every concrete handler MUST override this.
    DISPLAY_NAME: str = ""

    def __init__(self, config_manager):
        """Initialize the theme handler with configuration manager."""
        self.config = config_manager
        # Shared seeded PRNG (same object as ConfigManager.random):
        # ConfigManager.set_seed() re-seeds every handler automatically.
        self.rng = config_manager.random
        self.theme_config = {}
        self.debug_mode = False  # Default to debug off

    def set_debug(self, debug: bool):
        """Enable or disable debug mode."""
        self.debug_mode = debug

    def debug_print(self, message: str):
        """Log a debug message if debug mode is enabled."""
        if self.debug_mode:
            logger.debug("%s - %s", self.__class__.__name__, message)

    def _get_random_choice(self, config_key: str) -> str:
        """Get a random choice from configuration list."""
        try:
            choices = self.config.get_config(config_key)
            if not choices:
                # Default values for different types of configurations
                defaults = {
                    "characters": "character",
                    "outfits": "outfit",
                    "poses": "pose",
                    "expressions": "expression",
                    "emotions": "emotion",
                    "locations": "location",
                    "styles": "style",
                    "effects": "effect",
                    "textures": "texture",
                    "patterns": "pattern",
                    "shapes": "shape",
                    "motions": "motion",
                    "color_schemes": "color scheme",
                    "techniques": "technique"
                }
                # Try to find a default based on the last part of the config key
                key_parts = config_key.split('.')
                last_part = key_parts[-1]
                result = defaults.get(last_part, "element")
                self.debug_print(f"Selected {config_key}: {result} (from 0 options, using default)")
                return result

            result = self.rng.choice(choices)
            self.debug_print(f"Selected {config_key}: {result} (from {len(choices)} options)")
            return result
        except Exception as e:
            self.debug_print(f"Warning: Could not get random choice for {config_key}: {str(e)}")
            return "default"

    def _get_safe_random_choice(self, config_key: str, default_value: str) -> str:
        """Get a random choice from configuration list with a default value."""
        try:
            choices = self.config.get_config(config_key)
            result = self.rng.choice(choices) if choices else default_value
            self.debug_print(f"Selected {config_key}: {result} (from {len(choices)} options)")
            return result
        except Exception as e:
            self.debug_print(f"Warning: Could not get random choice for {config_key}: {str(e)}")
            return default_value

    def _get_random_choices(self, config_key: str, count: int = 1) -> List[str]:
        """Get multiple random choices from configuration list."""
        try:
            choices = self.config.get_config(config_key)
        except Exception as e:
            self.debug_print(f"Warning: Could not get random choices for {config_key}: {str(e)}")
            return ["default"] * count

        if not choices:
            # Default values for different types of configurations
            defaults = {
                "characters": ["character"],
                "outfits": ["outfit"],
                "poses": ["pose"],
                "expressions": ["expression"],
                "emotions": ["emotion"],
                "locations": ["location"],
                "styles": ["style"],
                "effects": ["effect"],
            }
            # Try to find defaults based on the last part of the config key
            key_parts = config_key.split('.')
            if key_parts:
                for default_key in defaults:
                    if default_key in key_parts[-1]:
                        result = defaults[default_key] * count
                        self.debug_print(f"Selected {config_key}: {result} (from 0 options, using defaults)")
                        return result
            result = ["default"] * count
            self.debug_print(f"Selected {config_key}: {result} (from 0 options, using default)")
            return result

        # If we don't have enough choices, repeat them to meet the count
        if len(choices) < count:
            choices = choices * (count // len(choices) + 1)

        result = self.rng.sample(choices, count)
        self.debug_print(f"Selected {config_key}: {result} (from {len(choices)} options)")
        return result

    @abstractmethod
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate theme-specific components.

        Args:
            custom_subject (str): Custom subject override
            custom_location (str): Custom location override
            include_environment (str): Whether to include environment
            include_style (str): Whether to include style
            include_effects (str): Whether to include effects

        Returns:
            Dict[str, str]: Dictionary containing generated components
        """
        self.debug_print("Generating new prompt...")
        pass
