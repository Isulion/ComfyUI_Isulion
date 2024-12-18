import random
from typing import Dict, Optional
from .base_handler import BaseThemeHandler
import json
import os

class Vintage1800sPhotographyHandler(BaseThemeHandler):
    """Handler for generating 1800s vintage photography-themed prompts."""

    def __init__(self, config):
        """Initialize with config manager."""
        super().__init__(config)
        self.theme_config = config.get_config("vintage_1800s_photography")
        if not self.theme_config:
            raise ValueError("Missing vintage_1800s_photography configuration")

    def _get_process_and_toning(self) -> tuple:
        """Select photographic process and toning effect."""
        process = self._get_random_choice("processes")
        toning = self._get_random_choice("toning")
        return process, toning

    def _get_composition_elements(self) -> tuple:
        """Select composition style and props."""
        composition = self._get_random_choice("compositions")
        props = self._get_random_choice("props")
        pose = self._get_random_choice("poses")
        lighting = self._get_random_choice("lighting")
        return composition, props, pose, lighting

    def _get_random_choice(self, key: str) -> str:
        """Get random choice from theme configuration."""
        if key not in self.theme_config:
            raise KeyError(f"Missing {key} in vintage_1800s_photography config")
        return random.choice(self.theme_config[key])

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        components = {}
        
        # Subject
        subject = custom_subject if custom_subject else self._get_random_choice("subjects")
        components["subject"] = (
            f"((extremely old photograph)), ((vintage 1800s photograph:1.4)) of {subject}, "
            f"((period-correct pose)), ((historical accuracy:1.3))"
        )
        
        # Environment
        if include_environment == "yes":
            setting = custom_location if custom_location else self._get_random_choice("settings")
            components["environment"] = (
                f"in ((period-authentic {setting})), ((authentic vintage studio)), "
                f"((historical photography setting:1.2))"
            )
        
        # Style
        if include_style == "yes":
            components["style"] = (
                f"((masterful daguerreotype:1.4)), ((authentic sepia toning:1.3)), "
                f"((historical photography techniques)), ((aged photograph)), "
                f"((vintage photographic plate))"
            )
        
        # Effects
        if include_effects == "yes":
            components["effects"] = (
                f"((extreme vintage artifacts:1.4)), ((severe aging:1.3)), "
                f"((chemical stains)), ((scratched emulsion)), "
                f"((deteriorated edges)), ((silver mirroring)), "
                f"((foxing marks)), ((heavy patina)), "
                f"((authentic vintage photograph damage:1.3))"
            )
        
        return components

    def get_negative_prompt(self) -> str:
        """Generate negative prompt to avoid modern elements."""
        return (
            "modern elements, contemporary style, digital effects, "
            "color photography, modern clothing, plastic, HDR, "
            "contemporary poses, modern background, artificial lighting, "
            "perfect condition, clean photo, sharp details, pristine condition, "
            "modern photo quality, digital artifacts, contemporary editing"
        )