import random
from .base_handler import BaseThemeHandler

class CulinaryThemeHandler(BaseThemeHandler):
    """Handler for culinary and food photography themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("culinary")

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and plating
        style = random.choice(self.theme_config.get("styles", []))
        plating = random.choice(self.theme_config.get("plating_techniques", []))
        
        # Food characteristics
        food_type = random.choice(self.theme_config.get("food_types", []))
        cuisine = random.choice(self.theme_config.get("cuisines", []))
        cooking = random.choice(self.theme_config.get("cooking_techniques", []))
        texture = random.choice(self.theme_config.get("textures", []))
        
        # Environment and props
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        prop = random.choice(self.theme_config.get("props", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmospheres", []))
        
        # Color and garnish
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        garnish = random.choice(self.theme_config.get("garnishes", []))
        
        # Build the prompt with enhanced weighting and emphasis
        prompt_parts = []
        
        # Add style and main subject with stronger emphasis
        if subject:
            prompt_parts.extend([
                f"((professional {style}, masterful food photography)) of {subject}",
                f"with ((exquisite {plating})), ((culinary art)), ((gourmet presentation))"
            ])
        else:
            prompt_parts.extend([
                f"((professional {style}, masterful food photography)) of (({cuisine} {food_type}))",
                f"((prepared using {cooking} technique))",
                f"with ((exquisite {plating})), ((culinary art)), ((gourmet presentation))"
            ])
        
        # Add texture and garnish with enhanced description
        prompt_parts.extend([
            f"featuring ((appetizing {texture} texture)), ((food styling))",
            f"beautifully garnished with (({garnish})), ((culinary detail))"
        ])
        
        # Add environment and props with professional emphasis
        prompt_parts.extend([
            f"in a ((professional {environment})), ((culinary setting))",
            f"styled with (({prop})), ((gourmet atmosphere))"
        ])
        
        # Add lighting and atmosphere with enhanced quality
        prompt_parts.extend([
            f"illuminated by ((perfect {lighting})), ((professional lighting))",
            f"creating a ((captivating {atmosphere} atmosphere)), ((restaurant quality))"
        ])
        
        # Add color scheme with artistic emphasis
        prompt_parts.append(f"in ((harmonious {color_scheme})), ((appetizing colors)), ((culinary aesthetics))")
        
        # Add technical quality emphasis
        prompt_parts.append("((8k resolution)), ((professional photography)), ((perfect composition))")
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "((blurry)), ((out of focus)), ((overexposed)), ((underexposed)), ((burnt food)), ((spoiled food)), ((messy plating)), ((dirty dishes)), ((poor lighting)), ((unappetizing)), ((artificial colors)), ((processed food)), ((low quality)), ((amateur)), ((bad composition)), ((dark shadows)), ((harsh lighting)), ((plastic looking)), ((oversaturated)), ((undersaturated))"
