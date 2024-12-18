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

        # Subject component
        if custom_subject:
            components["subject"] = (
                f"((antique 1800s photograph:1.4)) of {custom_subject}, "
                f"((period-correct pose)), ((historical accuracy)), "
                f"((vintage daguerreotype style:1.3))"
            )
        else:
            subject = self._get_random_choice("subjects")
            components["subject"] = (
                f"((antique 1800s photograph:1.4)) of {subject}, "
                f"((period-correct pose)), ((historical accuracy)), "
                f"((vintage daguerreotype style:1.3))"
            )

        # Environment component
        if include_environment == "yes":
            setting = custom_location if custom_location else self._get_random_choice("settings")
            composition, props, pose, lighting = self._get_composition_elements()
            components["environment"] = (
                f"in ((period-authentic {setting}:1.2)), "
                f"with ((authentic {props})), ((masterful {lighting} lighting)), "
                f"((historical studio arrangement:1.3))"
            )

        # Style component
        if include_style == "yes":
            process, toning = self._get_process_and_toning()
            components["style"] = (
                f"((masterful {process} process:1.4)), "
                f"((authentic {toning} toning:1.3)), "
                f"((historical photography techniques:1.2)), "
                f"((heavily aged photograph:1.3)), "
                f"((vintage photographic plate:1.2))"
            )

        # Effects component
        if include_effects == "yes":
            components["effects"] = (
                f"((extreme vintage photographic qualities:1.4)), "
                f"((severely aged photograph appearance:1.3)), "
                f"((vintage chemical stains:1.2)), ((scratched emulsion)), "
                f"((deteriorated edges)), ((silver mirroring effect)), "
                f"((foxing marks)), ((heavy patina)), "
                f"((light leaks)), ((uneven development)), "
                f"((period-appropriate severe aging)), "
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