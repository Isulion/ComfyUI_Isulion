from typing import Dict
from .base_handler import BaseThemeHandler

class PeakyBlindersThemeHandler(BaseThemeHandler):
    """Handler for Peaky Blinders-themed prompt generation, focusing on 1920s Birmingham."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid modern elements."""
        try:
            negative_elements = self._get_random_choices("peaky_blinders.negative_prompts", 8)
            return ", ".join(negative_elements) + ", modern background, contemporary setting, current era architecture"
        except Exception as e:
            print(f"Warning: Error getting negative prompts: {str(e)}")
            return "modern elements, contemporary setting, current era architecture"

    def _enforce_1920s_theme(self, custom_text: str) -> str:
        """Ensure the custom text maintains 1920s theme."""
        if not custom_text:
            return ""
        if any(modern_term in custom_text.lower() for modern_term in ['computer', 'phone', 'digital', 'modern', 'future']):
            return f"((historical 1920s character inspired by {custom_text}))"
        return f"((1920s version of {custom_text}))"

    def _get_safe_random_choice(self, config_key: str, default: str) -> str:
        """Safely get a random choice with fallback."""
        try:
            return self._get_random_choice(config_key)
        except Exception as e:
            print(f"Warning: Error getting choice for {config_key}: {str(e)}")
            return default

    def _get_safe_random_choices(self, config_key: str, count: int, defaults: list) -> list:
        """Safely get multiple random choices with fallback."""
        try:
            return self._get_random_choices(config_key, count)
        except Exception as e:
            print(f"Warning: Error getting choices for {config_key}: {str(e)}")
            return defaults[:count]

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate historically accurate 1920s Peaky Blinders-themed components."""
        components = {}
        
        try:
            # Get custom inputs and enforce 1920s theme
            custom_subject = self._enforce_1920s_theme(custom_subject.strip())
            custom_location = custom_location.strip()
            
            # Select core elements with safe fallbacks
            character = self._get_safe_random_choice(
                "peaky_blinders.characters",
                "gangster"
            )
            clothing = self._get_safe_random_choices(
                "peaky_blinders.clothing",
                2,
                ["period appropriate clothing", "1920s attire"]
            )
            props = self._get_safe_random_choices(
                "peaky_blinders.period_props",
                2,
                ["pocket watch", "leather gloves"]
            )
            color_scheme = self._get_safe_random_choice(
                "peaky_blinders.color_schemes",
                "industrial tones"
            )
            period_elements = self._get_safe_random_choices(
                "peaky_blinders.period_elements",
                3,
                ["gas lamps", "cobblestone streets", "brick buildings"]
            )
            
            # Generate subject component
            if custom_subject:
                components["subject"] = (
                    f"{custom_subject}, "
                    f"((dressed in 1920s attire)), ((wearing {', '.join(clothing)})), "
                    f"((with {', '.join(props)})), ((in 1920s Birmingham setting)), "
                    f"((strictly period accurate details)), ((1920s style)), "
                    f"in tones of {color_scheme}, ((historical accuracy)), ((1920s era))"
                )
            else:
                components["subject"] = (
                    f"((1920s historical portrait)) of a ((Birmingham {character})), "
                    f"((wearing {', '.join(clothing)})), ((with {', '.join(props)})), "
                    f"((strictly period accurate details)), ((1920s Birmingham style)), "
                    f"in tones of {color_scheme}, ((historical accuracy)), ((1920s era))"
                )
            
            # Generate environment component
            if include_environment:
                if custom_location:
                    lighting = self._get_safe_random_choice(
                        "peaky_blinders.lighting",
                        "period lighting"
                    )
                    components["environment"] = (
                        f"in ((1920s {custom_location})), ((with {', '.join(period_elements)})), "
                        f"((illuminated by {lighting})), ((authentic historical setting)), "
                        f"((1920s industrial atmosphere)), ((Victorian era architecture)), "
                        f"((no modern elements)), ((period accurate Birmingham))"
                    )
                else:
                    setting = self._get_safe_random_choice(
                        "peaky_blinders.period_settings",
                        "industrial street"
                    )
                    lighting = self._get_safe_random_choice(
                        "peaky_blinders.lighting",
                        "period lighting"
                    )
                    components["environment"] = (
                        f"in ((a {setting})), ((with {', '.join(period_elements)})), "
                        f"((illuminated by {lighting})), ((authentic historical setting)), "
                        f"((1920s industrial atmosphere)), ((Victorian era architecture)), "
                        f"((no modern elements)), ((period accurate Birmingham))"
                    )
            
            # Generate style component
            if include_style:
                style = self._get_safe_random_choice(
                    "peaky_blinders.period_styles",
                    "1920s period"
                )
                mood = self._get_safe_random_choice(
                    "peaky_blinders.mood",
                    "industrial era"
                )
                components["style"] = (
                    f"((authentic {style})), ((1920s photography)), "
                    f"((strictly period accurate details)), (({mood} atmosphere)), "
                    f"((1920s documentary aesthetic)), ((vintage photo quality)), "
                    f"((historical drama)), ((period appropriate film grain)), "
                    f"((Victorian industrial era)), ((1920s Birmingham)), 8k resolution"
                )
            
            # Generate effects component
            if include_effects:
                components["effects"] = (
                    f"with ((1920s photo effects)), ((period appropriate film grain)), "
                    f"((historical color grading)), ((authentic aging)), "
                    f"((early photography style)), ((industrial atmosphere)), "
                    f"((coal smoke ambiance)), ((historical authenticity)), "
                    f"((no modern post-processing)), ((1920s photographic technique))"
                )
            
            return components
            
        except Exception as e:
            print(f"Warning: Error in Peaky Blinders handler: {str(e)}")
            # Return safe fallback components that maintain theme instead of going to abstract
            return {
                "subject": (
                    f"((1920s historical portrait)) of a ((Birmingham character)), "
                    f"((wearing period appropriate clothing)), ((with period props)), "
                    f"((strictly period accurate details)), ((1920s Birmingham style))"
                ),
                "environment": (
                    f"in ((a 1920s industrial setting)), ((with period elements)), "
                    f"((authentic historical setting)), ((Victorian era architecture))"
                ),
                "style": (
                    f"((1920s photography)), ((historical accuracy)), "
                    f"((vintage photo quality)), ((period appropriate film grain))"
                ),
                "effects": (
                    f"with ((1920s photo effects)), ((historical color grading)), "
                    f"((authentic aging)), ((period appropriate details))"
                )
            }
