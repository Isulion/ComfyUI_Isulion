from typing import Dict
from .base_handler import BaseThemeHandler

class NatureThemeHandler(BaseThemeHandler):
    """Handler for nature-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate nature-themed components with enhanced realism and detail."""
        components = {}
        
        # Generate subject with natural elements
        if custom_subject:
            components["subject"] = (
                f"((hyper-realistic {custom_subject})), "
                f"((natural beauty)), ((perfect composition)), "
                f"((environmental excellence)), ((pristine condition)), "
                f"((nature photography))"
            )
        else:
            landscape = self._get_random_choice("nature.landscapes")
            water = self._get_random_choice("nature.water_features")
            flora = self._get_random_choice("nature.flora")
            components["subject"] = (
                f"((hyper-realistic {landscape})) with ((majestic {water})) "
                f"and ((beautiful {flora})), ((natural beauty)), "
                f"((perfect composition)), ((environmental excellence)), "
                f"((pristine wilderness)), ((nature photography))"
            )
        
        # Generate environment with natural settings
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((pristine {custom_location})) with "
                    f"((perfect natural lighting)), ((environmental harmony)), "
                    f"((wilderness setting)), ((untouched nature))"
                )
            else:
                weather = self._get_random_choice("nature.weather_conditions")
                geology = self._get_random_choice("nature.geological_features")
                pattern = self._get_random_choice("nature.natural_patterns")
                components["environment"] = (
                    f"during ((dramatic {weather})) featuring ((impressive {geology})) "
                    f"with ((intricate {pattern})), ((perfect natural lighting)), "
                    f"((environmental harmony)), ((wilderness setting)), "
                    f"((untouched nature))"
                )
        
        # Generate style with nature photography techniques
        if include_style == "yes":
            style = self._get_random_choice("nature.styles")
            technique = self._get_random_choice("nature.techniques")
            lighting = self._get_random_choice("nature.lighting_conditions")
            components["style"] = (
                f"((captured in {style} style)), ((using {technique})), "
                f"((with {lighting})), ((nature photography excellence)), "
                f"((environmental artistry)), ((perfect natural composition)), "
                f"((photographic mastery)), ((high resolution)), "
                f"((professional nature photography))"
            )
        
        # Generate effects with natural elements
        if include_effects == "yes":
            effect = self._get_random_choice("nature.effects")
            components["effects"] = (
                f"with ((natural {effect})), ((environmental authenticity)), "
                f"((wilderness atmosphere)), ((natural beauty)), "
                f"((pristine conditions)), ((perfect nature capture))"
            )
        
        return components 