from typing import Dict
from .base_handler import BaseThemeHandler

class ChristmasThemeHandler(BaseThemeHandler):
    """Handler for Christmas-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Christmas-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((Christmas {custom_subject})), "
                f"((festive design)), ((holiday spirit)), "
                f"((seasonal character))"
            )
        else:
            character = self._get_random_choice("christmas.characters")
            attire = self._get_random_choice("christmas.attire")
            prop = self._get_random_choice("christmas.props")
            components["subject"] = (
                f"((Christmas {character} wearing {attire})), "
                f"((holding {prop})), ((festive character)), "
                f"((holiday spirit)), ((seasonal design))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((Christmas {custom_location})) with "
                    f"((festive setting)), ((holiday atmosphere))"
                )
            else:
                setting = self._get_random_choice("christmas.settings")
                decoration = self._get_random_choice("christmas.decorations")
                components["environment"] = (
                    f"in ((Christmas {setting})) with "
                    f"((festive {decoration})), "
                    f"((holiday atmosphere)), ((seasonal surroundings)), "
                    f"((winter wonderland))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("christmas.styles")
            aesthetic = self._get_random_choice("christmas.aesthetics")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetic)), "
                f"((festive design)), ((holiday artistry)), "
                f"((seasonal quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("christmas.effects")
            mood = self._get_random_choice("christmas.moods")
            components["effects"] = (
                f"with ((Christmas {effect} effects)), "
                f"((festive {mood} mood)), "
                f"((holiday magic)), ((seasonal glow))"
            )
        
        return components
