from typing import Dict
from .base_handler import BaseThemeHandler

class ConceptArtThemeHandler(BaseThemeHandler):
    """Handler for concept art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate concept art-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((concept art {custom_subject})), "
                f"((design visualization)), ((concept design)), "
                f"((pre-production art))"
            )
        else:
            subject = self._get_random_choice("concept_art.subjects")
            design = self._get_random_choice("concept_art.designs")
            feature = self._get_random_choice("concept_art.features")
            components["subject"] = (
                f"((concept art {subject} with {design} design)), "
                f"((featuring {feature})), ((design visualization)), "
                f"((concept design)), ((pre-production art))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((concept art {custom_location})) with "
                    f"((design setting)), ((visualization environment))"
                )
            else:
                setting = self._get_random_choice("concept_art.settings")
                element = self._get_random_choice("concept_art.elements")
                components["environment"] = (
                    f"in ((concept art {setting})) with "
                    f"((design {element})), "
                    f"((visualization environment)), ((concept background)), "
                    f"((pre-production setting))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("concept_art.styles")
            technique = self._get_random_choice("concept_art.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((concept design)), ((visualization artistry)), "
                f"((pre-production quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("concept_art.effects")
            mood = self._get_random_choice("concept_art.moods")
            components["effects"] = (
                f"with ((concept art {effect} effects)), "
                f"((design {mood} mood)), "
                f"((visualization impact)), ((pre-production finish))"
            )
        
        return components
