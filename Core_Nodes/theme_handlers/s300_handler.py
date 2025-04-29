from typing import Dict
from .base_handler import BaseThemeHandler

class s300ThemeHandler(BaseThemeHandler):
    """ Handler for the s300 cinematic dark fantasy theme """

    def generate(self, 
                 custom_subject: str = "", 
                 custom_location: str = "", 
                 include_environment: str = "yes", 
                 include_style: str = "yes",
                 include_effects: str = "yes") -> Dict[str, str]:
        components = {}

        # Always use random elements, even with custom_subject
        lighting = self._get_random_choice("s300.lighting") if hasattr(self, "_get_random_choice") else "dramatic chiaroscuro lighting"
        realism = self._get_random_choice("s300.realism") if hasattr(self, "_get_random_choice") else "stylized realism"

        # Subject generation
        if custom_subject:
            components["subject"] = (
                f"((epic {custom_subject})), "
                f"(({lighting})), (({realism}))"
            )
        else:
            main_element = self._get_random_choice("s300.main_elements")
            lighting = self._get_random_choice("s300.lighting")
            realism = self._get_random_choice("s300.realism")
            components["subject"] = (
                f"((cinematic {main_element})), (({lighting})), (({realism}))"
            )

        # Environment
        if include_environment == "yes":
            setting = self._get_random_choice("s300.settings")
            weather = self._get_random_choice("s300.weather") if hasattr(self, "_get_random_choice") else "stormy, desaturated"
            components["environment"] = f"in a (({weather} {setting}))"

        # Style & Effects (optional)
        style_elements = [
            "film grain texture", "Dreamlike Quality", "Emotional Intensity",
            "painterly brushstrokes", "Strong Contrast and Lighting",
            "Frank Miller comic panel aesthetic", "Textured Background"
        ]
        effects_elements = [
            "cinematic depth of field", "Frank Miller Comic Book Style",
            "dynamic composition with rim lighting", "Stylized Realism",
            "Grainy Texture", "Desaturated Colors with Deep Reds and Golds", "Gritty Textures",
            "Painterly Brushstrokes", "Film Grain Texture", "Emotional Intensity"
        ]

        if include_style == "yes":
            components["style"] = f"((stylized {', '.join(style_elements)}))"
        if include_effects == "yes":
            components["effects"] = f"((dramatic {', '.join(effects_elements)}))"

        return components