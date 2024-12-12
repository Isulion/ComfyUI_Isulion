from typing import Dict
from .base_handler import BaseThemeHandler

class HalloweenThemeHandler(BaseThemeHandler):
    """Handler for Halloween-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Halloween-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((spooky {custom_subject})), "
                f"((Halloween theme)), ((eerie presence)), "
                f"((haunting appearance))"
            )
        else:
            character = self._get_random_choice("halloween.characters")
            costume = self._get_random_choice("halloween.costumes")
            pose = self._get_random_choice("halloween.poses")
            components["subject"] = (
                f"((spooky {character})) wearing ((creepy {costume})), "
                f"((in {pose})), ((Halloween theme)), "
                f"((eerie presence)), ((haunting appearance))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((haunted {custom_location})) with "
                    f"((spooky decorations)), ((Halloween atmosphere))"
                )
            else:
                location = self._get_random_choice("halloween.locations")
                decoration = self._get_random_choice("halloween.decorations")
                components["environment"] = (
                    f"in ((haunted {location})) with "
                    f"((spooky {decoration})), "
                    f"((Halloween atmosphere)), ((eerie setting))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("halloween.styles")
            mood = self._get_random_choice("halloween.moods")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {mood} mood)), "
                f"((Halloween aesthetics)), ((spooky artistry)), "
                f"((haunting quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("halloween.effects")
            lighting = self._get_random_choice("halloween.lighting")
            components["effects"] = (
                f"with ((spooky {effect} effects)), "
                f"((eerie {lighting} lighting)), "
                f"((Halloween ambiance)), ((haunting atmosphere))"
            )
        
        return components
