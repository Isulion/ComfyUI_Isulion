from typing import Dict
from .base_handler import BaseThemeHandler

class CrystalpunkThemeHandler(BaseThemeHandler):
    """Handler for crystalpunk-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate crystalpunk-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((crystalpunk {custom_subject})), "
                f"((crystalline design)), ((gemstone aesthetic)), "
                f"((mineral-tech fusion))"
            )
        else:
            character = self._get_random_choice("crystalpunk.characters")
            crystal = self._get_random_choice("crystalpunk.crystals")
            feature = self._get_random_choice("crystalpunk.features")
            components["subject"] = (
                f"((crystalpunk {character} with {crystal} crystals)), "
                f"((featuring {feature})), ((crystalline design)), "
                f"((gemstone aesthetic)), ((mineral-tech fusion))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((crystalpunk {custom_location})) with "
                    f"((crystalline setting)), ((gemstone environment))"
                )
            else:
                setting = self._get_random_choice("crystalpunk.settings")
                element = self._get_random_choice("crystalpunk.elements")
                components["environment"] = (
                    f"in ((crystalpunk {setting})) with "
                    f"((crystalline {element})), "
                    f"((gemstone environment)), ((mineral background)), "
                    f"((crystal-tech world))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("crystalpunk.styles")
            technique = self._get_random_choice("crystalpunk.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((crystalline design)), ((gemstone artistry)), "
                f"((mineral-tech quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("crystalpunk.effects")
            light = self._get_random_choice("crystalpunk.lighting")
            components["effects"] = (
                f"with ((crystalpunk {effect} effects)), "
                f"((crystalline {light} lighting)), "
                f"((gemstone glow)), ((mineral-tech radiance))"
            )
        
        return components
