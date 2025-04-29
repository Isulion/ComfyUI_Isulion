from typing import Dict
from .base_handler import BaseThemeHandler

class MicroscopicThemeHandler(BaseThemeHandler):
    """Handler for microscopic-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate microscopic-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        style = self._get_random_choice("microscopic.styles")
        technique = self._get_random_choice("microscopic.techniques")
        detail = self._get_random_choice("microscopic.details")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((microscopic view of {custom_subject})), "
                f"((with {detail})), ((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((cellular detail)), ((molecular structure)), "
                f"((microscope magnification))"
            )
        else:
            specimen = self._get_random_choice("microscopic.specimens")
            structure = self._get_random_choice("microscopic.structures")
            detail = self._get_random_choice("microscopic.details")
            components["subject"] = (
                f"((microscopic view of {specimen})) showing ((detailed {structure})), "
                f"((with {detail})), ((cellular detail)), "
                f"((molecular structure)), ((microscope magnification))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((microscopic {custom_location})) with "
                    f"((cellular environment)), ((molecular surroundings))"
                )
            else:
                environment = self._get_random_choice("microscopic.environments")
                feature = self._get_random_choice("microscopic.features")
                components["environment"] = (
                    f"in ((microscopic {environment})) with "
                    f"((detailed {feature})), "
                    f"((cellular environment)), ((molecular surroundings)), "
                    f"((microscopic world))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("microscopic.styles")
            technique = self._get_random_choice("microscopic.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((scientific visualization)), ((microscopic detail)), "
                f"((cellular aesthetics))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("microscopic.effects")
            coloring = self._get_random_choice("microscopic.coloring")
            components["effects"] = (
                f"with ((microscopic {effect} effects)), "
                f"((cellular {coloring} coloring)), "
                f"((molecular visualization)), ((microscope lens effects))"
            )
        
        return components
