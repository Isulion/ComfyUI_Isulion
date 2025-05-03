from typing import Dict
from .base_handler import BaseThemeHandler
import random

class SpaceColonyHandler(BaseThemeHandler):
    """Handler for the Space Colony theme."""

    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("space_colony")

    def _get_random(self, key, fallback=None):
        values = self.theme_config.get(key, [])
        if values:
            return random.choice(values)
        return fallback or ""

    def generate(
        self,
        custom_subject: str = "",
        custom_location: str = "",
        include_environment: bool = True,
        include_style: bool = True,
        include_effects: bool = True
    ) -> Dict[str, str]:
        """Generates prompt components for the Space Colony theme."""

        cfg = self.theme_config
        components = {}

        # Subject
        main_element = self._get_random("main_elements", "dome habitat")
        subject_parts = []

        if custom_subject:
            subject_parts.append(f"space colony {custom_subject}")
        else:
            subject_parts.append(f"space colony {main_element}")

        # Always add inhabitants, flora, activities, technologies if present and non-empty
        for key in ["inhabitants", "flora", "activities", "technologies"]:
            if key in cfg:
                value = self._get_random(key)
                if value:
                    subject_parts.append(value)

        # Optionally add nature photography technique
        if "nature_techniques" in cfg and random.random() < 0.5:
            technique = self._get_random("nature_techniques")
            if technique:
                subject_parts.append(f"{technique} technique")

        components["subject"] = ", ".join(f"(({part}))" for part in subject_parts)

        # Environment
        if include_environment:
            if custom_location:
                env = f"space environment {custom_location}"
            else:
                env = self._get_random("settings", "Martian desert")
            # Optionally add lighting
            if "lighting_conditions" in cfg and random.random() < 0.5:
                lighting = self._get_random("lighting_conditions")
                env = f"{env}, {lighting}"
            components["environment"] = f"in (({env}))"

        # Style
        if include_style:
            style = self._get_random("styles", "sleek futuristic")
            style_str = f"in the style of (({style}))"
            # Optionally add nature photography style
            if "nature_techniques" in cfg and random.random() < 0.5:
                technique = self._get_random("nature_techniques")
                style_str += f", ((hyper-realistic nature photography)), (({technique}))"
            components["style"] = style_str

        # Effects
        if include_effects:
            effect = self._get_random("effects", "starfield backdrop")
            effects_str = f"with (({effect}))"
            # Optionally add nature effect
            if "nature_effects" in cfg and random.random() < 0.7:
                nature_effect = self._get_random("nature_effects")
                effects_str += f", (({nature_effect}))"
            components["effects"] = effects_str

        return components
