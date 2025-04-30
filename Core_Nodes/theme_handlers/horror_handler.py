import random
from typing import Dict
from .base_handler import BaseThemeHandler

class HorrorThemeHandler(BaseThemeHandler):
    """Handler for horror-themed prompt generation with enhanced atmospheric and psychological elements."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("horror")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate sophisticated horror-themed components with psychological depth."""
        components = {}
        
        # Always use random elements, even with custom_subject
        state = self._get_random_choice("horror.states")
        pose = self._get_random_choice("horror.poses")
        emotion = self._get_random_choice("horror.emotions")

        # Generate subject with enhanced horror elements
        if custom_subject:
            components["subject"] = (
                f"((masterfully crafted horror rendition)) of ((nightmarish {custom_subject})), "
                f"((in a terrifying {state} state)), ((with {pose})), "
                f"((expressing {emotion})), ((dark and psychologically disturbing)), "
                f"((sinister presence)), ((intricate macabre details)), "
                f"((unsettling anatomical features)), ((haunting expression)), "
                f"((psychological horror)), ((masterful horror design)), "
                f"((visceral fear)), ((primal dread))"
            )
        else:
            creature = self._get_random_choice("horror.creatures")
            state = self._get_random_choice("horror.states")
            pose = self._get_random_choice("horror.poses")
            emotion = self._get_random_choice("horror.emotions")
            components["subject"] = (
                f"((masterfully crafted horror rendition)) of ((nightmarish {creature})), "
                f"((in a terrifying {state} state)), ((with {pose})), "
                f"((expressing {emotion})), ((dark and psychologically disturbing)), "
                f"((intricate macabre details)), ((unsettling anatomical features)), "
                f"((masterful horror design)), ((visceral fear)), ((primal dread))"
            )
        
        # Generate environment with enhanced atmospheric horror
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((masterfully crafted horror environment)) of ((nightmarish {custom_location})), "
                    f"((perfect horror atmosphere)), ((psychological tension)), "
                    f"((sinister architectural details)), ((haunting mood)), "
                    f"((unsettling perspective)), ((dark psychological elements)), "
                    f"((masterful environmental horror))"
                )
            else:
                location = self._get_random_choice("horror.locations")
                time = self._get_random_choice("horror.times")
                atmosphere = self._get_random_choice("horror.atmospheres")
                architecture = self._get_random_choice("horror.architecture")
                components["environment"] = (
                    f"in ((masterfully crafted horror environment)) of ((nightmarish {location})), "
                    f"((during {time})), ((with {atmosphere} atmosphere)), "
                    f"((featuring {architecture})), ((perfect horror atmosphere)), "
                    f"((psychological tension)), ((sinister architectural details)), "
                    f"((haunting mood)), ((unsettling perspective)), "
                    f"((masterful environmental horror))"
                )
        
        # Generate style with enhanced horror aesthetics
        if include_style:
            style = self._get_random_choice("horror.styles")
            detail = self._get_random_choice("horror.details")
            technique = self._get_random_choice("horror.techniques")
            lighting = self._get_random_choice("horror.lighting")
            components["style"] = (
                f"((masterfully crafted horror art style)), ((featuring {style})), "
                f"((with perfect {detail})), ((using {technique})), "
                f"((enhanced by {lighting})), ((psychological horror aesthetics)), "
                f"((perfect horror composition)), ((masterful dramatic lighting)), "
                f"((haunting atmosphere)), ((visceral impact)), "
                f"((psychological depth)), ((horror excellence)), "
                f"8k resolution, perfect details"
            )
        
        # Generate effects with enhanced horror elements
        if include_effects:
            effect = self._get_random_choice("horror.effects")
            element = self._get_random_choice("horror.elements")
            texture = self._get_random_choice("horror.textures")
            atmosphere = self._get_random_choice("horror.atmospheric_effects")
            components["effects"] = (
                f"with ((masterful horror {effect})), ((terrifying {element})), "
                f"((disturbing {texture})), ((haunting {atmosphere})), "
                f"((psychological horror elements)), ((visceral fear effects)), "
                f"((masterful horror atmosphere)), ((perfect dread)), "
                f"((unsettling details)), ((horror excellence))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate comprehensive negative prompt for horror theme."""
        return (
            "((cartoonish)), ((cute)), ((cheerful)), ((bright colors)), "
            "((happy atmosphere)), ((peaceful)), ((calming)), ((serene)), "
            "((amateur horror)), ((poor lighting)), ((weak atmosphere)), "
            "((unconvincing horror)), ((generic scary)), ((childish)), "
            "((poor composition)), ((bad anatomy)), ((weak shadows)), "
            "((flat lighting)), ((poor details)), ((missing atmosphere)), "
            "((weak psychological impact)), ((unrealistic horror)), "
            "((cheap effects)), ((inconsistent style)), ((poor quality)), "
            "((blurry)), ((noisy)), ((pixelated)), ((comedy)), "
            "((family friendly)), ((safe for work)), ((casual)), "
            "((everyday scenes)), ((normal lighting)), ((daylight))"
        )
