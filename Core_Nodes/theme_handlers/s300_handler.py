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
            "film grain texture", 
            "painterly brushstrokes", 
            "Frank Miller comic panel aesthetic"
        ]
        effects_elements = [
            "cinematic depth of field",
            "dynamic composition with rim lighting"
        ]

        components["style"] = f"((stylized {', '.join(style_elements)})"
        components["effects"] = f"((dramatic {', '.join(effects_elements)}))"

        return components