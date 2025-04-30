from typing import Dict
from .base_handler import BaseThemeHandler

class WatercolorThemeHandler(BaseThemeHandler):
    """Handler for watercolor-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate watercolor-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            technique = self._get_random_choice("watercolor.techniques")
            components["subject"] = (
                f"((watercolor painting of {custom_subject})), "
                f"((using {technique})), ((soft edges)), "
                f"((fluid forms)), ((artistic interpretation))"
            )
        else:
            subject = self._get_random_choice("watercolor.subjects")
            technique = self._get_random_choice("watercolor.techniques")
            style = self._get_random_choice("watercolor.styles")
            components["subject"] = (
                f"((watercolor painting of {subject})), "
                f"((using {technique})), ((in {style} style)), "
                f"((soft edges)), ((fluid forms))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((watercolor {custom_location})), "
                    f"((flowing colors)), ((artistic atmosphere)), "
                    f"((painterly background))"
                )
            else:
                location = self._get_random_choice("watercolor.locations")
                time = self._get_random_choice("watercolor.times")
                mood = self._get_random_choice("watercolor.moods")
                components["environment"] = (
                    f"in ((watercolor {location})), "
                    f"((during {time})), ((with {mood} mood)), "
                    f"((flowing colors)), ((artistic atmosphere))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("watercolor.painting_styles")
            detail = self._get_random_choice("watercolor.details")
            components["style"] = (
                f"((watercolor art style)), ((featuring {style})), "
                f"((with {detail})), ((traditional painting)), "
                f"((perfect composition)), ((artistic lighting)), "
                f"((painterly quality)), 8k resolution"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("watercolor.effects")
            texture = self._get_random_choice("watercolor.textures")
            components["effects"] = (
                f"with ((watercolor {effect})), ((artistic {texture})), "
                f"((color bleeding)), ((paint flow)), "
                f"((artistic medium)), ((traditional techniques))"
            )
        
        return components
