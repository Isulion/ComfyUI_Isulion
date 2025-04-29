import random
from .base_handler import BaseThemeHandler
from typing import Optional, Dict

class SpectralMistThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("SpectralMist")
        self.colors = ["azure", "violet", "emerald", "ruby", "gold", "sapphire", "amber", "jade"]
        self._default_subjects = ["elf", "phantom", "spirit", "ghost", "creature"]

    def _get_color_scheme(self, custom_location: str) -> tuple:
        """Select primary and secondary colors."""
        primary_color = custom_location if custom_location else random.choice(self.colors)
        secondary_color = random.choice(self.colors)
        return primary_color, secondary_color

    def generate(self, custom_subject: Optional[str] = None, **kwargs) -> Dict:
        try:
            # Get colors without validation
            custom_location = kwargs.get('custom_location', '').strip().lower()
            primary_color, secondary_color = self._get_color_scheme(custom_location)

            # Always use random elements, even with custom_subject
            subject = custom_subject if custom_subject else random.choice(self._default_subjects)
            aura = random.choice(["shimmering", "glowing", "flickering", "pulsating", "luminous"])
            form = random.choice(["apparition", "wraith", "phantasm", "entity", "spirit"])
            detail = random.choice(["wispy", "translucent", "ethereal", "mist-wrapped", "otherworldly"])

            # Build components
            environment = f"((masterful spectral environment)), ((with {primary_color} ethereal mist)), ((volumetric atmosphere:1.2))"
            style = "((ethereal art style:1.3)), ((ghostly aesthetics)), ((mystical atmosphere)), ((perfect composition))"
            effects = f"((dynamic {secondary_color} ectoplasmic particles:1.2)), ((forming intricate patterns)), ((magical energy flows))"

            # Subject always gets random spectral details
            components = {}
            components["subject"] = (
                f"((spectral {subject})), (({aura} aura)), (({detail} {form})), "
                f"((manifesting in {primary_color} mist)), ((otherworldly presence)), ((mystical energy))"
            )
            components["environment"] = environment
            components["style"] = style
            components["effects"] = effects
            components["prompt"] = (
                f"((masterful spectral art)) of {subject}, "
                f"manifesting within a {environment}, "
                f"((rendered in {style})), "
                f"with {effects}, "
                f"((8k resolution)), ((perfect details))"
            )

            return components

        except Exception as e:
            raise ValueError(f"Failed to generate spectral mist prompt: {str(e)}")
