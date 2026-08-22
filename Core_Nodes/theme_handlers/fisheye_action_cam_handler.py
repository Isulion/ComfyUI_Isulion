from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("fisheye_action_cam")
class FisheyeActionCamThemeHandler(BaseThemeHandler):
    def generate(self, custom_subject="", custom_location="",
                 include_environment=True, include_style=True, include_effects=True) -> Dict[str, str]:
        components = {}
        subject = self._get_random_choice("fisheye_action_cam.subjects")
        angle = self._get_random_choice("fisheye_action_cam.camera_angles")
        if custom_subject:
            components["subject"] = f"((fisheye action cam)) (({custom_subject})), (({angle})), ((extreme POV action))"
        else:
            components["subject"] = f"((fisheye action cam)) (({subject})), (({angle})), ((extreme POV action))"
        if include_environment:
            env = self._get_random_choice("fisheye_action_cam.environments") if not custom_location else custom_location
            components["environment"] = f"((in {env})), ((action zone))"
        if include_style:
            style = self._get_random_choice("fisheye_action_cam.style")
            components["style"] = f"(({style}))"
        if include_effects:
            effect = self._get_random_choice("fisheye_action_cam.effects")
            lighting = self._get_random_choice("fisheye_action_cam.lighting")
            mood = self._get_random_choice("fisheye_action_cam.moods")
            components["effects"] = f"(({effect})), (({lighting})), (({mood}))"
        return components