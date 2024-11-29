from typing import Dict
from .base_handler import BaseThemeHandler

class DiaDeLosmuertosThemeHandler(BaseThemeHandler):
    """Handler for Dia de los Muertos-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "realistic human anatomy", "modern technology", "clinical settings", 
            "cold colors", "minimalist design", "non-traditional imagery"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Dia de los Muertos-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["sugar skull figure", "calavera dancer", "traditional Mexican character", "festive skeleton", "cultural celebrant"]
        attire = ["traditional Mexican dress", "skull makeup", "colorful costume", "embroidered outfit", "festive cultural attire"]
        props = ["marigold flowers", "candle offering", "papel picado", "traditional altar items", "cultural remembrance objects"]
        color_schemes = ["vibrant Mexican colors", "skull palette", "marigold and red", "cultural color mix", "festive multicolor"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((vibrant Dia de los Muertos scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((cultural celebration)), ((spiritual magic))"
            )
        else:
            components["subject"] = (
                f"((vibrant Dia de los Muertos scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((cultural celebration)), ((spiritual magic))"
            )
        
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for Dia de los Muertos)), "
                    f"((cultural celebration setting)), ((traditional decorations)), "
                    f"((spiritual atmosphere)), ((cultural charm))"
                )
            else:
                settings = ["traditional cemetery", "Mexican plaza", "family altar", "cultural celebration space", "traditional home"]
                lighting = ["candlelight", "soft cultural illumination", "warm cultural glow", "spiritual lighting"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((cultural atmosphere)), ((Dia de los Muertos setting)), "
                    f"((Mexican landscape)), ((moments of remembrance))"
                )
        
        if include_style == "yes":
            components["style"] = (
                f"((celebratory Dia de los Muertos artwork)), ((Mexican illustration style)), "
                f"((traditional painting technique)), ((cultural composition)), "
                f"((vibrant color palette)), ((spiritual holiday mood)), "
                f"((cultural celebration quality)), ((artistic cultural rendering)), "
                f"8k resolution, ((magical cultural lighting))"
            )
        
        if include_effects == "yes":
            components["effects"] = (
                f"with ((magical spiritual glow)), ((warm cultural light)), "
                f"((floating marigold petals)), ((cultural sparkle)), "
                f"((spiritual atmosphere)), ((cultural magic)), "
                f"((remembrance shimmer)), ((dynamic cultural effects))"
            )
        
        return components
