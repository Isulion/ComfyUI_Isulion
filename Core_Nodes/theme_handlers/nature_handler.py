from typing import Dict
from .base_handler import BaseThemeHandler

class NatureThemeHandler(BaseThemeHandler):
    """Handler for nature-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate nature-themed components with enhanced realism and detail."""
        components = {}
        
        # Always use random elements, even with custom_subject
        atmosphere = self._get_random_choice("nature.atmospheres")
        season = self._get_random_choice("nature.seasons")
        natural_phenomena = self._get_random_choice("nature.natural_phenomena")
        flora = self._get_random_choice("nature.flora")

        # Generate subject with natural elements
        if custom_subject:
            components["subject"] = (
                f"((masterful landscape photograph of {atmosphere} {custom_subject})) "
                f"with ((majestic {natural_phenomena})) and ((beautiful {flora})), "
                f"((during {season})), ((breathtaking natural beauty)), "
                f"((perfect composition)), ((pristine wilderness)), "
                f"((professional landscape photography))"
            )
        else:
            landscape = self._get_random_choice("nature.landscapes")
            water = self._get_random_choice("nature.water_features")
            flora = self._get_random_choice("nature.flora")
            season = self._get_random_choice("nature.seasons")
            atmosphere = self._get_random_choice("nature.atmospheres")
            components["subject"] = (
                f"((masterful landscape photograph of {atmosphere} {landscape})) "
                f"with ((majestic {self._get_random_choice('nature.natural_phenomena')})) and ((beautiful {flora})), "
                f"((during {season})), ((breathtaking natural beauty)), "
                f"((perfect composition)), ((pristine wilderness)), "
                f"((professional landscape photography))"
            )
        
        # Generate environment with natural settings
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((pristine {custom_location})) with "
                    f"((perfect natural lighting)), ((environmental harmony)), "
                    f"((untouched wilderness)), ((raw natural beauty))"
                )
            else:
                weather = self._get_random_choice("nature.weather_conditions")
                geology = self._get_random_choice("nature.geological_features")
                pattern = self._get_random_choice("nature.natural_patterns")
                time = self._get_random_choice("nature.time_of_day")
                components["environment"] = (
                    f"during (({time} with {weather})), featuring ((impressive {geology})) "
                    f"with ((intricate {pattern})), ((perfect natural lighting)), "
                    f"((environmental harmony)), ((pristine wilderness)), "
                    f"((raw natural beauty))"
                )
        
        # Generate style with nature photography techniques
        if include_style:
            style = self._get_random_choice("nature.styles")
            technique = self._get_random_choice("nature.techniques")
            lighting = self._get_random_choice("nature.lighting_conditions")
            components["style"] = (
                f"((captured in {style} style)), ((using {technique})), "
                f"((with {lighting})), ((landscape photography excellence)), "
                f"((environmental artistry)), ((perfect natural composition)), "
                f"((8k resolution)), ((professional landscape photography)), "
                f"((award-winning landscape photograph)), ((National Geographic style))"
            )
        
        # Generate effects with natural elements
        if include_effects:
            effect = self._get_random_choice("nature.effects")
            pattern = self._get_random_choice("nature.natural_patterns")
            components["effects"] = (
                f"with ((natural {effect})), ((subtle {pattern})), "
                f"((environmental authenticity)), ((natural atmosphere)), "
                f"((natural color grading)), ((pristine conditions)), "
                f"((perfect exposure)), ((sharp details)), ((rich textures))"
            )
        
        return components