from typing import Dict
from .base_handler import BaseThemeHandler

class MarvelThemeHandler(BaseThemeHandler):
    """Handler for Marvel-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Marvel-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        costume = self._get_random_choice("marvel.costumes")
        pose = self._get_random_choice("marvel.poses")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((Marvel-style {custom_subject})) wearing ((epic {costume})), "
                f"((in {pose})), ((superhero aesthetic)), "
                f"((comic book style)), ((dynamic pose))"
            )
        else:
            character = self._get_random_choice("marvel.characters")
            costume = self._get_random_choice("marvel.costumes")
            pose = self._get_random_choice("marvel.poses")
            components["subject"] = (
                f"((Marvel-style {character})) wearing ((epic {costume})), "
                f"((in {pose})), ((superhero aesthetic)), "
                f"((comic book style)), ((dynamic pose))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((epic {custom_location})) with "
                    f"((Marvel atmosphere)), ((superhero setting))"
                )
            else:
                location = self._get_random_choice("marvel.locations")
                props = self._get_random_choice("marvel.props")
                components["environment"] = (
                    f"in ((epic {location})) with "
                    f"((dramatic {props})), "
                    f"((Marvel atmosphere)), ((superhero setting)), "
                    f"((comic book environment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("marvel.styles")
            artist = self._get_random_choice("marvel.artists")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((inspired by {artist})), "
                f"((Marvel comics aesthetics)), ((superhero art)), "
                f"((dynamic comic style))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("marvel.effects")
            power = self._get_random_choice("marvel.powers")
            components["effects"] = (
                f"with ((epic {effect} effects)), "
                f"((dramatic {power} powers)), "
                f"((Marvel energy)), ((superhero impact))"
            )
        
        return components
