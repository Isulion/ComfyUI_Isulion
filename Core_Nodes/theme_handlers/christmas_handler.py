from typing import Dict
from .base_handler import BaseThemeHandler

class ChristmasThemeHandler(BaseThemeHandler):
    """Handler for Christmas-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = self._get_random_choices("christmas.negative_prompts", 6)
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Christmas-themed components."""
        components = {}
        
        # Get custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        character = self._get_random_choice("christmas.characters")
        attire = self._get_random_choice("christmas.attire")
        props = self._get_random_choice("christmas.props")
        food = self._get_random_choice("christmas.foods")
        decorations = self._get_random_choice("christmas.decorations")
        color_scheme = self._get_random_choice("christmas.color_schemes")
        
        if custom_subject:
            components["subject"] = (
                f"((festive Christmas scene)) of {custom_subject}, "
                f"((wearing {attire})), ((with {props})), "
                f"((surrounded by {decorations})), "
                f"in {color_scheme} colors, ((holiday spirit)), ((Christmas magic))"
            )
        else:
            components["subject"] = (
                f"((festive Christmas scene)) of ((a {character})), "
                f"((wearing {attire})), ((with {props})), "
                f"((enjoying {food})), ((surrounded by {decorations})), "
                f"in {color_scheme} colors, ((holiday spirit)), ((Christmas magic))"
            )
        
        if include_environment:
            if custom_location:
                lighting = self._get_random_choice("christmas.lighting")
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for Christmas)), "
                    f"((illuminated by {lighting})), ((holiday atmosphere)), "
                    f"((Christmas decorations)), ((winter charm))"
                )
            else:
                setting = self._get_random_choice("christmas.settings")
                lighting = self._get_random_choice("christmas.lighting")
                weather = self._get_random_choice("christmas.weather")
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {lighting})), "
                    f"with ((beautiful {weather})), ((holiday atmosphere)), "
                    f"((Christmas decorations)), ((winter wonderland))"
                )
        
        if include_style:
            components["style"] = (
                f"((traditional Christmas artwork)), ((festive holiday style)), "
                f"((professional photography)), ((perfect composition)), "
                f"((holiday color palette)), ((seasonal charm)), "
                f"((Christmas card quality)), ((warm holiday atmosphere)), "
                f"8k resolution, ((masterful lighting))"
            )
        
        if include_effects:
            components["effects"] = (
                f"with ((magical Christmas glow)), ((soft winter light)), "
                f"((twinkling holiday lights)), ((gentle snow effects)), "
                f"((warm festive atmosphere)), ((seasonal magic)), "
                f"((Christmas sparkle)), ((cozy holiday ambiance))"
            )
        
        return components
