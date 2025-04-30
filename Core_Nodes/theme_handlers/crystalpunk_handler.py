from typing import Dict
from .base_handler import BaseThemeHandler

class CrystalpunkThemeHandler(BaseThemeHandler):
    """Handler for crystalpunk-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate crystalpunk-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        feature = self._get_random_choice("crystalpunk.features")
        crystal = self._get_random_choice("crystalpunk.crystals")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((crystalpunk {custom_subject} with {crystal} crystals)), "
                f"((featuring {feature})), ((crystalline design)), "
                f"((gemstone aesthetic)), ((mineral-tech fusion))"
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
        if include_environment:
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
        if include_style:
            style = self._get_random_choice("crystalpunk.styles")
            technique = self._get_random_choice("crystalpunk.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((crystalline design)), ((gemstone artistry)), "
                f"((mineral-tech quality))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("crystalpunk.effects")
            light = self._get_random_choice("crystalpunk.lighting")
            components["effects"] = (
                f"with ((crystalpunk {effect} effects)), "
                f"((crystalline {light} lighting)), "
                f"((gemstone glow)), ((mineral-tech radiance))"
            )
        
        return components
