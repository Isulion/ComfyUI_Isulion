import random
from .base_handler import BaseThemeHandler

class DreamWorksThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("dreamworks")

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and character features
        style = random.choice(self.theme_config.get("styles", []))
        character_feature = random.choice(self.theme_config.get("character_features", []))
        
        # Visual effects and props
        effect = random.choice(self.theme_config.get("visual_effects", []))
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
        
        # Add subject with DreamWorks context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} as a {character_type}",
                    f"with {character_feature}"
                ])
            else:
                prompt_parts.extend([
                    f"epic {subject}",
                    f"enhanced with {effect}"
                ])
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in an {environment}",
            f"featuring {architecture}"
        ])
        
        # Add props and lighting
        prompt_parts.extend([
            f"with {prop}",
            f"illuminated by {lighting}"
        ])
        
        # Add atmosphere and emotion
        prompt_parts.extend([
            f"in an {atmosphere}",
            f"creating a {emotional_tone} feeling"
        ])
        
        # Add visual effects and color scheme
        prompt_parts.extend([
            f"with {effect}",
            f"in {color_scheme}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "anime, hand-drawn, 2D animation, sketchy, traditional animation, low quality, basic rendering, flat colors, simple lighting, undetailed, amateur animation"
