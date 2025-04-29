from typing import Dict
from .base_handler import BaseThemeHandler

class FuturisticSciFiThemeHandler(BaseThemeHandler):
    """Handler for futuristic sci-fi-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate futuristic sci-fi-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        tech = self._get_random_choice("futuristic_scifi.technology")
        artifact = self._get_random_choice("futuristic_scifi.artifacts")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((futuristic {custom_subject})), "
                f"((wielding {tech})), ((with {artifact})), "
                f"((science fiction)), ((advanced being)), "
                f"((cosmic entity))"
            )
        else:
            subject = self._get_random_choice("futuristic_scifi.subjects")
            tech = self._get_random_choice("futuristic_scifi.technology")
            artifact = self._get_random_choice("futuristic_scifi.artifacts")
            components["subject"] = (
                f"(({subject})), "
                f"((wielding {tech})), ((with {artifact})), "
                f"((science fiction)), ((advanced being))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})) with "
                    f"((sci-fi setting)), ((cosmic environment))"
                )
            else:
                environment = self._get_random_choice("futuristic_scifi.environments")
                atmosphere = self._get_random_choice("futuristic_scifi.atmospheres")
                components["environment"] = (
                    f"in (({environment})) with "
                    f"(({atmosphere} atmosphere)), "
                    f"((cosmic vista)), ((otherworldly scene))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("futuristic_scifi.styles")
            detail = self._get_random_choice("futuristic_scifi.details")
            components["style"] = (
                f"((styled in {style})), "
                f"(({detail} aesthetic)), "
                f"((sci-fi precision)), ((advanced design)), "
                f"((futuristic technology))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("futuristic_scifi.effects")
            components["effects"] = (
                f"with (({effect} effects)), "
                f"((cosmic atmosphere)), "
                f"((sci-fi ambiance)), ((otherworldly environment))"
            )
        
        return components
