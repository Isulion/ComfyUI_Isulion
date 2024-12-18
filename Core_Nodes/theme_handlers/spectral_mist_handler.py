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
        environment = f"((masterful spectral environment)), ((with {color1} ethereal mist)), ((volumetric atmosphere:1.2))"
        style = "((ethereal art style:1.3)), ((ghostly aesthetics)), ((mystical atmosphere)), ((perfect composition)), ((professional quality)), ((highly detailed))"
        effects = f"((dynamic {color2} ectoplasmic particles:1.2)), ((forming intricate ethereal patterns)), ((magical energy flows)), ((atmospheric depth)), ((subtle glow)), ((perfect lighting))"

        prompt = (
            f"((masterful spectral art)) of {subject}, "
            f"manifesting within a {environment}, "
            f"((rendered in {style})), "
            f"with {effects}, "
            f"((8k resolution)), ((perfect details)), ((atmospheric excellence))"
        )

        components = {
            "prompt": prompt,
            "subject": subject,
            "environment": environment,
            "style": style,
            "effects": effects
        }

        return components
