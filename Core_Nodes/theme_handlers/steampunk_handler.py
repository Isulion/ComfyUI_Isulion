from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("steampunk")
class SteampunkThemeHandler(BaseThemeHandler):
    """Handler for steampunk-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("steampunk")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate steampunk-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            prompt = self.generate_theme_prompt(subject=custom_subject)
            components["subject"] = prompt
        else:
            character = self._get_random_choice("steampunk.characters")
            prompt = self.generate_theme_prompt(subject=character)
            components["subject"] = prompt
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                prompt = self.generate_theme_prompt(location=custom_location)
                components["environment"] = prompt
            else:
                location = self._get_random_choice("steampunk.locations")
                prompt = self.generate_theme_prompt(location=location)
                components["environment"] = prompt
        
        # Generate style if requested
        if include_style:
            style = self.generate_theme_prompt()
            components["style"] = style
        
        # Generate effects if requested
        if include_effects:
            effects = self.generate_theme_prompt()
            components["effects"] = effects
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and materials
        style = self.rng.choice(self.theme_config.get("styles", []))
        material = self.rng.choice(self.theme_config.get("materials", []))
        
        # Mechanical and decorative elements
        mechanical = self.rng.choice(self.theme_config.get("mechanical_elements", []))
        decorative = self.rng.choice(self.theme_config.get("decorative_elements", []))
        
        # Clothing and accessories if subject is a character
        clothing = self.rng.choice(self.theme_config.get("clothing", []))
        accessory = self.rng.choice(self.theme_config.get("accessories", []))
        
        # Environment and machines
        environment = self.rng.choice(self.theme_config.get("environments", [])) if not location else location
        machine = self.rng.choice(self.theme_config.get("machines", []))
        
        # Lighting and atmosphere
        lighting = self.rng.choice(self.theme_config.get("lighting", []))
        atmosphere = self.rng.choice(self.theme_config.get("atmosphere", []))
        
        # Color scheme
        color_scheme = self.rng.choice(self.theme_config.get("color_schemes", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and material
        prompt_parts.extend([style, f"made of {material}"])
        
        # Add subject with mechanical and decorative elements
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} wearing {clothing}",
                    f"adorned with {accessory}"
                ])
            else:
                prompt_parts.append(f"{subject} decorated with {decorative}")
        
        # Add mechanical elements
        prompt_parts.extend([
            f"featuring {mechanical}",
            f"with {decorative} details"
        ])
        
        # Add environment and machinery
        prompt_parts.extend([
            f"in a {environment}",
            f"with {machine} in scene"
        ])
        
        # Add atmosphere and lighting
        prompt_parts.extend([
            f"illuminated by {lighting}",
            f"in a {atmosphere}"
        ])
        
        # Add color scheme
        prompt_parts.append(f"in {color_scheme} color scheme")
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "modern technology, plastic, contemporary setting, minimalist, clean lines, digital displays, modern materials, simplistic design, plain surfaces, futuristic elements"
