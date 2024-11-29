from typing import Dict
from .base_handler import BaseThemeHandler

class NewYearsEveThemeHandler(BaseThemeHandler):
    """Handler for New Year's Eve-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "dark colors", "horror elements", "industrial settings", 
            "urban landscapes", "dull tones", "mundane imagery"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate New Year's Eve-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["party crowd", "celebratory group", "festive revelers", "elegant party-goers", "joyful people"]
        attire = ["party dress", "tuxedo", "sparkling outfit", "festive costume", "glamorous attire"]
        props = ["champagne glass", "party hat", "countdown clock", "fireworks", "celebration confetti"]
        color_schemes = ["gold and silver", "midnight blue", "glittering metallics", "festive rainbow", "elegant black and white"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((vibrant New Year's Eve scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((celebration atmosphere)), ((festive magic))"
            )
        else:
            components["subject"] = (
                f"((vibrant New Year's Eve scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((celebration atmosphere)), ((festive magic))"
            )
        
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for New Year's)), "
                    f"((celebration setting)), ((sparkling decorations)), "
                    f"((jubilant atmosphere)), ((New Year's Eve charm))"
                )
            else:
                settings = ["city square", "grand ballroom", "rooftop party", "elegant venue", "festive celebration space"]
                lighting = ["fireworks display", "city lights", "sparkling decorations", "midnight glow"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((celebration atmosphere)), ((New Year's Eve setting)), "
                    f"((festive landscape)), ((moment of transition))"
                )
        
        if include_style == "yes":
            components["style"] = (
                f"((celebratory New Year's artwork)), ((festive illustration style)), "
                f"((dynamic painting technique)), ((energetic composition)), "
                f"((festive color palette)), ((joyful holiday mood)), "
                f"((celebration card quality)), ((vibrant artistic rendering)), "
                f"8k resolution, ((magical celebration lighting))"
            )
        
        if include_effects == "yes":
            components["effects"] = (
                f"with ((magical celebration glow)), ((sparkling light)), "
                f"((floating confetti)), ((fireworks sparkle)), "
                f"((jubilant atmosphere)), ((festive magic)), "
                f"((countdown shimmer)), ((dynamic celebration effects))"
            )
        
        return components
