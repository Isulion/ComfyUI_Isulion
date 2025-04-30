from typing import Dict
from .base_handler import BaseThemeHandler

class BioOrganicTechThemeHandler(BaseThemeHandler):
    """Handler for bio-organic technology-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate bio-organic technology-themed components."""
        components = {}

        # Always use random elements, even with custom_subject
        form = self._get_random_choice("bio_organic_tech.forms")
        feature = self._get_random_choice("bio_organic_tech.features")

        if custom_subject:
            components["subject"] = (
                f"((bio-organic tech {custom_subject})) with ((organic {form})), "
                f"((featuring {feature})), ((biomechanical design)), "
                f"((living technology)), ((organic machinery))"
            )
        else:
            entity = self._get_random_choice("bio_organic_tech.entities")
            components["subject"] = (
                f"((bio-organic {entity})) with ((organic {form})), "
                f"((featuring {feature})), ((biomechanical design)), "
                f"((living technology)), ((organic machinery))"
            )

        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((bio-organic {custom_location})) with "
                    f"((living technology)), ((organic machinery))"
                )
            else:
                environment = self._get_random_choice("bio_organic_tech.environments")
                element = self._get_random_choice("bio_organic_tech.elements")
                components["environment"] = (
                    f"in ((bio-organic {environment})) with "
                    f"((organic {element})), "
                    f"((living technology)), ((biomechanical surroundings)), "
                    f"((organic tech environment))"
                )

        # Generate style if requested
        if include_style:
            style = self._get_random_choice("bio_organic_tech.styles")
            aesthetic = self._get_random_choice("bio_organic_tech.aesthetics")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetic)), "
                f"((bio-organic design)), ((living tech artistry)), "
                f"((organic machinery aesthetics))"
            )

        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("bio_organic_tech.effects")
            energy = self._get_random_choice("bio_organic_tech.energies")
            components["effects"] = (
                f"with ((bio-organic {effect} effects)), "
                f"((organic {energy} energy)), "
                f"((living tech glow)), ((biomechanical aura))"
            )

        return components
