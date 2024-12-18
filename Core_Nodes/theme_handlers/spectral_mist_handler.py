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
            
            # Get subject
            subject = custom_subject if custom_subject else random.choice(self._default_subjects)
            
            # Build components
            environment = f"((masterful spectral environment)), ((with {primary_color} ethereal mist)), ((volumetric atmosphere:1.2))"
            style = "((ethereal art style:1.3)), ((ghostly aesthetics)), ((mystical atmosphere)), ((perfect composition))"
            effects = f"((dynamic {secondary_color} ectoplasmic particles:1.2)), ((forming intricate patterns)), ((magical energy flows))"
            
            prompt = (
                f"((masterful spectral art)) of {subject}, "
                f"manifesting within a {environment}, "
                f"((rendered in {style})), "
                f"with {effects}, "
                f"((8k resolution)), ((perfect details))"
            )

            return {
                "prompt": prompt,
                "subject": subject,
                "environment": environment,
                "style": style,
                "effects": effects
            }

        except Exception as e:
            raise ValueError(f"Failed to generate spectral mist prompt: {str(e)}")
