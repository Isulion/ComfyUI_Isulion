from typing import Dict
from .base_handler import BaseThemeHandler

class MangaPanelThemeHandler(BaseThemeHandler):
    """Handler for manga panel-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate manga panel-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((manga panel of {custom_subject})), "
                f"((manga art style)), ((comic panel)), "
                f"((japanese comic))"
            )
        else:
            panel_type = self._get_random_choice("manga_panel.panel_types")
            composition = self._get_random_choice("manga_panel.compositions")
            element = self._get_random_choice("manga_panel.elements")
            components["subject"] = (
                f"((manga panel of {panel_type})), "
                f"((with {composition})), ((featuring {element})), "
                f"((manga art style)), ((comic panel))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((manga {custom_location})) with "
                    f"((comic panel setting)), ((manga environment))"
                )
            else:
                style = self._get_random_choice("manga_panel.styles")
                technique = self._get_random_choice("manga_panel.techniques")
                emotion = self._get_random_choice("manga_panel.emotions")
                components["environment"] = (
                    f"in (({style} style)) with (({technique})), "
                    f"((creating {emotion} mood)), "
                    f"((manga scene)), ((comic panel environment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            atmosphere = self._get_random_choice("manga_panel.atmospheres")
            components["style"] = (
                f"((styled as manga art)), "
                f"(({atmosphere} atmosphere)), "
                f"((comic panel aesthetic)), ((manga design)), "
                f"((japanese comic style))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("manga_panel.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((manga atmosphere)), "
                f"((comic panel effects)), ((manga environment))"
            )
        
        return components
