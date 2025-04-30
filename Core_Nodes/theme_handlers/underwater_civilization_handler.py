from typing import Dict
from .base_handler import BaseThemeHandler

class UnderwaterCivilizationThemeHandler(BaseThemeHandler):
    """Handler for underwater civilization-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate underwater civilization-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        technology = self._get_random_choice("underwater_civilization.technology")
        creature = self._get_random_choice("underwater_civilization.creatures")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((underwater {custom_subject})), "
                f"((using {technology})), ((with {creature})), "
                f"((aquatic)), ((oceanic)), ((submerged))"
            )
        else:
            inhabitant = self._get_random_choice("underwater_civilization.inhabitants")
            technology = self._get_random_choice("underwater_civilization.technology")
            creature = self._get_random_choice("underwater_civilization.creatures")
            components["subject"] = (
                f"((underwater {inhabitant})), "
                f"((using {technology})), ((with {creature})), "
                f"((aquatic)), ((oceanic))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((underwater {custom_location})) with "
                    f"((aquatic setting)), ((oceanic environment))"
                )
            else:
                environment = self._get_random_choice("underwater_civilization.environment")
                structure = self._get_random_choice("underwater_civilization.structures")
                element = self._get_random_choice("underwater_civilization.elements")
                components["environment"] = (
                    f"in (({environment})) with (({structure})), "
                    f"((featuring {element})), "
                    f"((underwater vista)), ((oceanic realm))"
                )
        
        # Generate style if requested
        if include_style:
            atmosphere = self._get_random_choice("underwater_civilization.atmospheres")
            components["style"] = (
                f"((styled as {atmosphere})), "
                f"((underwater aesthetic)), "
                f"((aquatic design)), ((oceanic look)), "
                f"((submerged authenticity))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("underwater_civilization.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((underwater atmosphere)), "
                f"((aquatic ambiance)), ((oceanic environment))"
            )
        
        return components
