from typing import Dict
from .base_handler import BaseThemeHandler

class InstagramLifestyleThemeHandler(BaseThemeHandler):
    """Handler for Instagram lifestyle-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Instagram lifestyle-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        activity = self._get_random_choice("instagram_lifestyle.activities")
        prop = self._get_random_choice("instagram_lifestyle.props")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((lifestyle {custom_subject} {activity})), "
                f"((with {prop})), "
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
        if include_environment:
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
        if include_style:
            style = self._get_random_choice("instagram_lifestyle.styles")
            components["style"] = (
                f"((styled as {style})), "
                f"((instagram aesthetic)), "
                f"((social media beauty)), ((lifestyle design)), "
                f"((influencer quality))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("instagram_lifestyle.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((instagram atmosphere)), "
                f"((lifestyle ambiance)), ((social media environment))"
            )
        
        return components
