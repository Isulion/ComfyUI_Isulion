from typing import Dict
from .base_handler import BaseThemeHandler

class CaricatureThemeHandler(BaseThemeHandler):
    """Handler for caricature-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate caricature-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((exaggerated caricature)) of ((humorous {custom_subject})), "
                f"((comical proportions)), ((expressive features)), "
                f"((cartoon style))"
            )
        else:
            character = self._get_random_choice("caricature.characters")
            expression = self._get_random_choice("caricature.expressions")
            pose = self._get_random_choice("caricature.poses")
            components["subject"] = (
                f"((exaggerated caricature)) of ((humorous {character})), "
                f"((with {expression} expression)), ((in {pose})), "
                f"((comical proportions)), ((expressive features)), "
                f"((cartoon style))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((whimsical {custom_location})) with "
                    f"((humorous details)), ((playful atmosphere))"
                )
            else:
                setting = self._get_random_choice("caricature.settings")
                props = self._get_random_choice("caricature.props")
                components["environment"] = (
                    f"in ((whimsical {setting})) with "
                    f"((humorous {props})), "
                    f"((playful atmosphere)), ((comic scene))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("caricature.styles")
            technique = self._get_random_choice("caricature.techniques")
            components["style"] = (
                f"((drawn in {style} style)), "
                f"((using {technique} technique)), "
                f"((exaggerated art)), ((comic artistry)), "
                f"((professional caricature))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("caricature.effects")
            detail = self._get_random_choice("caricature.details")
            components["effects"] = (
                f"with ((humorous {effect} effects)), "
                f"((exaggerated {detail})), "
                f"((comic charm)), ((playful energy))"
            )
        
        return components
