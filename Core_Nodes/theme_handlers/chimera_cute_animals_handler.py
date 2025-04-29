from typing import Dict
from .base_handler import BaseThemeHandler

class ChimeraCuteAnimalsThemeHandler(BaseThemeHandler):
    """Handler for chimera cute animals-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate chimera cute animals-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        feature = self._get_random_choice("chimera_cute_animals.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((cute chimeric {custom_subject})), "
                f"((featuring {feature})), ((adorable hybrid)), "
                f"((kawaii creature)), ((magical pet))"
            )
        else:
            base = self._get_random_choice("chimera_cute_animals.base_creatures")
            fusion = self._get_random_choice("chimera_cute_animals.fusion_parts")
            feature = self._get_random_choice("chimera_cute_animals.features")
            components["subject"] = (
                f"((cute {base} with {fusion})), "
                f"((featuring {feature})), ((adorable hybrid)), "
                f"((kawaii creature)), ((magical pet))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((cute {custom_location})) with "
                    f"((adorable setting)), ((kawaii environment))"
                )
            else:
                habitat = self._get_random_choice("chimera_cute_animals.habitats")
                element = self._get_random_choice("chimera_cute_animals.elements")
                components["environment"] = (
                    f"in ((cute {habitat})) with "
                    f"((adorable {element})), "
                    f"((kawaii setting)), ((magical surroundings)), "
                    f"((charming realm))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("chimera_cute_animals.styles")
            aesthetic = self._get_random_choice("chimera_cute_animals.aesthetics")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetic)), "
                f"((kawaii design)), ((adorable artistry)), "
                f"((cute quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("chimera_cute_animals.effects")
            aura = self._get_random_choice("chimera_cute_animals.auras")
            components["effects"] = (
                f"with ((magical {effect} effects)), "
                f"((adorable {aura} aura)), "
                f"((kawaii energy)), ((cute glow))"
            )
        
        return components
