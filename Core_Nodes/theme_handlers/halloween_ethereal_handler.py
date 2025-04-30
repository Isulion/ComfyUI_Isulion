from typing import Dict
from .base_handler import BaseThemeHandler

class HalloweenEtherealThemeHandler(BaseThemeHandler):
    """Handler for halloween ethereal-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate halloween ethereal-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        creature = self._get_random_choice("halloween_ethereal.creatures")
        obj = self._get_random_choice("halloween_ethereal.objects")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((ethereal {custom_subject})), "
                f"((with {creature})), ((holding {obj})), "
                f"((halloween spirit)), ((mystical being)), "
                f"((supernatural entity))"
            )
        else:
            subject = self._get_random_choice("halloween_ethereal.subjects")
            creature = self._get_random_choice("halloween_ethereal.creatures")
            obj = self._get_random_choice("halloween_ethereal.objects")
            components["subject"] = (
                f"(({subject})), "
                f"((with {creature})), ((holding {obj})), "
                f"((halloween spirit)), ((mystical being))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((ethereal {custom_location})) with "
                    f"((haunted setting)), ((mystical environment))"
                )
            else:
                environment = self._get_random_choice("halloween_ethereal.environments")
                time = self._get_random_choice("halloween_ethereal.time")
                atmosphere = self._get_random_choice("halloween_ethereal.atmospheres")
                components["environment"] = (
                    f"in (({environment})) during (({time})) with "
                    f"(({atmosphere} atmosphere)), "
                    f"((haunted vista)), ((mystical scene))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("halloween_ethereal.styles")
            components["style"] = (
                f"((styled in {style})), "
                f"((ethereal aesthetic)), "
                f"((haunting beauty)), ((mystical design)), "
                f"((supernatural elegance))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("halloween_ethereal.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((ethereal atmosphere)), "
                f"((mystical ambiance)), ((haunted environment))"
            )
        
        return components
