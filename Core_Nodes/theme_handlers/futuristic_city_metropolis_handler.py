from typing import Dict
from .base_handler import BaseThemeHandler

class FuturisticCityMetropolisThemeHandler(BaseThemeHandler):
    """Handler for futuristic city metropolis-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate futuristic city metropolis-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((futuristic {custom_subject})), "
                f"((advanced cityscape)), ((metropolis)), "
                f"((urban future))"
            )
        else:
            subject = self._get_random_choice("futuristic_city_metropolis.subjects")
            architecture = self._get_random_choice("futuristic_city_metropolis.architecture")
            tech = self._get_random_choice("futuristic_city_metropolis.technology")
            components["subject"] = (
                f"(({architecture} {subject})), "
                f"((integrated with {tech})), ((metropolis)), "
                f"((urban future)), ((advanced cityscape))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})) with "
                    f"((advanced urban setting)), ((city environment))"
                )
            else:
                infrastructure = self._get_random_choice("futuristic_city_metropolis.infrastructure")
                time = self._get_random_choice("futuristic_city_metropolis.time_of_day")
                atmosphere = self._get_random_choice("futuristic_city_metropolis.atmospheres")
                components["environment"] = (
                    f"in (({atmosphere} metropolis)) with "
                    f"(({infrastructure})), during (({time})), "
                    f"((urban vista)), ((city panorama))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("futuristic_city_metropolis.styles")
            detail = self._get_random_choice("futuristic_city_metropolis.details")
            components["style"] = (
                f"((styled in {style})), "
                f"(({detail} aesthetic)), "
                f"((urban precision)), ((advanced design)), "
                f"((futuristic architecture))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("futuristic_city_metropolis.effects")
            components["effects"] = (
                f"with (({effect} effects)), "
                f"((urban atmosphere)), "
                f"((city ambiance)), ((metropolitan environment))"
            )
        
        return components
