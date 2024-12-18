from typing import Dict
from .base_handler import BaseThemeHandler

class EssentialVintageThemeHandler(BaseThemeHandler):
    """Handler for essential vintage-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate essential vintage-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((vintage {custom_subject})), "
                f"((retro style)), ((classic look)), "
                f"((nostalgic appearance))"
            )
        else:
            subject = self._get_random_choice("essential_vintage.subjects")
            era = self._get_random_choice("essential_vintage.eras")
            feature = self._get_random_choice("essential_vintage.features")
            components["subject"] = (
                f"((vintage {subject} from {era})), "
                f"((featuring {feature})), ((retro style)), "
                f"((classic look)), ((nostalgic appearance))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((vintage {custom_location})) with "
                    f"((retro setting)), ((classic environment))"
                )
            else:
                setting = self._get_random_choice("essential_vintage.settings")
                element = self._get_random_choice("essential_vintage.elements")
                components["environment"] = (
                    f"in ((vintage {setting})) with "
                    f"((retro {element})), "
                    f"((classic environment)), ((nostalgic atmosphere)), "
                    f"((period accurate details))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("essential_vintage.styles")
            technique = self._get_random_choice("essential_vintage.techniques")
            components["style"] = (
                f"((styled in {style} manner)), "
                f"((using {technique} technique)), "
                f"((vintage aesthetic)), ((retro artistry)), "
                f"((classic quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("essential_vintage.effects")
            tone = self._get_random_choice("essential_vintage.tones")
            components["effects"] = (
                f"with ((vintage {effect} effects)), "
                f"((retro {tone} tones)), "
                f"((classic finish)), ((nostalgic mood))"
            )
        
        return components