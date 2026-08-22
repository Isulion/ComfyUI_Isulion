from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("pixel_art")
class PixelArtThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("pixel_art.subjects")
        palette = self._get_random_choice("pixel_art.color_palettes")

        if custom_subject:
            components["subject"] = (
                f"((pixel art)) of {custom_subject}, "
                f"(({palette} palette)), "
                f"((retro game sprite quality))"
            )
        else:
            components["subject"] = (
                f"((pixel art)) of (({subject})), "
                f"(({palette} palette)), "
                f"((retro game sprite quality))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((in pixel {custom_location})), "
                    f"((retro game backdrop))"
                )
            else:
                env = self._get_random_choice("pixel_art.environments")
                components["environment"] = (
                    f"((in {env})), "
                    f"((retro game backdrop))"
                )

        if include_style:
            style = self._get_random_choice("pixel_art.styles")
            lighting = self._get_random_choice("pixel_art.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((crisp pixel grid detail))"
            )

        if include_effects:
            effect = self._get_random_choice("pixel_art.effects")
            mood = self._get_random_choice("pixel_art.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components