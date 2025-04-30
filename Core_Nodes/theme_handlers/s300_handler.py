from typing import Dict
from .base_handler import BaseThemeHandler

class s300ThemeHandler(BaseThemeHandler):
    """ Handler for the s300 cinematic dark fantasy theme """

    def _get_random_choice(self, key):
        FALLBACKS = {
            "s300.lighting": [
                "dramatic chiaroscuro lighting", "harsh backlighting", "fiery sunset glow",
                "moonlit shadows", "torch-lit ambiance", "stormy lightning flashes"
            ],
            "s300.realism": [
                "stylized realism", "hyper-realistic detail", "painterly realism", "cinematic realism"
            ],
            "s300.weather": [
                "stormy", "foggy", "rain-soaked", "dusty", "wind-swept", "desaturated"
            ],
        }
        try:
            return self.config_manager.get_random_choice(key)
        except Exception:
            if key in FALLBACKS:
                if getattr(self, "debug", False):
                    print(f"[DEBUG] Using fallback for missing config key: {key}")
                return self.config_manager.random.choice(FALLBACKS[key])
            raise

    def _safe_random_choice(self, key, fallback):
        try:
            return self._get_random_choice(key)
        except Exception:
            return fallback

    def generate(self, 
                 custom_subject: str = "", 
                 custom_location: str = "", 
                 include_environment: bool = True, 
                 include_style: bool = True,
                 include_effects: bool = True) -> Dict[str, str]:
        components = {}

        # Always use random elements, even with custom_subject
        lighting = self._safe_random_choice("s300.lighting", "dramatic chiaroscuro lighting")
        realism = self._safe_random_choice("s300.realism", "stylized realism")

        # Subject generation
        if custom_subject:
            components["subject"] = (
                f"((epic {custom_subject})), "
                f"(({lighting})), (({realism}))"
            )
        else:
            main_element = self._safe_random_choice("s300.main_elements", "warrior")
            lighting = self._safe_random_choice("s300.lighting", "dramatic chiaroscuro lighting")
            realism = self._safe_random_choice("s300.realism", "stylized realism")
            components["subject"] = (
                f"((cinematic {main_element})), (({lighting})), (({realism}))"
            )

        # Environment
        if include_environment:
            setting = self._safe_random_choice("s300.settings", "ancient battlefield")
            weather = self._safe_random_choice("s300.weather", "stormy, desaturated")
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

        if include_style:
            components["style"] = f"((stylized {', '.join(style_elements)}))"
        if include_effects:
            components["effects"] = f"((dramatic {', '.join(effects_elements)}))"

        return components