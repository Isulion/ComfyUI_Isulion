from typing import Dict
from .base_handler import BaseThemeHandler

class MinimalistThemeHandler(BaseThemeHandler):
    """Handler for minimalist-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate minimalist-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((minimalist {custom_subject})), "
                f"((clean design)), ((simple form)), "
                f"((elegant simplicity))"
            )
        else:
            subject = self._get_random_choice("minimalist.subjects")
            form = self._get_random_choice("minimalist.forms")
            element = self._get_random_choice("minimalist.elements")
            components["subject"] = (
                f"((minimalist {subject})) with ((simple {form})), "
                f"((featuring {element})), ((clean design)), "
                f"((elegant simplicity)), ((pure form))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((minimalist {custom_location})) with "
                    f"((clean space)), ((simple background))"
                )
            else:
                space = self._get_random_choice("minimalist.spaces")
                feature = self._get_random_choice("minimalist.features")
                components["environment"] = (
                    f"in ((minimalist {space})) with "
                    f"((simple {feature})), "
                    f"((clean space)), ((pure background)), "
                    f"((minimal setting))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("minimalist.styles")
            aesthetic = self._get_random_choice("minimalist.aesthetics")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetic)), "
                f"((minimalist design)), ((clean artistry)), "
                f"((simple elegance))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("minimalist.effects")
            tone = self._get_random_choice("minimalist.tones")
            components["effects"] = (
                f"with ((minimal {effect} effects)), "
                f"((simple {tone} tones)), "
                f"((clean finish)), ((pure lighting))"
            )
        
        return components
