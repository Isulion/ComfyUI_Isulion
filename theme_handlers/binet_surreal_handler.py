from typing import Dict
from .base_handler import BaseThemeHandler

class BinetSurrealThemeHandler(BaseThemeHandler):
    """Handler for Binet surreal-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Binet surreal-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((surreal {custom_subject})), "
                f"((dreamlike imagery)), ((surreal composition)), "
                f"((Binet style))"
            )
        else:
            subject = self._get_random_choice("binet_surreal.subjects")
            element = self._get_random_choice("binet_surreal.elements")
            symbol = self._get_random_choice("binet_surreal.symbols")
            components["subject"] = (
                f"((surreal {subject})) with ((dreamlike {element})), "
                f"((featuring {symbol})), ((surreal composition)), "
                f"((Binet style)), ((symbolic imagery))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((surreal {custom_location})) with "
                    f"((dreamlike setting)), ((surreal atmosphere))"
                )
            else:
                setting = self._get_random_choice("binet_surreal.settings")
                feature = self._get_random_choice("binet_surreal.features")
                components["environment"] = (
                    f"in ((surreal {setting})) with "
                    f"((dreamlike {feature})), "
                    f"((surreal atmosphere)), ((symbolic surroundings)), "
                    f"((Binet environment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("binet_surreal.styles")
            technique = self._get_random_choice("binet_surreal.techniques")
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((using {technique} technique)), "
                f"((surreal aesthetics)), ((Binet artistry)), "
                f"((dreamlike quality))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("binet_surreal.effects")
            mood = self._get_random_choice("binet_surreal.moods")
            components["effects"] = (
                f"with ((surreal {effect} effects)), "
                f"((dreamlike {mood} mood)), "
                f"((symbolic atmosphere)), ((Binet essence))"
            )
        
        return components
