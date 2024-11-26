from typing import Dict
from .base_handler import BaseThemeHandler

class ComicBookThemeHandler(BaseThemeHandler):
    """Handler for comic book-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate comic book-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((comic book {custom_subject})), "
                f"((graphic novel style)), ((comic art)), "
                f"((illustrated character))"
            )
        else:
            character = self._get_random_choice("comic_book.characters")
            pose = self._get_random_choice("comic_book.poses")
            feature = self._get_random_choice("comic_book.features")
            components["subject"] = (
                f"((comic book {character} in {pose} pose)), "
                f"((featuring {feature})), ((graphic novel style)), "
                f"((comic art)), ((illustrated character))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((comic book {custom_location})) with "
                    f"((graphic novel setting)), ((comic panel))"
                )
            else:
                setting = self._get_random_choice("comic_book.settings")
                element = self._get_random_choice("comic_book.elements")
                components["environment"] = (
                    f"in ((comic book {setting})) with "
                    f"((graphic novel {element})), "
                    f"((comic panel)), ((illustrated background)), "
                    f"((sequential art))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("comic_book.styles")
            technique = self._get_random_choice("comic_book.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((comic art)), ((graphic novel design)), "
                f"((sequential art quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("comic_book.effects")
            texture = self._get_random_choice("comic_book.textures")
            components["effects"] = (
                f"with ((comic book {effect} effects)), "
                f"((graphic novel {texture} texture)), "
                f"((comic art style)), ((illustrated finish))"
            )
        
        return components
