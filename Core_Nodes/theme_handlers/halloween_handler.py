from typing import Dict
from .base_handler import BaseThemeHandler

class HalloweenThemeHandler(BaseThemeHandler):
    """Handler for Halloween-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Halloween-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        costume = self._get_random_choice("halloween.costumes")
        pose = self._get_random_choice("halloween.poses")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((spooky {custom_subject})) wearing ((creepy {costume})), "
                f"((in {pose})), ((Halloween theme)), "
                f"((eerie presence)), ((haunting appearance))"
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
        if include_environment:
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
        if include_style:
            style = self._get_random_choice("halloween.styles")
            mood = self._get_random_choice("halloween.moods")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {mood} mood)), "
                f"((Halloween aesthetics)), ((spooky artistry)), "
                f"((haunting quality))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("halloween.effects")
            lighting = self._get_random_choice("halloween.lighting")
            components["effects"] = (
                f"with ((spooky {effect} effects)), "
                f"((eerie {lighting} lighting)), "
                f"((Halloween ambiance)), ((haunting atmosphere))"
            )
        
        return components
