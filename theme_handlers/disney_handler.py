import random
from .base_handler import BaseThemeHandler

class DisneyThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("disney")

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and character features
        style = random.choice(self.theme_config.get("styles", []))
        character_feature = random.choice(self.theme_config.get("character_features", []))
        
        # Magical elements and props
        magic = random.choice(self.theme_config.get("magical_elements", []))
        prop = random.choice(self.theme_config.get("props", []))
        
        # Environment and architecture
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmospheres", []))
        
        # Color and emotion
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        emotional_tone = random.choice(self.theme_config.get("emotional_tones", []))
        
        # Animation effect and character type
        animation_effect = random.choice(self.theme_config.get("animation_effects", []))
        character_type = random.choice(self.theme_config.get("character_types", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and animation effect
        prompt_parts.extend([style, f"with {animation_effect}"])
        
        # Add subject with Disney context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} as a {character_type}",
                    f"with {character_feature}"
                ])
            else:
                prompt_parts.extend([
                    f"enchanted {subject}",
                    f"blessed with {magic}"
                ])
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in a {environment}",
            f"with {architecture}"
        ])
        
        # Add props and lighting
        prompt_parts.extend([
            f"featuring {prop}",
            f"illuminated by {lighting}"
        ])
        
        # Add atmosphere and emotion
        prompt_parts.extend([
            f"with {atmosphere}",
            f"creating a {emotional_tone} feeling"
        ])
        
        # Add magical elements and color scheme
        prompt_parts.extend([
            f"enhanced by {magic}",
            f"in {color_scheme}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "realistic, photorealistic, photograph, modern, contemporary, dark themes, horror, violence, scary elements, adult themes, complex textures, gritty, hyper-detailed"
