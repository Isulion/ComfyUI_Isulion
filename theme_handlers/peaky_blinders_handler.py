from typing import Dict
from .base_handler import BaseThemeHandler

class PeakyBlindersThemeHandler(BaseThemeHandler):
    """Handler for Peaky Blinders-themed prompt generation, focusing on 1920s Birmingham."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid modern elements."""
        negative_elements = self._get_random_choices("peaky_blinders.negative_prompts", 6)
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate historically accurate 1920s Peaky Blinders-themed components."""
        components = {}
        
        # Get custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        character = self._get_random_choice("peaky_blinders.characters")
        clothing = self._get_random_choice("peaky_blinders.clothing")
        props = self._get_random_choice("peaky_blinders.period_props")
        color_scheme = self._get_random_choice("peaky_blinders.color_schemes")
        period_elements = self._get_random_choice("peaky_blinders.period_elements")
        
        if custom_subject:
            components["subject"] = (
                f"((1920s portrait)) of {custom_subject}, "
                f"((wearing {clothing})), ((with {props})), "
                f"((period accurate details)), ((1920s style)), "
                f"in tones of {color_scheme}, ((historical accuracy))"
            )
        else:
            components["subject"] = (
                f"((1920s portrait)) of a ((Birmingham {character})), "
                f"((wearing {clothing})), ((with {props})), "
                f"((period accurate details)), ((1920s style)), "
                f"in tones of {color_scheme}, ((historical accuracy))"
            )
        
        if include_environment == "yes":
            if custom_location:
                lighting = self._get_random_choice("peaky_blinders.lighting")
                components["environment"] = (
                    f"in ((1920s {custom_location})), ((with {period_elements})), "
                    f"((illuminated by {lighting})), ((historical setting)), "
                    f"((industrial era atmosphere)), ((period accurate))"
                )
            else:
                setting = self._get_random_choice("peaky_blinders.period_settings")
                lighting = self._get_random_choice("peaky_blinders.lighting")
                components["environment"] = (
                    f"in ((a {setting})), ((with {period_elements})), "
                    f"((illuminated by {lighting})), ((historical setting)), "
                    f"((industrial era atmosphere)), ((period accurate))"
                )
        
        if include_style == "yes":
            style = self._get_random_choice("peaky_blinders.period_styles")
            mood = self._get_random_choice("peaky_blinders.mood")
            components["style"] = (
                f"((authentic {style})), ((historical photography)), "
                f"((period accurate details)), (({mood} atmosphere)), "
                f"((1920s aesthetic)), ((vintage photo quality)), "
                f"((historical drama)), ((film grain)), "
                f"8k resolution, ((masterful composition))"
            )
        
        if include_effects == "yes":
            components["effects"] = (
                f"with ((period photo effects)), ((vintage film grain)), "
                f"((historical color grading)), ((authentic aging)), "
                f"((1920s photo style)), ((industrial atmosphere)), "
                f"((smoky ambiance)), ((historical authenticity))"
            )
        
        return components
