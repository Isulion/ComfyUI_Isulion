from typing import Dict
from .base_handler import BaseThemeHandler
import random

class SelfieThemeHandler(BaseThemeHandler):
    """Handler for selfie theme with location-appropriate styling."""

    def handle(self, **kwargs) -> Dict[str, str]:
        """Handle selfie theme generation with location-based styling."""
        components = {}
        
        # Define location-based clothing styles
        location_outfits = {
            "beach": ["swimsuit", "beach cover-up", "summer dress", "board shorts", "resort wear"],
            "gym": ["workout outfit", "athletic wear", "sports bra and leggings", "gym shorts and tank top"],
            "cafe": ["casual chic outfit", "trendy streetwear", "fashionable ensemble", "smart casual attire"],
            "restaurant": ["elegant dress", "formal suit", "cocktail attire", "upscale outfit"],
            "hiking trail": ["hiking gear", "outdoor activewear", "trail outfit", "adventure wear"],
            "tourist spot": ["comfortable tourist outfit", "casual travel wear", "sightseeing attire"],
            "shopping mall": ["trendy casual wear", "shopping outfit", "fashion-forward ensemble"],
            "party": ["party dress", "club wear", "evening attire", "festive outfit"],
            "office": ["business attire", "professional suit", "corporate wear", "business casual"],
            "park": ["casual outdoor wear", "picnic outfit", "relaxed ensemble"]
        }
        
        # Get custom location and subject
        custom_location = kwargs.get("custom_location", "").strip()
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Determine location and outfit
        if custom_location:
            # Use the custom location directly if provided
            location = custom_location
            # Try to find matching outfits or use generic outfit options
            matching_locations = [loc for loc in location_outfits.keys() 
                                if loc.lower() in custom_location.lower()]
            if matching_locations:
                outfit = random.choice(location_outfits[matching_locations[0]])
            else:
                # Use casual outfit if no specific location match
                outfit = "stylish casual wear"
        else:
            location = random.choice(list(location_outfits.keys()))
            outfit = random.choice(location_outfits[location])
        
        # Build subject component
        if custom_subject:
            components["subject"] = (
                f"((professional selfie photograph)) of {custom_subject} at a ((beautiful {location})), "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        else:
            components["subject"] = (
                f"((professional selfie photograph)) of ((attractive person)) at a ((beautiful {location})), "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(["golden hour", "sunset", "bright daylight", "blue hour", "evening"])
            components["environment"] = (
                f"during {time}, ((perfect lighting)), "
                f"((instagram-worthy {location} background)), "
                f"((social media aesthetic)), ((lifestyle photography))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((social media photography)), ((smartphone aesthetic)), "
                f"((perfect exposure)), ((authentic lifestyle)), "
                f"((trendy composition)), ((influencer style)), "
                f"((natural looking)), ((candid moment)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((natural bokeh)), ((soft skin glow)), "
                f"((perfect lighting)), ((subtle vignette)), "
                f"((instagram filter)), ((social media finish)), "
                f"((lifestyle colors)), ((authentic atmosphere))"
            )
        
        return components
