from typing import Dict, List
from .base_handler import BaseThemeHandler
from ..configs.config_manager import ConfigManager

class MiuraThemeHandler(BaseThemeHandler):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.theme_name = "miura"

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
        """Generate a prompt based on Kentarō Miura's distinctive style."""
        components = {}
        
        # Generate subject with Miura's characteristic style
        if custom_subject:
            base_subject = custom_subject
        else:
            character = self._get_random_choice(f"{self.theme_name}.subjects")
            traits = self._get_multiple_random_choices(f"{self.theme_name}.character_traits", 2)
            base_subject = f"{character}, {', '.join(traits)}"
        
        # Add Miura's signature detailed styling
        components["subject"] = f"((hyperdetailed {base_subject})), (intricate armor details), (dramatic pose), (gothic aesthetic), (dark fantasy style), (extreme detail in black and white)"

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
            
            components["environment"] = f"((detailed medieval fantasy environment)), {base_environment}, (intricate architectural details), (dramatic lighting)"

        # Add style elements if included
        if include_style == "yes":
            style_elements = [
                "(Kentarō Miura art style)",
                "(manga panel composition)",
                "(extreme attention to detail)",
                "(high contrast black and white)",
                "(dramatic shadows)",
                "(intricate line work)",
            ]
            components["style"] = ", ".join(style_elements)

        # Add effects if included
        if include_effects == "yes":
            effects = [
                "(gothic atmosphere)",
                "(dramatic lighting)",
                "(detailed cross-hatching)",
                "(cinematic composition)",
                "(dark fantasy mood)"
            ]
            components["effects"] = ", ".join(effects)

        return components
