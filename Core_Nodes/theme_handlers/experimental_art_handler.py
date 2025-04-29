from typing import Dict
from .base_handler import BaseThemeHandler

class ExperimentalArtThemeHandler(BaseThemeHandler):
    """Handler for experimental art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate experimental art-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        concept = self._get_random_choice("experimental_art.concepts")
        technique = self._get_random_choice("experimental_art.techniques")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((experimental {custom_subject} exploring {concept})), "
                f"((using {technique})), ((avant-garde)), "
                f"((innovative)), ((unconventional approach))"
            )
        else:
            subject = self._get_random_choice("experimental_art.subjects")
            concept = self._get_random_choice("experimental_art.concepts")
            technique = self._get_random_choice("experimental_art.techniques")
            components["subject"] = (
                f"((experimental {subject} exploring {concept})), "
                f"((using {technique})), ((avant-garde)), "
                f"((innovative)), ((unconventional approach))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((experimental {custom_location})) with "
                    f"((abstract setting)), ((innovative space))"
                )
            else:
                setting = self._get_random_choice("experimental_art.settings")
                element = self._get_random_choice("experimental_art.elements")
                components["environment"] = (
                    f"in ((experimental {setting})) with "
                    f"((innovative {element})), "
                    f"((abstract environment)), ((avant-garde atmosphere)), "
                    f"((unconventional space))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("experimental_art.styles")
            method = self._get_random_choice("experimental_art.methods")
            components["style"] = (
                f"((styled with {style} approach)), "
                f"((using {method} method)), "
                f"((experimental aesthetic)), ((innovative artistry)), "
                f"((avant-garde quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("experimental_art.effects")
            texture = self._get_random_choice("experimental_art.textures")
            components["effects"] = (
                f"with ((experimental {effect} effects)), "
                f"((innovative {texture} textures)), "
                f"((avant-garde finish)), ((unconventional treatment))"
            )
        
        return components
