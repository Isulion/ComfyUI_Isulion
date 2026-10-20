from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme

@register_theme("valentines_day")
class ValentinesDayThemeHandler(BaseThemeHandler):
    """Handler for Valentine's Day-themed prompt generation."""
    DISPLAY_NAME = "💘 Valentine's Day"

    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = [
            "dark colors", "horror elements", "industrial settings",
            "urban landscapes", "cold tones", "aggressive imagery"
        ]
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate Valentine's Day-themed components."""
        components = {}

        # Custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()

        # Select core elements
        characters = ["romantic couple", "lovers", "heart-shaped silhouette", "tender embrace", "romantic figure"]
        attire = ["elegant dress", "romantic outfit", "soft flowing clothing", "heart-themed accessories", "love-inspired attire"]
        props = ["roses", "heart-shaped gift", "love letter", "romantic candle", "delicate jewelry"]
        color_schemes = ["romantic red", "soft pink", "rose gold", "blush and white", "passionate crimson"]

        character = self.config.random.choice(characters)
        color_scheme = self.config.random.choice(color_schemes)

        if custom_subject:
            components["subject"] = (
                f"((romantic Valentine's Day scene)) of {custom_subject}, "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((love atmosphere)), ((romantic magic))"
            )
        else:
            components["subject"] = (
                f"((romantic Valentine's Day scene)) of ((a {character})), "
                f"((wearing {self.config.random.choice(attire)}) ), "
                f"((with {self.config.random.choice(props)}) ), "
                f"in {color_scheme} colors, ((love atmosphere)), ((romantic magic))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((romantic {custom_location})), ((decorated for Valentine's Day)), "
                    f"((intimate setting)), ((soft lighting)), "
                    f"((love-filled atmosphere)), ((Valentine's charm))"
                )
            else:
                settings = ["candlelit room", "cozy cafe", "moonlit garden", "elegant ballroom", "intimate restaurant"]
                lighting = ["soft candlelight", "romantic moonlight", "warm ambient glow", "gentle evening light"]

                setting = self.config.random.choice(settings)
                light = self.config.random.choice(lighting)

                components["environment"] = (
                    f"in ((a magical {setting})), ((illuminated by {light})), "
                    f"((romantic atmosphere)), ((Valentine's Day setting)), "
                    f"((love-inspired landscape)), ((tender moments))"
                )

        if include_style:
            components["style"] = (
                "((romantic Valentine's Day artwork)), ((love illustration style)), "
                "((soft watercolor technique)), ((delicate painting)), "
                "((romantic color palette)), ((passionate holiday mood)), "
                "((Valentine's card quality)), ((tender artistic rendering)), "
                "8k resolution, ((magical love lighting))"
            )

        if include_effects:
            components["effects"] = (
                "with ((magical love glow)), ((soft romantic light)), "
                "((floating rose petals)), ((heart sparkle)), "
                "((warm love atmosphere)), ((romantic magic)), "
                "((love letter shimmer)), ((delicate emotion effects))"
            )

        return components
