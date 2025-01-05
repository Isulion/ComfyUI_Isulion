from typing import Dict
from .base_handler import BaseThemeHandler

class MedievalThemeHandler(BaseThemeHandler):
    """Handler for medieval-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        components = {}
        
        # Subject generation
        if custom_subject:
            components["subject"] = (
                f"((medieval {custom_subject})), "
                f"((authentic historical appearance)), ((period-accurate details)), "
                f"((medieval craftsmanship)), ((historical authenticity))"
            )
        else:
            character = self._get_random_choice("medieval.characters")
            attire = self._get_random_choice("medieval.attire")
            components["subject"] = (
                f"((medieval {character})), wearing ((authentic {attire})), "
                f"((period-accurate details)), ((medieval craftsmanship))"
            )
            
        # Environment
        if include_environment == "yes":
            setting = self._get_random_choice("medieval.settings")
            time_period = self._get_random_choice("medieval.time_periods")
            components["environment"] = (
                f"in ((authentic medieval {setting})), "
                f"during ((the {time_period})), "
                f"((historical accuracy)), ((period-appropriate surroundings))"
            )
            
        # Style
        if include_style == "yes":
            style = self._get_random_choice("medieval.artistic_styles")
            technique = self._get_random_choice("medieval.techniques")
            components["style"] = (
                f"((rendered in {style})), ((using {technique})), "
                f"((medieval art style)), ((historical painting)), "
                f"((masterwork quality)), ((8k resolution))"
            )
            
        # Effects
        if include_effects == "yes":
            lighting = self._get_random_choice("medieval.lighting")
            atmosphere = self._get_random_choice("medieval.atmosphere")
            components["effects"] = (
                f"with ((dramatic {lighting})), ((atmospheric {atmosphere})), "
                f"((historical ambiance)), ((period authenticity)), "
                f"((rich details)), ((perfect exposure))"
            )
            
        return components
