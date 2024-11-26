import random
from typing import Dict
from .base_handler import BaseThemeHandler

class ImpressionistThemeHandler(BaseThemeHandler):
    """Handler for impressionist-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("impressionist")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate impressionist-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((impressionist {custom_subject})), "
                f"((painterly style)), ((artistic interpretation)), "
                f"((light and color))"
            )
        else:
            subject_type = random.choice(self.theme_config.get("subjects", []))
            color = random.choice(self.theme_config.get("colors", []))
            technique = random.choice(self.theme_config.get("techniques", []))
            components["subject"] = (
                f"(({color} {subject_type})), "
                f"((painted with {technique})), "
                f"((impressionist style)), ((artistic interpretation))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((impressionist {custom_location})) with "
                    f"((painterly setting)), ((artistic environment))"
                )
            else:
                scene_location = random.choice(self.theme_config.get("locations", []))
                lighting = random.choice(self.theme_config.get("lighting", []))
                atmosphere = random.choice(self.theme_config.get("atmospheres", []))
                components["environment"] = (
                    f"in (({scene_location})) with (({lighting})), "
                    f"((creating {atmosphere} atmosphere)), "
                    f"((impressionist scene)), ((artistic vista))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = random.choice(self.theme_config.get("styles", []))
            components["style"] = (
                f"((styled in {style})), "
                f"((impressionist aesthetic)), "
                f"((painterly beauty)), ((artistic design)), "
                f"((light and color mastery))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = random.choice(self.theme_config.get("effects", []))
            components["effects"] = (
                f"with (({effect})), "
                f"((impressionist atmosphere)), "
                f"((artistic ambiance)), ((painterly environment))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and artist influence
        style = random.choice(self.theme_config.get("styles", []))
        artist = random.choice(self.theme_config.get("artists", []))
        
        # Technique and color
        technique = random.choice(self.theme_config.get("techniques", []))
        color_palette = random.choice(self.theme_config.get("color_palettes", []))
        
        # Scene and location
        subject_type = random.choice(self.theme_config.get("subjects", [])) if not subject else subject
        scene_location = random.choice(self.theme_config.get("locations", [])) if not location else location
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmospheres", []))
        weather = random.choice(self.theme_config.get("weather_effects", []))
        
        # Time period
        time_period = random.choice(self.theme_config.get("time_periods", []))

        # Build the prompt
        prompt_parts = []
        
        # Add style and artist influence
        prompt_parts.extend([style, artist])
        
        # Add technique and color
        prompt_parts.extend([technique, color_palette])
        
        # Add subject and location
        if subject:
            prompt_parts.append(f"{subject} in impressionist style")
        else:
            prompt_parts.append(subject_type)
            
        prompt_parts.append(f"in a {scene_location}")
        
        # Add lighting and atmosphere
        prompt_parts.extend([
            f"with {lighting}",
            f"during {atmosphere}",
            f"featuring {weather}"
        ])
        
        # Add time period
        prompt_parts.append(f"set in {time_period}")
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "sharp details, photorealistic, digital art, modern style, harsh lines, perfect edges, high contrast, cartoon style, anime, manga, contemporary setting"
