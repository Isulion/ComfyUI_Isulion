from typing import Dict
from .base_handler import BaseThemeHandler

class PeakyBlindersThemeHandler(BaseThemeHandler):
    """Handler for Peaky Blinders style-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Peaky Blinders style-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((1920s {custom_subject})), "
                f"((peaky blinders style)), ((gangster era)), "
                f"((british criminal))"
            )
        else:
            character = self._get_random_choice("peaky_blinders.characters")
            clothing = self._get_random_choice("peaky_blinders.clothing")
            prop = self._get_random_choice("peaky_blinders.props")
            components["subject"] = (
                f"((1920s {character})), "
                f"((wearing {clothing})), ((with {prop})), "
                f"((peaky blinders style)), ((gangster era))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((1920s {custom_location})) with "
                    f"((industrial setting)), ((period environment))"
                )
            else:
                setting = self._get_random_choice("peaky_blinders.settings")
                atmosphere = self._get_random_choice("peaky_blinders.atmospheres")
                lighting = self._get_random_choice("peaky_blinders.lighting")
                components["environment"] = (
                    f"in (({setting})) with (({lighting} lighting)), "
                    f"((creating {atmosphere} atmosphere)), "
                    f"((1920s scene)), ((industrial vista))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("peaky_blinders.styles")
            components["style"] = (
                f"((styled as {style})), "
                f"((peaky blinders aesthetic)), "
                f"((1920s design)), ((gangster look)), "
                f"((period authenticity))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("peaky_blinders.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((period atmosphere)), "
                f"((industrial ambiance)), ((1920s environment))"
            )
        
        return components
