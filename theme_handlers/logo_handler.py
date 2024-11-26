from typing import Dict
from .base_handler import BaseThemeHandler

class LogoThemeHandler(BaseThemeHandler):
    """Handler for logo-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate logo-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((minimalist logo design)) of ((stylized {custom_subject})), "
                f"((clean lines)), ((professional branding)), "
                f"((vector style))"
            )
        else:
            style = self._get_random_choice("logo.styles")
            element = self._get_random_choice("logo.elements")
            color_scheme = self._get_random_choice("logo.color_schemes")
            components["subject"] = (
                f"((minimalist {style} logo design)) with ((stylized {element})), "
                f"((featuring {color_scheme} color scheme)), "
                f"((clean lines)), ((professional branding)), "
                f"((vector style))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"on ((clean {custom_location} background)) with "
                    f"((professional layout)), ((balanced composition))"
                )
            else:
                background = self._get_random_choice("logo.backgrounds")
                layout = self._get_random_choice("logo.layouts")
                components["environment"] = (
                    f"on ((clean {background} background)) with "
                    f"((professional {layout} layout)), "
                    f"((balanced composition)), ((perfect alignment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            typography = self._get_random_choice("logo.typography")
            technique = self._get_random_choice("logo.techniques")
            components["style"] = (
                f"((professional {typography} typography)), "
                f"((using {technique} technique)), "
                f"((modern design principles)), "
                f"((corporate identity))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("logo.effects")
            finish = self._get_random_choice("logo.finishes")
            components["effects"] = (
                f"with ((subtle {effect} effects)), "
                f"((professional {finish} finish)), "
                f"((perfect execution)), ((brand consistency))"
            )
        
        return components
