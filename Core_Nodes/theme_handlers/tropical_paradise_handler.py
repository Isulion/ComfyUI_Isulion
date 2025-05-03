from typing import Dict
from .base_handler import BaseThemeHandler
import random

class TropicalParadiseThemeHandler(BaseThemeHandler):
    """Handler for tropical paradise-themed prompt generation."""

    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("tropical_paradise")

    def _get_random(self, key, fallback=None):
        try:
            values = self.theme_config.get(key, [])
            if values:
                return random.choice(values)
            if fallback is not None:
                return fallback
        except Exception:
            pass
        return fallback or "tropical"

    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        """Generate tropical paradise-themed components."""
        components = {}

        # Subject
        flora = self._get_random("flora", "orchids")
        fauna = self._get_random("fauna", "parrots")
        feature = self._get_random("features", "palm trees")
        if custom_subject:
            components["subject"] = (
                f"((tropical paradise {custom_subject})), "
                f"((lush {flora})), ((vivid {fauna})), (({feature})), "
                f"((idyllic setting)), ((paradise atmosphere))"
            )
        else:
            main = self._get_random("main_elements", "beach")
            components["subject"] = (
                f"((tropical paradise with {main})), "
                f"((lush {flora})), ((vivid {fauna})), (({feature})), "
                f"((idyllic setting)), ((paradise atmosphere))"
            )

        # Environment
        if include_environment:
            water = self._get_random("water", "crystal-clear water")
            sand = self._get_random("sand", "white sand beach")
            weather = self._get_random("weather", "sunny")
            time = self._get_random("times", "sunset")
            if custom_location:
                components["environment"] = (
                    f"in (({custom_location})), (({water})), (({sand})), "
                    f"(({weather})), (({time})), ((serene horizon)), ((paradise environment))"
                )
            else:
                setting = self._get_random("settings", "secluded island")
                components["environment"] = (
                    f"in (({setting})), (({water})), (({sand})), "
                    f"(({weather})), (({time})), ((serene horizon)), ((paradise environment))"
                )

        # Style
        if include_style:
            style = self._get_random("styles", "vivid color palette")
            technique = self._get_random("techniques", "soft focus")
            components["style"] = (
                f"((rendered in {style} style)), ((using {technique} technique)), "
                f"((artistic composition)), ((perfect exposure)), ((professional quality)), "
                f"((vibrant colors)), ((dreamlike atmosphere))"
            )

        # Effects
        if include_effects:
            effect = self._get_random("effects", "sunbeams")
            pattern = self._get_random("patterns", "rippling water")
            components["effects"] = (
                f"with (({effect})), (({pattern})), "
                f"((atmospheric haze)), ((glowing highlights)), "
                f"((tropical ambiance)), ((paradise effect))"
            )

        return components
