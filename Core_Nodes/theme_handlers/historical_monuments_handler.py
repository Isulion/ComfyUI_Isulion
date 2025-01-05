from typing import Dict
from .base_handler import BaseThemeHandler

class HistoricalMonumentsHandler(BaseThemeHandler):
    """Handler for historical monuments theme generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        components = {}
        
        # Subject generation
        if custom_subject:
            components["subject"] = (
                f"((majestic {custom_subject})), "
                f"((architectural masterpiece)), ((monumental scale)), "
                f"((historical architecture)), ((grand structure)), "
                f"((landscape photography excellence)), ((perfect natural composition))"
            )
        else:
            monument = self._get_random_choice("historical_monuments.monuments")
            architectural_style = self._get_random_choice("historical_monuments.architectural_styles")
            components["subject"] = (
                f"((majestic {monument})), ((built in {architectural_style} style)), "
                f"((monumental scale)), ((historical architecture)), "
                f"((landscape photography excellence)), ((perfect natural composition))"
            )
            
        # Environment
        if include_environment == "yes":
            era = self._get_random_choice("historical_monuments.eras")
            setting = self._get_random_choice("historical_monuments.settings")
            cloud_formation = self._get_random_choice("historical_monuments.cloud_formations")
            components["environment"] = (
                f"in ((historic {setting})), during ((the {era})), "
                f"with ((subtle {cloud_formation})), ((environmental authenticity)), "
                f"((natural atmosphere)), ((environmental artistry))"
            )
            
        # Style
        if include_style == "yes":
            style = self._get_random_choice("historical_monuments.artistic_styles")
            technique = self._get_random_choice("historical_monuments.techniques")
            components["style"] = (
                f"((rendered in {style})), ((using {technique})), "
                f"((National Geographic style)), ((professional landscape photography)), "
                f"((award-winning landscape photograph)), ((8k resolution)), "
                f"((sharp details)), ((rich textures))"
            )
            
        # Effects
        if include_effects == "yes":
            lighting = self._get_random_choice("historical_monuments.lighting")
            atmosphere = self._get_random_choice("historical_monuments.atmosphere")
            components["effects"] = (
                f"with ((dramatic {lighting})), ((atmospheric {atmosphere})), "
                f"((natural water reflections)), ((natural color grading)), "
                f"((pristine conditions)), ((perfect exposure))"
            )
            
        return components
