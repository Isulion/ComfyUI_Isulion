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
        
        # Subject generation with enhanced historical context
        if custom_subject:
            components["subject"] = (
                f"((majestic {custom_subject})), "
                f"((architectural masterpiece at its peak)), ((monumental scale)), "
                f"((historical grandeur)), ((architectural excellence)), "
                f"((original appearance)), ((perfect condition))"
            )
        else:
            monument = self._get_random_choice("historical_monuments.monuments")
            architectural_style = self._get_random_choice("historical_monuments.architectural_styles")
            historical_period = self._get_random_choice("historical_monuments.historical_periods")
            civilization = self._get_random_choice("historical_monuments.civilizations")
            
            components["subject"] = (
                f"((majestic {monument})), ((at its greatest splendor)), "
                f"((built in authentic {architectural_style} style)), "
                f"((during the height of {civilization} civilization)), "
                f"((in {historical_period})), ((perfectly preserved)), "
                f"((architectural magnificence)), ((original appearance))"
            )
            
        # Enhanced historical environment
        if include_environment == "yes":
            era = self._get_random_choice("historical_monuments.eras")
            setting = self._get_random_choice("historical_monuments.settings")
            activity = self._get_random_choice("historical_monuments.historical_activities")
            components["environment"] = (
                f"in ((historically accurate {setting})), during ((the {era})), "
                f"with ((period-authentic {activity})), ((historical accuracy)), "
                f"((bustling with period-appropriate life)), "
                f"((rich historical context)), ((cultural significance))"
            )
            
        # Enhanced artistic style
        if include_style == "yes":
            style = self._get_random_choice("historical_monuments.artistic_styles")
            technique = self._get_random_choice("historical_monuments.techniques")
            components["style"] = (
                f"((rendered in {style})), ((using {technique})), "
                f"((masterful architectural photography)), ((historical documentation quality)), "
                f"((supreme architectural detail)), ((perfect scale representation)), "
                f"((professional historical record)), ((8k resolution))"
            )
            
        # Enhanced atmospheric effects
        if include_effects == "yes":
            lighting = self._get_random_choice("historical_monuments.lighting")
            atmosphere = self._get_random_choice("historical_monuments.atmosphere")
            time = self._get_random_choice("historical_monuments.time_of_day")
            components["effects"] = (
                f"during ((majestic {lighting})), ((at {time})), "
                f"with ((atmospheric {atmosphere})), ((dramatic scale)), "
                f"((awe-inspiring presence)), ((timeless beauty)), "
                f"((perfect historical preservation))"
            )
            
        return components
