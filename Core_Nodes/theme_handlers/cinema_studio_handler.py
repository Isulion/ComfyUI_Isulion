from typing import Dict
from .base_handler import BaseThemeHandler

class CinemaStudioThemeHandler(BaseThemeHandler):
    """Handler for cinema studio-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate cinema studio-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        shot = self._get_random_choice("cinema_studio.shots")
        feature = self._get_random_choice("cinema_studio.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((cinematic {custom_subject} in {shot} shot)), "
                f"((featuring {feature})), ((professional film quality)), "
                f"((movie production)), ((studio cinematography))"
            )
        else:
            subject = self._get_random_choice("cinema_studio.subjects")
            components["subject"] = (
                f"((cinematic {subject} in {shot} shot)), "
                f"((featuring {feature})), ((professional film quality)), "
                f"((movie production)), ((studio cinematography))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((cinematic {custom_location})) with "
                    f"((film set)), ((studio lighting))"
                )
            else:
                setting = self._get_random_choice("cinema_studio.settings")
                element = self._get_random_choice("cinema_studio.elements")
                components["environment"] = (
                    f"in ((cinematic {setting})) with "
                    f"((studio {element})), "
                    f"((film set)), ((production background)), "
                    f"((movie environment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("cinema_studio.styles")
            technique = self._get_random_choice("cinema_studio.techniques")
            components["style"] = (
                f"((filmed in {style} style)), "
                f"((using {technique} technique)), "
                f"((cinematic quality)), ((studio production)), "
                f"((professional filming))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("cinema_studio.effects")
            lighting = self._get_random_choice("cinema_studio.lighting")
            components["effects"] = (
                f"with ((cinematic {effect} effects)), "
                f"((studio {lighting} lighting)), "
                f"((film grade)), ((production finish))"
            )
        
        return components
