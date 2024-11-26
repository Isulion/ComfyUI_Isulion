import random
from .base_handler import BaseThemeHandler

class StopMotionThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("stopmotion")

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and material textures
        style = random.choice(self.theme_config.get("styles", []))
        texture = random.choice(self.theme_config.get("material_textures", []))
        
        # Character features and props
        character_feature = random.choice(self.theme_config.get("character_features", []))
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
        
        # Add subject with stop-motion context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} as a {character_type}",
                    f"with {character_feature}"
                ])
            else:
                prompt_parts.extend([
                    f"handcrafted {subject}",
                    f"with {texture}"
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
        
        # Add material texture and color scheme
        prompt_parts.extend([
            f"showing {texture}",
            f"in {color_scheme}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "smooth 3D, CGI, digital animation, realistic textures, photorealistic, modern rendering, perfect surfaces, high detail, sharp edges, digital effects"
