from typing import Dict
from .base_handler import BaseThemeHandler

class EasterThemeHandler(BaseThemeHandler):
    """Handler for Easter-themed prompt generation."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "dark colors", "gothic style", "horror elements", 
            "industrial settings", "urban landscapes", "modern technology"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Easter-themed components."""
        components = {}
        
        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select core elements
        characters = ["cute bunny", "baby chick", "spring lamb", "colorful butterfly", "baby farm animal"]
        attire = ["pastel bow", "flower crown", "spring dress", "soft ribbon", "delicate accessories"]
        props = ["decorated Easter egg", "basket of eggs", "spring flowers", "colorful ribbons", "chocolate treats"]
        color_schemes = ["pastel", "soft spring colors", "Easter egg palette", "light and airy", "gentle rainbow"]
        
        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)
        
        if custom_subject:
            components["subject"] = (
                f"((adorable Easter scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((spring spirit)), ((Easter magic))"
            )
        else:
            components["subject"] = (
                f"((adorable Easter scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((spring spirit)), ((Easter magic))"
            )
        
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((festive {custom_location})), ((decorated for Easter)), "
                    f"((spring garden setting)), ((blooming flowers)), "
                    f"((soft pastel atmosphere)), ((Easter charm))"
                )
            else:
                settings = ["flower meadow", "spring garden", "blooming orchard", "countryside field", "pastoral landscape"]
                lighting = ["soft morning light", "golden hour", "gentle spring sunlight", "diffused daylight"]
                
                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)
                
                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((spring blossoms)), ((Easter atmosphere)), "
                    f"((colorful spring landscape)), ((renewal of life))"
                )
        
        if include_style:
            components["style"] = (
                f"((whimsical Easter artwork)), ((spring illustration style)), "
                f"((soft watercolor technique)), ((delicate painting)), "
                f"((pastel color palette)), ((cheerful holiday mood)), "
                f"((Easter card quality)), ((gentle artistic rendering)), "
                f"8k resolution, ((magical spring lighting))"
            )
        
        if include_effects:
            components["effects"] = (
                f"with ((magical spring glow)), ((soft pastel light)), "
                f"((floating spring petals)), ((gentle egg sparkle)), "
                f"((warm Easter atmosphere)), ((spring magic)), "
                f"((Easter egg shimmer)), ((delicate nature effects))"
            )
        
        return components
