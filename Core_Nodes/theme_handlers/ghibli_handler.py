import random
from typing import Dict
from .base_handler import BaseThemeHandler

class GhibliThemeHandler(BaseThemeHandler):
    """Handler for Studio Ghibli-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("ghibli")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Studio Ghibli-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        emotion = self._get_random_choice("ghibli.emotions")
        action = self._get_random_choice("ghibli.actions")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((Studio Ghibli style {custom_subject})), "
                f"((showing {emotion})), ((dynamically {action})), "
                f"((whimsical character design)), "
                f"((gentle expression)), ((charming details)), "
                f"((Miyazaki inspired))"
            )
        else:
            character = self._get_random_choice("ghibli.characters")
            emotion = self._get_random_choice("ghibli.emotions")
            action = self._get_random_choice("ghibli.actions")
            components["subject"] = (
                f"((Studio Ghibli style {character})), "
                f"((showing {emotion})), ((dynamically {action})), "
                f"((whimsical character design)), "
                f"((gentle expression)), ((Miyazaki inspired))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((magical Ghibli-style {custom_location})), "
                    f"((soft lighting)), ((enchanted atmosphere)), "
                    f"((stunning background detail))"
                )
            else:
                location = self._get_random_choice("ghibli.locations")
                time = self._get_random_choice("ghibli.times")
                nature = self._get_random_choice("ghibli.nature_elements")
                components["environment"] = (
                    f"in ((magical Ghibli-style {location})), "
                    f"((during {time})), ((with {nature})), "
                    f"((soft lighting)), ((enchanted atmosphere)), "
                    f"((stunning background detail))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("ghibli.styles")
            technique = self._get_random_choice("ghibli.techniques")
            components["style"] = (
                f"((Studio Ghibli art style)), ((featuring {style})), "
                f"((with {technique})), ((hand-drawn quality)), "
                f"((perfect color palette)), ((masterful composition)), "
                f"((traditional animation)), 8k resolution"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("ghibli.effects")
            detail = self._get_random_choice("ghibli.magical_elements")
            components["effects"] = (
                f"with ((magical {effect})), ((enchanted {detail})), "
                f"((gentle glow)), ((natural elements)), "
                f"((Ghibli magic)), ((whimsical atmosphere))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and character traits
        style = random.choice(self.theme_config.get("styles", []))
        trait = random.choice(self.theme_config.get("character_traits", []))
        
        # Environment and natural elements
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        nature = random.choice(self.theme_config.get("natural_elements", []))
        
        # Magical and architectural elements
        magic = random.choice(self.theme_config.get("magical_elements", []))
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        weather = random.choice(self.theme_config.get("weather_effects", []))
        
        # Color and time
        color_palette = random.choice(self.theme_config.get("color_palettes", []))
        time_period = random.choice(self.theme_config.get("time_periods", []))
        
        # Emotional tone
        emotion = random.choice(self.theme_config.get("emotional_tones", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and character traits
        prompt_parts.extend([style, f"with {trait}"])
        
        # Add subject with appropriate context
        if subject:
            if any(word in subject.lower() for word in ["person", "girl", "boy", "child", "character"]):
                prompt_parts.append(f"{subject} with {trait}")
            else:
                prompt_parts.append(f"magical {subject}")
        
        # Add environment and nature
        prompt_parts.extend([
            f"in a {environment}",
            f"with {nature}"
        ])
        
        # Add magical and architectural elements
        prompt_parts.extend([
            f"featuring {magic}",
            f"near {architecture}"
        ])
        
        # Add atmosphere and lighting
        prompt_parts.extend([
            f"in {lighting}",
            f"with {weather}"
        ])
        
        # Add color and time
        prompt_parts.extend([
            f"in {color_palette}",
            f"during {time_period}"
        ])
        
        # Add emotional tone
        prompt_parts.append(f"expressing {emotion}")
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "photorealistic, modern technology, urban setting, dark themes, violence, harsh lighting, sharp edges, digital effects, hyperrealistic, gritty details"
