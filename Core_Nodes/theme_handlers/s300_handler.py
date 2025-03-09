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

        # Subject generation
        if custom_subject:
            components["subject"] = (
                f"((epic {custom_subject})), "
                f"((dramatic chiaroscuro lighting)), ((stylized realism))"
            )
        else:
            main_element = self._get_random_choice("s300.main_elements")
            components["subject"] = f"((cinematic {main_element})), ((high-contrast battlefield))"

        # Environment
        if include_environment == "yes":
            setting = self._get_random_choice("s300.settings")
            components["environment"] = f"in a ((stormy, desaturated {setting}))"

        # Style & Effects (optional)
        style_elements = [
            "film grain texture", "Dreamlike Quality","Emotional Intensity",
            "painterly brushstrokes", "Strong Contrast and Lighting",
            "Frank Miller comic panel aesthetic","Textured Background"
        ]
        effects_elements = [
            "cinematic depth of field","Frank Miller Comic Book Style"
            "dynamic composition with rim lighting","Stylized Realism",
            "Grainy Texture", "Desaturated Colors with Deep Reds and Golds","Gritty Textures",
            "Painterly Brushstrokes","Film Grain Texture","Emotional Intensity"
        ]

        components["style"] = f"((stylized {', '.join(style_elements)})"
        components["effects"] = f"((dramatic {', '.join(effects_elements)}))"

        return components