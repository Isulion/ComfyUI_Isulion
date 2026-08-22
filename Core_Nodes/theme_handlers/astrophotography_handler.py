from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("astrophotography")
class AstrophotographyThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("astrophotography.subjects")
        celestial = self._get_random_choice("astrophotography.celestial_bodies")
        phenomenon = self._get_random_choice("astrophotography.phenomena")

        if custom_subject:
            components["subject"] = (
                f"((astrophotograph)) of {custom_subject}, "
                f"((with {celestial} in the sky)), "
                f"(({phenomenon}))"
            )
        else:
            components["subject"] = (
                f"((astrophotograph)) of (({subject})), "
                f"((with {celestial} in the sky)), "
                f"(({phenomenon}))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((taken at {custom_location})), "
                    f"((pristine dark sky location))"
                )
            else:
                env = self._get_random_choice("astrophotography.environments")
                components["environment"] = (
                    f"((taken at {env})), "
                    f"((pristine dark sky location))"
                )

        if include_style:
            style = self._get_random_choice("astrophotography.styles")
            lighting = self._get_random_choice("astrophotography.lighting")
            components["style"] = (
                f"((rendered in {style})), "
                f"(({lighting})), "
                f"((cosmic clarity)), deep space detail"
            )

        if include_effects:
            effect = self._get_random_choice("astrophotography.effects")
            mood = self._get_random_choice("astrophotography.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components