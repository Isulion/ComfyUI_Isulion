import random
from typing import Dict
from .base_handler import BaseThemeHandler

class VintageAnthropomorphicThemeHandler(BaseThemeHandler):
    """Handler for vintage anthropomorphic-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("vintage_anthropomorphic")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate vintage anthropomorphic-themed components."""
        components = {}

        # Always use random elements, even with custom_subject
        character = self._get_random_choice("vintage_anthropomorphic.characters")
        species = self._get_random_choice("vintage_anthropomorphic.species")
        clothing = self._get_random_choice("vintage_anthropomorphic.clothing")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((vintage anthropomorphic {custom_subject})), "
                f"((wearing {clothing})), "
                f"((dressed animal)), ((period style)), "
                f"((classic character))"
            )
        else:
            components["subject"] = (
                f"((vintage {character} {species})), "
                f"((wearing {clothing})), "
                f"((dressed animal)), ((period style))"
            )

        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((vintage {custom_location})) with "
                    f"((period setting)), ((classic environment))"
                )
            else:
                setting = self._get_random_choice("vintage_anthropomorphic.settings")
                activity = self._get_random_choice("vintage_anthropomorphic.activities")
                prop = self._get_random_choice("vintage_anthropomorphic.props")
                components["environment"] = (
                    f"in (({setting})) during (({activity})), "
                    f"((with {prop})), "
                    f"((vintage scene)), ((period setting))"
                )

        # Generate style if requested
        if include_style == "yes":
            atmosphere = self._get_random_choice("vintage_anthropomorphic.atmospheres")
            components["style"] = (
                f"((styled as {atmosphere})), "
                f"((vintage aesthetic)), "
                f"((period design)), ((classic look)), "
                f"((antique authenticity))"
            )

        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("vintage_anthropomorphic.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((vintage atmosphere)), "
                f"((period ambiance)), ((classic environment))"
            )

        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and art technique
        style = random.choice(self.theme_config.get("styles", []))
        art_technique = random.choice(self.theme_config.get("art_techniques", []))
        
        # Character elements
        characteristic = random.choice(self.theme_config.get("characteristics", []))
        clothing = random.choice(self.theme_config.get("clothing_styles", []))
        
        # Environment and setting
        scene = random.choice(self.theme_config.get("scene_settings", [])) if not location else location
        environment = random.choice(self.theme_config.get("environments", []))
        time_period = random.choice(self.theme_config.get("time_periods", []))
        
        # Additional details
        prop = random.choice(self.theme_config.get("props", []))
        mood = random.choice(self.theme_config.get("moods", []))
        color_palette = random.choice(self.theme_config.get("color_palettes", []))

        # Build the prompt
        prompt_parts = []
        
        # Add style and art technique
        prompt_parts.extend([style, art_technique])
        
        # Add subject with characteristics if provided
        if subject:
            prompt_parts.extend([
                f"{subject} as an anthropomorphic character",
                f"wearing {clothing}",
                characteristic
            ])
        
        # Add environment and setting details
        prompt_parts.extend([
            f"in a {scene}",
            environment,
            f"set in {time_period}"
        ])
        
        # Add props and atmosphere
        prompt_parts.extend([
            f"with {prop}",
            mood,
            color_palette
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "modern style, contemporary, digital art, 3D rendering, photorealistic, harsh colors, sloppy linework, poor composition, anime style, manga style, inappropriate clothing, out of period elements"
