from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("xray_anatomy")
class XRayAnatomyThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("xray_anatomy.subjects")
        inner_structure = self._get_random_choice("xray_anatomy.inner_structures")
        color_scheme = self._get_random_choice("xray_anatomy.color_schemes")

        if custom_subject:
            components["subject"] = (
                f"((x-ray scan)) of {custom_subject}, "
                f"((revealing {inner_structure})), "
                f"(({color_scheme} color scheme))"
            )
        else:
            components["subject"] = (
                f"((x-ray scan)) of (({subject})), "
                f"((revealing {inner_structure})), "
                f"(({color_scheme} color scheme))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((in {custom_location})), "
                    f"((dark high contrast backdrop))"
                )
            else:
                env = self._get_random_choice("xray_anatomy.environments")
                components["environment"] = (
                    f"((in {env})), "
                    f"((dark high contrast backdrop))"
                )

        if include_style:
            style = self._get_random_choice("xray_anatomy.styles")
            lighting = self._get_random_choice("xray_anatomy.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((high contrast medical imaging quality))"
            )

        if include_effects:
            effect = self._get_random_choice("xray_anatomy.effects")
            mood = self._get_random_choice("xray_anatomy.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components