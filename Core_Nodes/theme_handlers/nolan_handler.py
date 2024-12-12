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
        
        # Generate subject with cinematic enhancements and varied camera angles
        if custom_subject:
            base_subject = custom_subject
        else:
            character = self._get_random_choice(f"{self.theme_name}.subjects")
            traits = self._get_multiple_random_choices(f"{self.theme_name}.character_traits", 2)
            base_subject = f"{character}, {', '.join(traits)}"
        
        camera_angles = ["dramatic front shot of", "epic side profile of", "dynamic 3/4 view of", 
                        "intense close-up of", "heroic low angle shot of", "dramatic overhead shot of"]
        chosen_angle = self.config.random.choice(camera_angles)
        components["subject"] = f"(({chosen_angle} {base_subject})), (intense expression), (cinematic lighting), (dramatic composition)"

        # Generate environment if included
        if include_environment == "yes":
            if custom_location:
                atmosphere = self._get_random_choice(f"{self.theme_name}.atmospheres")
                time = self._get_random_choice(f"{self.theme_name}.times")
                base_environment = f"{custom_location}, {atmosphere}, {time}"
            else:
                location = self._get_random_choice(f"{self.theme_name}.environments")
                atmosphere = self._get_random_choice(f"{self.theme_name}.atmospheres")
                time = self._get_random_choice(f"{self.theme_name}.times")
                base_environment = f"{location}, {atmosphere}, {time}"
            
            components["environment"] = f"((epic {base_environment})), (extreme perspective), (IMAX scale), (dynamic camera movement)"

        # Generate style if included
        if include_style == "yes":
            style = self._get_random_choice(f"{self.theme_name}.styles")
            cinematography = self._get_random_choice(f"{self.theme_name}.cinematography")
            components["style"] = f"((masterful {style})), ({cinematography}), (hans zimmer intensity), (high contrast), (adrenaline-pumping action)"

        # Generate effects if included with enhanced explosions
        if include_effects == "yes":
            explosion_effects = ["massive explosions", "fiery explosions", "spectacular pyrotechnics", 
                               "chain reaction explosions", "explosive shockwaves", "debris flying everywhere"]
            main_effect = self._get_random_choice(f"{self.theme_name}.effects")
            practical_effect = self._get_random_choice(f"{self.theme_name}.practical_effects")
            chosen_explosion = self.config.random.choice(explosion_effects)
            components["effects"] = f"((intense {main_effect})), ({practical_effect}), ((({chosen_explosion}))), (practical effects), (no cgi), (michael bay level explosions)"

        return components
