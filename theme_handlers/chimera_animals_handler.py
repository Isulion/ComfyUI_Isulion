from typing import Dict
from .base_handler import BaseThemeHandler

class ChimeraAnimalsThemeHandler(BaseThemeHandler):
    """Handler for chimera animals-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate chimera animals-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((chimeric {custom_subject})), "
                f"((hybrid creature)), ((mythical fusion)), "
                f"((fantastic beast))"
            )
        else:
            base = self._get_random_choice("chimera_animals.base_creatures")
            fusion = self._get_random_choice("chimera_animals.fusion_parts")
            feature = self._get_random_choice("chimera_animals.features")
            components["subject"] = (
                f"((chimeric {base} with {fusion})), "
                f"((featuring {feature})), ((hybrid creature)), "
                f"((mythical fusion)), ((fantastic beast))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((mythical {custom_location})) with "
                    f"((fantastic setting)), ((magical environment))"
                )
            else:
                habitat = self._get_random_choice("chimera_animals.habitats")
                element = self._get_random_choice("chimera_animals.elements")
                components["environment"] = (
                    f"in ((mythical {habitat})) with "
                    f"((magical {element})), "
                    f"((fantastic setting)), ((mystical surroundings)), "
                    f"((chimeric realm))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("chimera_animals.styles")
            aesthetic = self._get_random_choice("chimera_animals.aesthetics")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetic)), "
                f"((chimeric design)), ((mythical artistry)), "
                f"((fantastic quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("chimera_animals.effects")
            aura = self._get_random_choice("chimera_animals.auras")
            components["effects"] = (
                f"with ((magical {effect} effects)), "
                f"((mystical {aura} aura)), "
                f"((chimeric energy)), ((fantastic glow))"
            )
        
        return components
