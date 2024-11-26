from typing import Dict
from .base_handler import BaseThemeHandler

class InstagramThemeHandler(BaseThemeHandler):
    """Handler for Instagram-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Instagram-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((aesthetic {custom_subject})), "
                f"((Instagram worthy)), ((trendy composition)), "
                f"((social media style))"
            )
        else:
            subject = self._get_random_choice("instagram.subjects")
            pose = self._get_random_choice("instagram.poses")
            outfit = self._get_random_choice("instagram.outfits")
            components["subject"] = (
                f"((aesthetic {subject})) in ((trendy {outfit})), "
                f"((with {pose})), ((Instagram worthy)), "
                f"((social media style)), ((influencer aesthetic))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((Instagram-worthy {custom_location})) with "
                    f"((perfect lighting)), ((aesthetic background))"
                )
            else:
                location = self._get_random_choice("instagram.locations")
                props = self._get_random_choice("instagram.props")
                components["environment"] = (
                    f"in ((Instagram-worthy {location})) with "
                    f"((aesthetic {props})), "
                    f"((perfect lighting)), ((trendy setting)), "
                    f"((social media background))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("instagram.styles")
            filter = self._get_random_choice("instagram.filters")
            components["style"] = (
                f"((shot in {style} style)), "
                f"((with {filter} filter)), "
                f"((Instagram aesthetics)), ((social media quality)), "
                f"((trendy photography))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("instagram.effects")
            mood = self._get_random_choice("instagram.moods")
            components["effects"] = (
                f"with ((trendy {effect} effects)), "
                f"((aesthetic {mood} mood)), "
                f"((Instagram vibes)), ((social media appeal))"
            )
        
        return components