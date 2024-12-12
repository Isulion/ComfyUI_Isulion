from typing import Dict, List
from .base_handler import BaseThemeHandler
from ..configs.config_manager import ConfigManager

class MiuraThemeHandler(BaseThemeHandler):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.theme_name = "miura"
        self.debug = False

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

    def _debug_print(self, message: str) -> None:
        """Print debug message only if debug mode is enabled."""
        if hasattr(self, 'debug') and self.debug:
            print(f"MiuraThemeHandler: {message}")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate a prompt based on Kentarō Miura's distinctive style."""
        components = {}
        
        # Generate subject with Miura's characteristic style
        if custom_subject:
            base_subject = custom_subject
            self._debug_print(f"Using custom subject: {base_subject}")
        else:
            character = self._get_random_choice(f"{self.theme_name}.subjects")
            traits = self._get_multiple_random_choices(f"{self.theme_name}.character_traits", 2)
            details = self._get_multiple_random_choices(f"{self.theme_name}.detail_elements", 2)
            base_subject = f"{character}, {', '.join(traits)}, {', '.join(details)}"
            self._debug_print(f"Generated subject: {base_subject}")

        # Add Miura's signature detailed styling
        components["subject"] = f"((masterfully detailed {base_subject})), (intricate pen work:1.3), (meticulous cross-hatching:1.2), (high detail illustration), (dramatic chiaroscuro), (extreme attention to texture:1.2), (masterful line weight variation)"
        self._debug_print(f"Subject generated: {components['subject']}")

        # Generate environment if included
        if include_environment == "yes":
            if custom_location:
                atmosphere = self._get_random_choice(f"{self.theme_name}.atmospheres")
                time = self._get_random_choice(f"{self.theme_name}.times")
                details = self._get_random_choice(f"{self.theme_name}.environment_details")
                base_environment = f"{custom_location}, {atmosphere}, {time}, {details}"
                self._debug_print(f"Using custom location: {custom_location}")
            else:
                location = self._get_random_choice(f"{self.theme_name}.locations")
                atmosphere = self._get_random_choice(f"{self.theme_name}.atmospheres")
                time = self._get_random_choice(f"{self.theme_name}.times")
                details = self._get_random_choice(f"{self.theme_name}.environment_details")
                base_environment = f"{location}, {atmosphere}, {time}, {details}"
                self._debug_print(f"Generated environment: {base_environment}")

            components["environment"] = f"((hyper-detailed environment)), {base_environment}, (intricate architectural details:1.2), (dramatic perspective), (meticulous background detail:1.3)"
            self._debug_print(f"Environment generated: {components['environment']}")

        # Add style elements if included
        if include_style == "yes":
            style_elements = [
                "(Kentarō Miura art style:1.3)",
                "(masterful pen and ink technique:1.2)",
                "(extreme attention to detail:1.4)",
                "(high contrast black and white:1.2)",
                "(intricate cross-hatching patterns:1.3)",
                "(meticulous line work:1.2)",
                "(dramatic shadow placement)",
                "(textural complexity:1.2)"
            ]
            components["style"] = ", ".join(style_elements)
            self._debug_print(f"Style elements added: {', '.join(style_elements)}")
            self._debug_print(f"Style generated: {components['style']}")

        # Add effects if included
        if include_effects == "yes":
            effects = [
                "(masterful light and shadow interplay:1.3)",
                "(intricate texture layering:1.2)",
                "(detailed surface rendering)",
                "(atmospheric depth:1.2)",
                "(precise line weight variation)",
                "(micro details in shadows:1.2)",
                "(complex material textures)"
            ]
            components["effects"] = ", ".join(effects)
            self._debug_print(f"Effects added: {', '.join(effects)}")
            self._debug_print(f"Effects generated: {components['effects']}")

        return components
