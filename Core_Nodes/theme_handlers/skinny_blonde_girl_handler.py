# filepath: Core_Nodes/theme_handlers/skinny_blonde_girl_handler.py
from typing import Dict, Optional
from .base_handler import BaseThemeHandler

class SkinnyBlondeGirlHandler(BaseThemeHandler):
    """Instagram-style 'Skinny Blonde Girl' theme."""

    def generate(self,
                 custom_subject: str = "",
                 custom_location: str = "",  
                 include_environment: str = "yes",
                 include_style: str = "yes",
                 include_effects: str = "yes") -> Dict[str, str]:
        components = {}

        # Instagram-style poses & expressions
        pose = self._get_random_choice("skinny_blonde_girl.poses")
        expression = self._get_random_choice("skinny_blonde_girl.expressions")

        # Core subject generation
        if custom_subject:
            components["subject"] = (
                f"((slim blonde girl with curves)), "
                f"wearing {self._get_outfit()}, "
                f"{pose}, {expression}"
            )
        else:
            components["subject"] = (
                f"((blonde bombshell)), "
                f"dressed in {self._get_outfit()}, "
                f"{pose} while {expression}"
            )

        # Instagram-style backdrops
        if include_environment == "yes":
            setting = self._get_random_choice("skinny_blonde_girl.settings")
            components["environment"] = (
                f"((in a {setting})), "
                f"((golden hour lighting)), ((minimalist decor))"
            )

        # Filters/effects (optional)
        if include_effects == "yes":
            filter_ = self._get_random_choice("skinny_blonde_girl.filters")
            components["effects"] = (
                f"((applied {filter_})), "
                f"((subtle lens flare)), ((sharp focus))"
            )

        return components

    def _get_outfit(self) -> str:
        top = self._get_random_choice("skinny_blonde_girl.outfits_top")
        bottom = self._get_random_choice("skinny_blonde_girl.outfits_bottom")
        accessories = self._get_random_choice("skinny_blonde_girl.accessories")
        
        return f"{top} and {bottom}, accessorized with {accessories}"