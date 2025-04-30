from typing import Dict
from .base_handler import BaseThemeHandler

class CurvyFashionThemeHandler(BaseThemeHandler):
    """Handler for curvy fashion-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate curvy fashion-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        model = self._get_random_choice("curvy_fashion.models")
        outfit = self._get_random_choice("curvy_fashion.outfits")
        feature = self._get_random_choice("curvy_fashion.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((curvy fashion {custom_subject})), "
                f"((modeled by {model} wearing {outfit})), "
                f"((featuring {feature})), ((plus size model)), "
                f"((body positive)), ((fashion photography))"
            )
        else:
            components["subject"] = (
                f"((curvy fashion {model} wearing {outfit})), "
                f"((featuring {feature})), ((plus size model)), "
                f"((body positive)), ((fashion photography))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((fashion {custom_location})) with "
                    f"((professional setting)), ((fashion backdrop))"
                )
            else:
                setting = self._get_random_choice("curvy_fashion.settings")
                element = self._get_random_choice("curvy_fashion.elements")
                components["environment"] = (
                    f"in ((fashion {setting})) with "
                    f"((fashion {element})), "
                    f"((professional setting)), ((fashion backdrop)), "
                    f"((studio environment))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("curvy_fashion.styles")
            technique = self._get_random_choice("curvy_fashion.techniques")
            components["style"] = (
                f"((styled in {style} fashion)), "
                f"((using {technique} technique)), "
                f"((fashion photography)), ((professional styling)), "
                f"((body positive representation))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("curvy_fashion.effects")
            lighting = self._get_random_choice("curvy_fashion.lighting")
            components["effects"] = (
                f"with ((fashion {effect} effects)), "
                f"((studio {lighting} lighting)), "
                f"((professional finish)), ((fashion quality))"
            )
        
        return components
