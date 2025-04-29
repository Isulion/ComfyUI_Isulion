from typing import Dict
from .base_handler import BaseThemeHandler

class CrayonArtThemeHandler(BaseThemeHandler):
    """Handler for crayon art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate crayon art-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        color = self._get_random_choice("crayon_art.colors")
        feature = self._get_random_choice("crayon_art.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((crayon art {custom_subject} in {color} colors)), "
                f"((featuring {feature})), ((childlike drawing)), "
                f"((crayon sketch)), ((hand-drawn creation))"
            )
        else:
            subject = self._get_random_choice("crayon_art.subjects")
            color = self._get_random_choice("crayon_art.colors")
            feature = self._get_random_choice("crayon_art.features")
            components["subject"] = (
                f"((crayon art {subject} in {color} colors)), "
                f"((featuring {feature})), ((childlike drawing)), "
                f"((crayon sketch)), ((hand-drawn creation))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((crayon art {custom_location})) with "
                    f"((childlike setting)), ((hand-drawn environment))"
                )
            else:
                setting = self._get_random_choice("crayon_art.settings")
                element = self._get_random_choice("crayon_art.elements")
                components["environment"] = (
                    f"in ((crayon art {setting})) with "
                    f"((childlike {element})), "
                    f"((hand-drawn environment)), ((crayon background)), "
                    f"((sketched surroundings))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("crayon_art.styles")
            technique = self._get_random_choice("crayon_art.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((childlike art)), ((crayon artistry)), "
                f"((hand-drawn quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("crayon_art.effects")
            texture = self._get_random_choice("crayon_art.textures")
            components["effects"] = (
                f"with ((crayon art {effect} effects)), "
                f"((childlike {texture} texture)), "
                f"((hand-drawn style)), ((sketched finish))"
            )
        
        return components
