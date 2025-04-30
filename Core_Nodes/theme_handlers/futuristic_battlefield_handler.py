from typing import Dict
from .base_handler import BaseThemeHandler

class FuturisticBattlefieldThemeHandler(BaseThemeHandler):
    """Handler for futuristic battlefield-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate futuristic battlefield-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        weapon = self._get_random_choice("futuristic_battlefield.weapons")
        tech = self._get_random_choice("futuristic_battlefield.tech")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((futuristic {custom_subject} wielding {weapon})), "
                f"((equipped with {tech})), ((advanced warfare)), "
                f"((high-tech combat)), ((military technology))"
            )
        else:
            subject = self._get_random_choice("futuristic_battlefield.subjects")
            weapon = self._get_random_choice("futuristic_battlefield.weapons")
            tech = self._get_random_choice("futuristic_battlefield.tech")
            components["subject"] = (
                f"((futuristic {subject} wielding {weapon})), "
                f"((equipped with {tech})), ((advanced warfare)), "
                f"((high-tech combat)), ((military technology))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})) with "
                    f"((war-torn setting)), ((battlefield environment))"
                )
            else:
                setting = self._get_random_choice("futuristic_battlefield.settings")
                element = self._get_random_choice("futuristic_battlefield.elements")
                components["environment"] = (
                    f"in ((futuristic {setting})) with "
                    f"((advanced {element})), "
                    f"((war-torn environment)), ((combat zone)), "
                    f"((military installation))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("futuristic_battlefield.styles")
            aesthetic = self._get_random_choice("futuristic_battlefield.aesthetics")
            components["style"] = (
                f"((styled with {style} aesthetic)), "
                f"((featuring {aesthetic} design)), "
                f"((military precision)), ((advanced technology)), "
                f"((futuristic warfare))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("futuristic_battlefield.effects")
            atmosphere = self._get_random_choice("futuristic_battlefield.atmospheres")
            components["effects"] = (
                f"with ((futuristic {effect} effects)), "
                f"((combat {atmosphere} atmosphere)), "
                f"((battlefield ambiance)), ((war-torn environment))"
            )
        
        return components
