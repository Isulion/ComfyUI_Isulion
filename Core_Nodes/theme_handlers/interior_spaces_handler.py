from typing import Dict
from .base_handler import BaseThemeHandler

class InteriorSpacesThemeHandler(BaseThemeHandler):
    """Handler for interior spaces-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate interior spaces-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((interior of {custom_subject})), "
                f"((architectural interior)), ((interior design)), "
                f"((indoor space))"
            )
        else:
            room = self._get_random_choice("interior_spaces.room_types")
            furniture = self._get_random_choice("interior_spaces.furniture")
            decor = self._get_random_choice("interior_spaces.decor")
            components["subject"] = (
                f"((interior of {room})), "
                f"((featuring {furniture})), ((with {decor})), "
                f"((architectural interior)), ((interior design))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((designed {custom_location})) with "
                    f"((interior setting)), ((indoor environment))"
                )
            else:
                style = self._get_random_choice("interior_spaces.styles")
                lighting = self._get_random_choice("interior_spaces.lighting")
                material = self._get_random_choice("interior_spaces.materials")
                components["environment"] = (
                    f"in (({style} space)) with (({lighting})), "
                    f"((featuring {material} elements)), "
                    f"((interior vista)), ((designed space))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            color = self._get_random_choice("interior_spaces.colors")
            atmosphere = self._get_random_choice("interior_spaces.atmospheres")
            components["style"] = (
                f"((styled in {color} palette)), "
                f"(({atmosphere} atmosphere)), "
                f"((interior design aesthetic)), ((architectural beauty)), "
                f"((spatial harmony))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            components["effects"] = (
                f"with ((natural lighting effects)), "
                f"((interior atmosphere)), "
                f"((spatial ambiance)), ((architectural environment))"
            )
        
        return components
