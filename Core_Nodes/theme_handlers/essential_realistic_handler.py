from typing import Dict
from .base_handler import BaseThemeHandler

class EssentialRealisticThemeHandler(BaseThemeHandler):
    """Handler for essential realistic-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate essential realistic-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        detail = self._get_random_choice("essential_realistic.details")
        feature = self._get_random_choice("essential_realistic.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((realistic {custom_subject} with {detail})), "
                f"((featuring {feature})), ((photorealistic)), "
                f"((true to life)), ((natural appearance))"
            )
        else:
            subject = self._get_random_choice("essential_realistic.subjects")
            detail = self._get_random_choice("essential_realistic.details")
            feature = self._get_random_choice("essential_realistic.features")
            components["subject"] = (
                f"((realistic {subject} with {detail})), "
                f"((featuring {feature})), ((photorealistic)), "
                f"((true to life)), ((natural appearance))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((realistic {custom_location})) with "
                    f"((natural setting)), ((authentic environment))"
                )
            else:
                setting = self._get_random_choice("essential_realistic.settings")
                element = self._get_random_choice("essential_realistic.elements")
                components["environment"] = (
                    f"in ((realistic {setting})) with "
                    f"((natural {element})), "
                    f"((authentic environment)), ((true setting)), "
                    f"((real world atmosphere))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("essential_realistic.styles")
            technique = self._get_random_choice("essential_realistic.techniques")
            components["style"] = (
                f"((captured in {style} style)), "
                f"((using {technique} technique)), "
                f"((photorealistic quality)), ((authentic representation)), "
                f"((natural rendering))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("essential_realistic.effects")
            lighting = self._get_random_choice("essential_realistic.lighting")
            components["effects"] = (
                f"with ((realistic {effect} effects)), "
                f"((natural {lighting} lighting)), "
                f"((true to life)), ((authentic finish))"
            )
        
        return components
