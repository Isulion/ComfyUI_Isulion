from typing import Dict
from .base_handler import BaseThemeHandler

class ChineseNewYearThemeHandler(BaseThemeHandler):
    """Handler for Chinese New Year-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "western style", "non-Asian cultural elements", "modern technology", 
            "industrial settings", "cold colors", "minimalist design"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Chinese New Year-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["traditional Chinese figure", "festive dragon dancer", "cultural celebrant", "zodiac animal", "family gathering"]
        attire = ["traditional Chinese dress", "red festival clothing", "cultural costume", "silk outfit", "festive cultural attire"]
        props = ["red lantern", "Chinese zodiac symbol", "traditional decoration", "lucky red envelope", "cultural celebration item"]
        color_schemes = ["traditional red and gold", "Chinese festival colors", "auspicious red palette", "cultural color mix", "festive golden red"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((vibrant Chinese New Year scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((cultural celebration)), ((festive magic))"
            )
        else:
            components["subject"] = (
                f"((vibrant Chinese New Year scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((cultural celebration)), ((festive magic))"
            )
        
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for Chinese New Year)), "
                    f"((cultural celebration setting)), ((traditional decorations)), "
                    f"((jubilant atmosphere)), ((cultural charm))"
                )
            else:
                settings = ["traditional Chinese street", "festival ground", "family home", "cultural celebration space", "traditional temple"]
                lighting = ["red lantern glow", "festive illumination", "traditional cultural lighting", "warm celebration light"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((cultural atmosphere)), ((Chinese New Year setting)), "
                    f"((traditional landscape)), ((moment of renewal))"
                )
        
        if include_style:
            components["style"] = (
                f"((celebratory Chinese New Year artwork)), ((traditional Chinese illustration style)), "
                f"((cultural painting technique)), ((festive composition)), "
                f"((auspicious color palette)), ((joyful holiday mood)), "
                f"((cultural celebration quality)), ((artistic cultural rendering)), "
                f"8k resolution, ((magical cultural lighting))"
            )
        
        if include_effects:
            components["effects"] = (
                f"with ((magical festive glow)), ((warm cultural light)), "
                f"((floating red lanterns)), ((cultural sparkle)), "
                f"((jubilant atmosphere)), ((festive magic)), "
                f"((zodiac shimmer)), ((dynamic cultural effects))"
            )
        
        return components
