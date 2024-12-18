from typing import Dict
from .base_handler import BaseThemeHandler

class InstagramLifestyleThemeHandler(BaseThemeHandler):
    """Handler for Instagram lifestyle-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Instagram lifestyle-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((lifestyle {custom_subject})), "
                f"((instagram aesthetic)), ((social media style)), "
                f"((influencer look))"
            )
        else:
            subject = self._get_random_choice("instagram_lifestyle.subjects")
            activity = self._get_random_choice("instagram_lifestyle.activities")
            prop = self._get_random_choice("instagram_lifestyle.props")
            components["subject"] = (
                f"(({subject} {activity})), "
                f"((with {prop})), "
                f"((instagram aesthetic)), ((influencer style))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((trendy {custom_location})) with "
                    f"((lifestyle setting)), ((instagram worthy))"
                )
            else:
                location = self._get_random_choice("instagram_lifestyle.locations")
                aesthetic = self._get_random_choice("instagram_lifestyle.aesthetics")
                mood = self._get_random_choice("instagram_lifestyle.moods")
                components["environment"] = (
                    f"in (({location})) with (({aesthetic} design)), "
                    f"((creating {mood} atmosphere)), "
                    f"((instagram worthy)), ((lifestyle scene))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("instagram_lifestyle.styles")
            components["style"] = (
                f"((styled as {style})), "
                f"((instagram aesthetic)), "
                f"((social media beauty)), ((lifestyle design)), "
                f"((influencer quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("instagram_lifestyle.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((instagram atmosphere)), "
                f"((lifestyle ambiance)), ((social media environment))"
            )
        
        return components