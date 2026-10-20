from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("analog_film")
class AnalogFilmThemeHandler(BaseThemeHandler):
    DISPLAY_NAME = "🎬 Analog 35mm Film"
    def generate(self, custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: bool = True,
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        subject = self._get_random_choice("analog_film.subjects")
        film_stock = self._get_random_choice("analog_film.film_stocks")
        camera = self._get_random_choice("analog_film.cameras")

        if custom_subject:
            components["subject"] = (
                f"((analog film photograph)) of {custom_subject}, "
                f"((shot on {film_stock})), "
                f"((with {camera}))"
            )
        else:
            components["subject"] = (
                f"((analog film photograph)) of (({subject})), "
                f"((shot on {film_stock})), "
                f"((with {camera}))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"((captured in {custom_location})), "
                    f"((analog documentary setting))"
                )
            else:
                env = self._get_random_choice("analog_film.environments")
                components["environment"] = (
                    f"((captured in {env})), "
                    f"((analog documentary setting))"
                )

        if include_style:
            style = self._get_random_choice("analog_film.styles")
            lighting = self._get_random_choice("analog_film.lighting")
            components["style"] = (
                f"(({style})), "
                f"(({lighting})), "
                f"((vintage analog aesthetic))"
            )

        if include_effects:
            effect = self._get_random_choice("analog_film.effects")
            mood = self._get_random_choice("analog_film.moods")
            components["effects"] = (
                f"with (({effect})), "
                f"(({mood} atmosphere))"
            )

        return components
