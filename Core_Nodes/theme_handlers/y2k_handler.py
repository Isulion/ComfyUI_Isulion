from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("y2k")
class Y2KThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("y2k.subjects")
        color_scheme = self._get_random_choice("y2k.color_schemes")
        texture = self._get_random_choice("y2k.textures")
        accessory = self._get_random_choice("y2k.accessories")

        if custom_subject:
            components["subject"] = (
                f"((Y2K style {custom_subject})), "
                f"((wearing {accessory})), "
                f"(({color_scheme} color palette)), "
                f"(({texture} texture))"
            )
        else:
            components["subject"] = (
                f"(({subject})), "
                f"((wearing {accessory})), "
                f"(({color_scheme} color palette)), "
                f"(({texture} texture))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((Y2K {custom_location})), "
                    f"((retro futuristic setting))"
                )
            else:
                env = self._get_random_choice("y2k.environments")
                components["environment"] = (
                    f"in (({env})), "
                    f"((retro futuristic setting))"
                )

        if include_style:
            style = self._get_random_choice("y2k.styles")
            lighting = self._get_random_choice("y2k.lighting")
            components["style"] = (
                f"((rendered in {style})), "
                f"(({lighting})), "
                f"((glossy magazine quality))"
            )

        if include_effects:
            effect = self._get_random_choice("y2k.effects")
            mood = self._get_random_choice("y2k.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components