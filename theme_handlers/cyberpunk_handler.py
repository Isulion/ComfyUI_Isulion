import random
from typing import Dict
from .base_handler import BaseThemeHandler

class CyberpunkThemeHandler(BaseThemeHandler):
    """Handler for cyberpunk-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("cyberpunk")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate cyberpunk-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            tech = random.choice(self.theme_config.get("tech_elements", []))
            components["subject"] = (
                f"((cyberpunk {custom_subject})) with ((advanced {tech})), "
                f"((neo-futuristic design)), ((cyber-enhanced)), "
                f"((neon-lit details)), ((high-tech aesthetics))"
            )
        else:
            character = random.choice(self.theme_config.get("characters", []))
            tech = random.choice(self.theme_config.get("tech_elements", []))
            style = random.choice(self.theme_config.get("character_styles", []))
            components["subject"] = (
                f"((cyberpunk {character})) with ((advanced {tech})), "
                f"((featuring {style})), ((neo-futuristic design)), "
                f"((cyber-enhanced)), ((neon-lit details))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((neon-lit {custom_location})), "
                    f"((cyberpunk atmosphere)), ((high-tech surroundings)), "
                    f"((dystopian elements))"
                )
            else:
                location = random.choice(self.theme_config.get("locations", []))
                time = random.choice(self.theme_config.get("times", []))
                atmosphere = random.choice(self.theme_config.get("atmospheres", []))
                components["environment"] = (
                    f"in ((neon-lit {location})), "
                    f"((during {time})), ((with {atmosphere} atmosphere)), "
                    f"((cyberpunk world)), ((dystopian future))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = random.choice(self.theme_config.get("styles", []))
            detail = random.choice(self.theme_config.get("details", []))
            components["style"] = (
                f"((cyberpunk art style)), ((featuring {style})), "
                f"((with {detail})), ((neo-noir aesthetics)), "
                f"((perfect composition)), ((neon lighting)), "
                f"((high contrast)), 8k resolution"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = random.choice(self.theme_config.get("effects", []))
            tech_effect = random.choice(self.theme_config.get("tech_effects", []))
            components["effects"] = (
                f"with ((cyberpunk {effect})), ((high-tech {tech_effect})), "
                f"((neon glow)), ((cyber elements)), "
                f"((digital distortion)), ((tech interference))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and tech elements
        style = random.choice(self.theme_config.get("styles", []))
        tech = random.choice(self.theme_config.get("tech_elements", []))
        
        # Clothing and accessories if subject is a character
        clothing = random.choice(self.theme_config.get("clothing", []))
        accessory = random.choice(self.theme_config.get("accessories", []))
        
        # Environment and tech devices
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        device = random.choice(self.theme_config.get("tech_devices", []))
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmosphere", []))
        weather = random.choice(self.theme_config.get("weather_effects", []))
        
        # Time and color
        time_period = random.choice(self.theme_config.get("time_periods", []))
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and tech elements
        prompt_parts.extend([style, f"with {tech}"])
        
        # Add subject with clothing and accessories if it's a character
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} wearing {clothing}",
                    f"equipped with {accessory}"
                ])
            else:
                prompt_parts.append(f"high-tech {subject}")
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in a {environment}",
            f"surrounded by {architecture}",
            f"featuring {device}"
        ])
        
        # Add atmosphere and weather
        prompt_parts.extend([
            f"illuminated by {lighting}",
            f"with {atmosphere}",
            f"during {weather}"
        ])
        
        # Add time and color
        prompt_parts.extend([
            f"set in {time_period}",
            f"in {color_scheme} colors"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "natural environment, historical setting, vintage style, organic materials, rustic elements, pastoral scenes, traditional clothing, classical architecture, earthy colors, daylight"
