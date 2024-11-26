from typing import Dict
from .base_handler import BaseThemeHandler
import random

class ChristmasThemeHandler(BaseThemeHandler):
    """Handler for Christmas-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Christmas theme components."""
        components = {}
        
        # Get custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Select random elements
        character = random.choice(self.christmas_elements["characters"])
        food = random.choice(self.christmas_elements["foods"])
        decoration = random.choice(self.christmas_elements["decorations"])
        
        components["subject"] = (
            f"((festive Christmas scene)) of {custom_subject if custom_subject else f'((cheerful {character}))'}, "
            f"((enjoying {food})), ((surrounded by {decoration})), "
            f"((holiday spirit)), ((magical atmosphere))"
        )
        
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((magical {custom_location})) with ((festive atmosphere)), "
                    f"((Christmas magic)), ((holiday warmth))"
                )
            else:
                setting = random.choice(self.christmas_elements["settings"])
                weather = random.choice(self.christmas_elements["weather"])
                components["environment"] = (
                    f"in a ((magical {setting})) during {weather}, "
                    f"((holiday atmosphere)), ((winter wonderland))"
                )
        
        if include_style == "yes":
            style = random.choice(self.christmas_styles)
            components["style"] = (
                f"((Christmas themed {style})), ((festive mood)), "
                f"((holiday colors)), ((seasonal charm)), "
                f"((traditional Christmas)), ((winter magic)), "
                f"((perfect composition)), 8k resolution"
            )
        
        if include_effects == "yes":
            mood = random.choice(self.christmas_moods)
            components["effects"] = (
                f"with ((soft winter glow)), ((magical sparkles)), "
                f"((holiday lighting)), ((warm atmosphere)), "
                f"(({mood} mood)), ((seasonal effects)), "
                f"((Christmas spirit)), ((festive ambiance))"
            )
        
        return components
