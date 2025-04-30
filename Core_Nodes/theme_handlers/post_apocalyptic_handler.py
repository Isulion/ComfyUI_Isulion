from typing import Dict
from .base_handler import BaseThemeHandler

class PostApocalypticThemeHandler(BaseThemeHandler):
    """Handler for post-apocalyptic wasteland-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate post-apocalyptic wasteland-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        equipment = self._get_random_choice("post_apocalyptic.equipment")
        vehicle = self._get_random_choice("post_apocalyptic.vehicles")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((post-apocalyptic {custom_subject})), "
                f"((wearing {equipment})), ((with {vehicle})), "
                f"((wasteland style)), ((survival)), "
                f"((post-nuclear))"
            )
        else:
            survivor = self._get_random_choice("post_apocalyptic.survivors")
            equipment = self._get_random_choice("post_apocalyptic.equipment")
            vehicle = self._get_random_choice("post_apocalyptic.vehicles")
            components["subject"] = (
                f"((post-apocalyptic {survivor})), "
                f"((wearing {equipment})), ((with {vehicle})), "
                f"((wasteland style)), ((survival))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((post-apocalyptic {custom_location})) with "
                    f"((wasteland setting)), ((destroyed environment))"
                )
            else:
                environment = self._get_random_choice("post_apocalyptic.environments")
                weather = self._get_random_choice("post_apocalyptic.weather")
                structure = self._get_random_choice("post_apocalyptic.structures")
                components["environment"] = (
                    f"in (({environment})) with (({weather})), "
                    f"((featuring {structure})), "
                    f"((wasteland vista)), ((destroyed world))"
                )
        
        # Generate style if requested
        if include_style:
            atmosphere = self._get_random_choice("post_apocalyptic.atmospheres")
            components["style"] = (
                f"((styled as {atmosphere})), "
                f"((post-apocalyptic aesthetic)), "
                f"((wasteland design)), ((survival look)), "
                f"((post-nuclear authenticity))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("post_apocalyptic.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((wasteland atmosphere)), "
                f"((post-apocalyptic ambiance)), ((destroyed environment))"
            )
        
        return components
