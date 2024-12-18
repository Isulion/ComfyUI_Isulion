import random
from .base_handler import BaseThemeHandler
from typing import Optional, Tuple

class SpectralMistThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("SpectralMist")
        self.colors = ["azure", "violet", "emerald", "ruby", "gold", "sapphire", "amber", "jade"]

    def generate(self, custom_subject: Optional[str] = None, **kwargs) -> dict:
        color1 = random.choice(self.colors)
        color2 = random.choice(self.colors)
        while color2 == color1:
            color2 = random.choice(self.colors)

        subject = custom_subject if custom_subject else random.choice(["elf", "phantom", "spirit", "ghost", "creature"])
        environment = f"Spectral Mist Emanation with {color1} spectral mist"
        style = "ethereal, ghostly, mystical"
        effects = f"intertwining {color2} ectoplasmic particles, forming ethereal shapes"

        components = {
            "prompt": f"A {subject} manifesting within a {environment}. The scene is {style}, as {effects}.",
            "subject": subject,
            "environment": environment,
            "style": style,
            "effects": effects
        }

        return components
