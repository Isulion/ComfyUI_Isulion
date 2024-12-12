from typing import Dict
from .base_handler import BaseThemeHandler

class ThanksgivingThemeHandler(BaseThemeHandler):
    """Handler for Thanksgiving-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "modern technology", "futuristic elements", "urban landscapes", 
            "cold colors", "industrial settings", "minimalist design"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Thanksgiving-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["family gathering", "warm family scene", "thanksgiving dinner group", "grateful people", "festive family"]
        attire = ["cozy sweater", "autumn dress", "warm clothing", "traditional outfit", "comfortable family attire"]
        props = ["roasted turkey", "pumpkin pie", "cornucopia", "autumn harvest basket", "thanksgiving feast"]
        color_schemes = ["warm autumn colors", "golden brown", "harvest palette", "rustic orange and red", "earthy tones"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((heartwarming Thanksgiving scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((gratitude atmosphere)), ((family magic))"
            )
        else:
            components["subject"] = (
                f"((heartwarming Thanksgiving scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((gratitude atmosphere)), ((family magic))"
            )
        
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((warm {custom_location})), ((decorated for Thanksgiving)), "
                    f"((family gathering setting)), ((autumn decorations)), "
                    f"((cozy atmosphere)), ((Thanksgiving charm))"
                )
            else:
                settings = ["family dining room", "rustic farmhouse", "autumn garden", "traditional home", "harvest celebration space"]
                lighting = ["warm fireplace glow", "soft autumn light", "golden hour", "gentle indoor lighting"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((family atmosphere)), ((Thanksgiving setting)), "
                    f"((autumn landscape)), ((moments of gratitude))"
                )
        
        if include_style == "yes":
            components["style"] = (
                f"((heartwarming Thanksgiving artwork)), ((family illustration style)), "
                f"((warm painting technique)), ((nostalgic composition)), "
                f"((autumn color palette)), ((grateful holiday mood)), "
                f"((family gathering quality)), ((tender artistic rendering)), "
                f"8k resolution, ((magical family lighting))"
            )
        
        if include_effects == "yes":
            components["effects"] = (
                f"with ((magical gratitude glow)), ((warm soft light)), "
                f"((falling autumn leaves)), ((feast sparkle)), "
                f"((cozy atmosphere)), ((family magic)), "
                f"((harvest shimmer)), ((tender family effects))"
            )
        
        return components
