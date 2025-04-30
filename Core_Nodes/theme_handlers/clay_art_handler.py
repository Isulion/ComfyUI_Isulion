from typing import Dict
from .base_handler import BaseThemeHandler

class ClayArtThemeHandler(BaseThemeHandler):
    """Handler for clay art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate clay art-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        texture = self._get_random_choice("clay_art.textures")
        detail = self._get_random_choice("clay_art.details")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((clay art {custom_subject} with {texture} texture)), "
                f"((featuring {detail})), ((sculpted figure)), "
                f"((ceramic design)), ((moldable creation))"
            )
        else:
            figure = self._get_random_choice("clay_art.figures")
            texture = self._get_random_choice("clay_art.textures")
            detail = self._get_random_choice("clay_art.details")
            components["subject"] = (
                f"((clay art {figure} with {texture} texture)), "
                f"((featuring {detail})), ((sculpted figure)), "
                f"((ceramic design)), ((moldable creation))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((clay art {custom_location})) with "
                    f"((ceramic setting)), ((sculpted environment))"
                )
            else:
                setting = self._get_random_choice("clay_art.settings")
                element = self._get_random_choice("clay_art.elements")
                components["environment"] = (
                    f"in ((clay art {setting})) with "
                    f"((ceramic {element})), "
                    f"((sculpted environment)), ((moldable surroundings)), "
                    f"((pottery world))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("clay_art.styles")
            technique = self._get_random_choice("clay_art.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((ceramic design)), ((clay artistry)), "
                f"((sculptural quality))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("clay_art.effects")
            finish = self._get_random_choice("clay_art.finishes")
            components["effects"] = (
                f"with ((clay art {effect} effects)), "
                f"((ceramic {finish} finish)), "
                f"((sculptural texture)), ((pottery surface))"
            )
        
        return components
