from typing import Dict, List
from .base_handler import BaseThemeHandler
from ..configs.config_manager import ConfigManager

class NolanThemeHandler(BaseThemeHandler):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.theme_name = "nolan"

    def _get_random_choice(self, key: str) -> str:
        """Get a random choice from the config."""
        choices = self.config.get_config(key)
        return self.config.random.choice(choices) if choices else ""

    def _get_multiple_random_choices(self, key: str, count: int = 2) -> List[str]:
        """Get multiple random choices from the config."""
        choices = self.config.get_config(key)
        if not choices:
            return []
        return [self.config.random.choice(choices) for _ in range(count)]

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate a prompt based on the theme and complexity."""
        components = {}
        
        # Generate subject with cinematic enhancements
        if custom_subject:
            base_subject = custom_subject
        else:
            character = self._get_random_choice(f"{self.theme_name}.subjects")
            traits = self._get_multiple_random_choices(f"{self.theme_name}.character_traits", 2)
            base_subject = f"{character}, {', '.join(traits)}"
        
        components["subject"] = f"((dramatic shot of {base_subject})), (intense expression), (cinematic lighting)"

        # Generate environment if included
        if include_environment == "yes":
            if custom_location:
                base_environment = custom_location
            else:
                location = self._get_random_choice(f"{self.theme_name}.environments")
                atmosphere = self._get_random_choice(f"{self.theme_name}.atmospheres")
                time = self._get_random_choice(f"{self.theme_name}.times")
                base_environment = f"{location}, {atmosphere}, {time}"
            
            components["environment"] = f"((epic {base_environment})), (extreme perspective), (IMAX scale)"

        # Generate style if included
        if include_style == "yes":
            style = self._get_random_choice(f"{self.theme_name}.styles")
            cinematography = self._get_random_choice(f"{self.theme_name}.cinematography")
            components["style"] = f"((masterful {style})), ({cinematography}), (hans zimmer intensity)"

        # Generate effects if included
        if include_effects == "yes":
            main_effect = self._get_random_choice(f"{self.theme_name}.effects")
            practical_effect = self._get_random_choice(f"{self.theme_name}.practical_effects")
            components["effects"] = f"((intense {main_effect})), ({practical_effect}), (practical effects), (no cgi)"

        return components
