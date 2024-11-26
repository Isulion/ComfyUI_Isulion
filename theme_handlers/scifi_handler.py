import random
from typing import Dict
from .base_handler import BaseThemeHandler

class SciFiThemeHandler(BaseThemeHandler):
    """Handler for sci-fi themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("scifi")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate sci-fi themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            tech = random.choice(self.theme_config.get("tech_elements", []))
            components["subject"] = (
                f"((futuristic {custom_subject})) with ((advanced {tech})), "
                f"((sci-fi aesthetic)), ((high-tech details)), "
                f"((cybernetic elements))"
            )
        else:
            subject = random.choice(self.theme_config.get("subjects", []))
            tech = random.choice(self.theme_config.get("tech_elements", []))
            action = random.choice(self.theme_config.get("actions", []))
            components["subject"] = (
                f"((ultra detailed {subject})) with ((advanced {tech})), "
                f"((dynamically {action})), ((futuristic design)), "
                f"((sci-fi aesthetic)), ((high-tech details))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})) with "
                    f"((advanced technology)), ((sci-fi atmosphere))"
                )
            else:
                setting = random.choice(self.theme_config.get("environments", []))
                atmosphere = random.choice(self.theme_config.get("atmospheres", []))
                lighting = random.choice(self.theme_config.get("lighting", []))
                components["environment"] = (
                    f"in ((detailed {setting})) with ((advanced technology)), "
                    f"((featuring {atmosphere} atmosphere)), "
                    f"((dramatic {lighting} lighting))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = random.choice(self.theme_config.get("styles", []))
            tech_detail = random.choice(self.theme_config.get("tech_details", []))
            components["style"] = (
                f"((professional {style})), ((sci-fi art)), "
                f"((featuring {tech_detail})), "
                f"((ultra detailed)), ((cinematic quality)), "
                f"((perfect composition)), 8k resolution"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = random.choice(self.theme_config.get("effects", []))
            tech_effect = random.choice(self.theme_config.get("tech_effects", []))
            components["effects"] = (
                f"with ((advanced {effect})), ((high-tech {tech_effect})), "
                f"((futuristic glow)), ((technological precision)), "
                f"((sci-fi finish))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and tech elements
        style = random.choice(self.theme_config.get("styles", []))
        tech = random.choice(self.theme_config.get("tech_elements", []))
        
        # Vehicle and equipment
        vehicle = random.choice(self.theme_config.get("vehicles", []))
        equipment = random.choice(self.theme_config.get("equipment", []))
        
        # Environment and architecture
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmospheres", []))
        
        # Weather and color
        weather = random.choice(self.theme_config.get("weather_effects", []))
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        
        # Time period
        time_period = random.choice(self.theme_config.get("time_periods", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and tech elements
        prompt_parts.extend([style, f"with {tech}"])
        
        # Add subject with sci-fi context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"futuristic {subject}",
                    f"equipped with {equipment}"
                ])
            else:
                prompt_parts.extend([
                    f"advanced {subject}",
                    f"enhanced with {tech}"
                ])
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in a {environment}",
            f"featuring {architecture}"
        ])
        
        # Add vehicle and equipment
        prompt_parts.extend([
            f"with {vehicle} nearby",
            f"utilizing {equipment}"
        ])
        
        # Add atmosphere and weather
        prompt_parts.extend([
            f"in {atmosphere}",
            f"during {weather}"
        ])
        
        # Add lighting and color
        prompt_parts.extend([
            f"illuminated by {lighting}",
            f"in {color_scheme}"
        ])
        
        # Add time period
        prompt_parts.append(f"during the {time_period}")
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "medieval, fantasy elements, natural landscapes, organic materials, primitive technology, ancient artifacts, rustic settings, historical elements, traditional clothing, magical effects"
