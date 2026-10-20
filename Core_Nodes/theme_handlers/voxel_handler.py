from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("voxel")
class VoxelThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🕹️ Voxel Low-Poly"
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("voxel.subjects")
        color_scheme = self._get_random_choice("voxel.color_schemes")

        if custom_subject:
            components["subject"] = (
                f"((voxel art)) of {custom_subject}, "
                f"((blocky cubic construction)), "
                f"(({color_scheme} palette))"
            )
        else:
            components["subject"] = (
                f"((voxel art)) of (({subject})), "
                f"((blocky cubic construction)), "
                f"(({color_scheme} palette))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((in voxel {custom_location})), "
                    f"((blocky game world))"
                )
            else:
                env = self._get_random_choice("voxel.environments")
                components["environment"] = (
                    f"((in {env})), "
                    f"((blocky game world))"
                )

        if include_style:
            style = self._get_random_choice("voxel.styles")
            lighting = self._get_random_choice("voxel.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((clean geometric low-poly aesthetic))"
            )

        if include_effects:
            effect = self._get_random_choice("voxel.effects")
            mood = self._get_random_choice("voxel.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components
