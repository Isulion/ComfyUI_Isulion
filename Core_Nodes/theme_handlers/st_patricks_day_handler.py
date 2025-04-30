from typing import Dict
from .base_handler import BaseThemeHandler

class StPatricksDayThemeHandler(BaseThemeHandler):
    """Handler for St. Patrick's Day-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "dark colors", "horror elements", "industrial settings", 
            "urban landscapes", "non-green tones", "serious imagery"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate St. Patrick's Day-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["leprechaun", "Irish dancer", "festive party-goer", "Celtic figure", "joyful Irish character"]
        attire = ["green outfit", "shamrock accessories", "traditional Irish clothing", "festive costume", "Celtic-inspired attire"]
        props = ["shamrock", "pot of gold", "Irish flag", "Celtic ornament", "lucky charm"]
        color_schemes = ["emerald green", "Irish green", "green and gold", "Celtic palette", "lucky green"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((festive St. Patrick's Day scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((celebration atmosphere)), ((Irish magic))"
            )
        else:
            components["subject"] = (
                f"((festive St. Patrick's Day scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((celebration atmosphere)), ((Irish magic))"
            )
        
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for St. Patrick's Day)), "
                    f"((Irish celebration setting)), ((green decorations)), "
                    f"((jubilant atmosphere)), ((St. Patrick's Day charm))"
                )
            else:
                settings = ["Irish pub", "city parade", "Celtic landscape", "festival ground", "traditional Irish setting"]
                lighting = ["green party lights", "festive illumination", "emerald glow", "celebration lighting"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((celebration atmosphere)), ((St. Patrick's Day setting)), "
                    f"((Irish landscape)), ((moment of joy))"
                )
        
        if include_style:
            components["style"] = (
                f"((celebratory St. Patrick's Day artwork)), ((Irish illustration style)), "
                f"((festive painting technique)), ((energetic composition)), "
                f"((green color palette)), ((joyful holiday mood)), "
                f"((celebration card quality)), ((vibrant artistic rendering)), "
                f"8k resolution, ((magical celebration lighting))"
            )
        
        if include_effects:
            components["effects"] = (
                f"with ((magical celebration glow)), ((emerald light)), "
                f"((floating shamrock)), ((lucky sparkle)), "
                f"((jubilant atmosphere)), ((Irish magic)), "
                f"((Celtic shimmer)), ((dynamic celebration effects))"
            )
        
        return components
