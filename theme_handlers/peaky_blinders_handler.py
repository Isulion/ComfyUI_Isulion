from typing import Dict
from .base_handler import BaseThemeHandler

class PeakyBlindersThemeHandler(BaseThemeHandler):
    """Handler for Peaky Blinders-themed prompt generation, focusing on 1920s Birmingham."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid modern elements."""
        negative_elements = self._get_random_choices("peaky_blinders.negative_prompts", 8)
        return ", ".join(negative_elements) + ", modern background, contemporary setting, current era architecture"

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
        clothing = self._get_random_choices("peaky_blinders.clothing", 2)
        props = self._get_random_choices("peaky_blinders.period_props", 2)
        color_scheme = self._get_random_choice("peaky_blinders.color_schemes")
        period_elements = self._get_random_choices("peaky_blinders.period_elements", 3)
        
        if custom_subject:
            components["subject"] = (
                f"((1920s historical portrait)) of {custom_subject}, "
                f"((wearing {', '.join(clothing)})), ((with {', '.join(props)})), "
                f"((strictly period accurate details)), ((1920s Birmingham style)), "
                f"in tones of {color_scheme}, ((historical accuracy)), ((1920s era))"
            )
        else:
            components["subject"] = (
                f"((1920s historical portrait)) of a ((Birmingham {character})), "
                f"((wearing {', '.join(clothing)})), ((with {', '.join(props)})), "
                f"((strictly period accurate details)), ((1920s Birmingham style)), "
                f"in tones of {color_scheme}, ((historical accuracy)), ((1920s era))"
            )
        
        if include_environment == "yes":
            if custom_location:
                lighting = self._get_random_choice("peaky_blinders.lighting")
                components["environment"] = (
                    f"in ((1920s {custom_location})), ((with {', '.join(period_elements)})), "
                    f"((illuminated by {lighting})), ((authentic historical setting)), "
                    f"((1920s industrial atmosphere)), ((Victorian era architecture)), "
                    f"((no modern elements)), ((period accurate Birmingham))"
                )
            else:
                setting = self._get_random_choice("peaky_blinders.period_settings")
                lighting = self._get_random_choice("peaky_blinders.lighting")
                components["environment"] = (
                    f"in ((a {setting})), ((with {', '.join(period_elements)})), "
                    f"((illuminated by {lighting})), ((authentic historical setting)), "
                    f"((1920s industrial atmosphere)), ((Victorian era architecture)), "
                    f"((no modern elements)), ((period accurate Birmingham))"
                )
        
        if include_style == "yes":
            style = self._get_random_choice("peaky_blinders.period_styles")
            mood = self._get_random_choice("peaky_blinders.mood")
            components["style"] = (
                f"((authentic {style})), ((historical photography)), "
                f"((strictly period accurate details)), (({mood} atmosphere)), "
                f"((1920s documentary aesthetic)), ((vintage photo quality)), "
                f"((historical drama)), ((period appropriate film grain)), "
                f"((Victorian industrial era)), 8k resolution, ((masterful composition))"
            )
        
        if include_effects == "yes":
            components["effects"] = (
                f"with ((1920s photo effects)), ((period appropriate film grain)), "
                f"((historical color grading)), ((authentic aging)), "
                f"((early photography style)), ((industrial atmosphere)), "
                f"((coal smoke ambiance)), ((historical authenticity)), "
                f"((no modern post-processing))"
            )
        
        return components
