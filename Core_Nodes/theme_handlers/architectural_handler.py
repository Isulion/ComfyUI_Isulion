from typing import Dict
from .base_handler import BaseThemeHandler

class ArchitecturalThemeHandler(BaseThemeHandler):
    """Handler for architectural-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate architectural-themed components with professional quality."""
        components = {}

        # Always use random elements, even with custom_subject
        style = self._get_random_choice("architectural.styles")
        feature = self._get_random_choice("architectural.features")

        if custom_subject:
            components["subject"] = (
                f"((masterful architectural photography)) of {custom_subject}, "
                f"((in {style} style)), ((featuring {feature})), "
                f"((perfect architectural composition)), ((structural excellence)), "
                f"((professional architectural detail)), ((design mastery)), "
                f"((geometric precision)), ((architectural brilliance))"
            )
        else:
            building = self._get_random_choice("architectural.buildings")
            components["subject"] = (
                f"((masterful architectural photography)) of ((magnificent {building})), "
                f"((in {style} style)), ((featuring {feature})), "
                f"((perfect architectural composition)), ((structural excellence)), "
                f"((design mastery)), ((geometric precision))"
            )

        # Generate environment with enhanced spatial context
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((professionally composed {custom_location})) with "
                    f"((perfect spatial context)), ((architectural harmony)), "
                    f"((environmental integration)), ((masterful composition)), "
                    f"((urban planning excellence))"
                )
            else:
                location = self._get_random_choice("architectural.locations")
                time = self._get_random_choice("architectural.times")
                weather = self._get_random_choice("architectural.weather")
                components["environment"] = (
                    f"in ((professionally composed {location})) during "
                    f"((dramatic {time})) with ((perfect {weather} conditions)), "
                    f"((architectural context)), ((spatial harmony)), "
                    f"((environmental mastery)), ((urban excellence))"
                )

        # Generate style with enhanced architectural techniques
        if include_style:
            technique = self._get_random_choice("architectural.techniques")
            perspective = self._get_random_choice("architectural.perspectives")
            components["style"] = (
                f"((masterfully captured using {technique})), "
                f"((perfect {perspective} perspective)), ((architectural photography)), "
                f"((professional lighting)), ((structural clarity)), "
                f"((design excellence)), ((technical mastery)), "
                f"((flawless composition)), 8k resolution"
            )

        # Generate effects with enhanced architectural elements
        if include_effects:
            effect = self._get_random_choice("architectural.effects")
            lighting = self._get_random_choice("architectural.lighting")
            atmosphere = self._get_random_choice("architectural.atmosphere")
            components["effects"] = (
                f"with ((perfect architectural {effect})), "
                f"((masterful {lighting} lighting)), ((beautiful {atmosphere})), "
                f"((dramatic shadows)), ((structural detail)), "
                f"((professional finish)), ((visual excellence))"
            )

        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common architectural photography issues."""
        return (
            "((blurry)), ((poor composition)), ((bad perspective)), ((distorted)), "
            "((amateur)), ((poor lighting)), ((blown highlights)), ((crushed shadows)), "
            "((lens distortion)), ((chromatic aberration)), ((noise)), ((grain)), "
            "((overexposed)), ((underexposed)), ((poor focus)), ((camera shake)), "
            "((bad framing)), ((cluttered)), ((distracting elements)), "
            "((poor architectural detail)), ((incorrect perspective)), "
            "((bad geometry)), ((structural errors)), ((poor construction))"
        )
