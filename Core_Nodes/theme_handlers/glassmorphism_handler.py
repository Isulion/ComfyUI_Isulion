from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("glassmorphism")
class GlassmorphismThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("glassmorphism.subjects")
        color_scheme = self._get_random_choice("glassmorphism.color_schemes")
        texture = self._get_random_choice("glassmorphism.textures")

        if custom_subject:
            components["subject"] = (
                f"((glassmorphism {custom_subject})), "
                f"((translucent frosted acrylic aesthetic)), "
                f"(({color_scheme} color scheme)), "
                f"(({texture} texture))"
            )
        else:
            components["subject"] = (
                f"(({subject})), "
                f"((translucent frosted acrylic aesthetic)), "
                f"(({color_scheme} color scheme)), "
                f"(({texture} texture))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in (({custom_location})), "
                    f"((clean minimal backdrop))"
                )
            else:
                env = self._get_random_choice("glassmorphism.environments")
                components["environment"] = (
                    f"in (({env})), "
                    f"((clean minimal backdrop))"
                )

        if include_style:
            style = self._get_random_choice("glassmorphism.styles")
            lighting = self._get_random_choice("glassmorphism.lighting")
            components["style"] = (
                f"((rendered in {style})), "
                f"(({lighting})), "
                f"((crystal clear quality)), 8k resolution"
            )

        if include_effects:
            effect = self._get_random_choice("glassmorphism.effects")
            mood = self._get_random_choice("glassmorphism.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components