from typing import Dict
from .base_handler import BaseThemeHandler

class DigitalArtThemeHandler(BaseThemeHandler):
    """Handler for digital art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate digital art-themed components with professional quality."""
        components = {}
        
        # Generate subject with enhanced digital art characteristics
        if custom_subject:
            components["subject"] = (
                f"((masterful digital art)) of {custom_subject}, "
                f"((perfect digital rendering)), ((professional illustration)), "
                f"((artistic excellence)), ((digital mastery)), "
                f"((detailed design)), ((creative brilliance))"
            )
        else:
            subject = self._get_random_choice("digital_art.subjects")
            style = self._get_random_choice("digital_art.styles")
            technique = self._get_random_choice("digital_art.techniques")
            components["subject"] = (
                f"((masterful digital art)) of ((detailed {subject})), "
                f"((rendered in {style} style)), ((using {technique})), "
                f"((professional illustration)), ((digital excellence)), "
                f"((perfect execution)), ((artistic mastery))"
            )
        
        # Generate environment with enhanced digital atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((digitally mastered {custom_location})) with "
                    f"((perfect environmental detail)), ((digital atmosphere)), "
                    f"((scene composition excellence)), ((artistic environment)), "
                    f"((professional background)), ((digital world building))"
                )
            else:
                environment = self._get_random_choice("digital_art.environments")
                lighting = self._get_random_choice("digital_art.lighting")
                mood = self._get_random_choice("digital_art.moods")
                components["environment"] = (
                    f"in ((digitally mastered {environment})) with "
                    f"((perfect {lighting} lighting)), ((masterful {mood} atmosphere)), "
                    f"((digital excellence)), ((scene composition)), "
                    f"((environmental harmony)), ((artistic depth))"
                )
        
        # Generate style with enhanced digital techniques
        if include_style == "yes":
            workflow = self._get_random_choice("digital_art.workflows")
            software = self._get_random_choice("digital_art.software")
            color_scheme = self._get_random_choice("digital_art.color_schemes")
            components["style"] = (
                f"((masterfully created using {workflow})), "
                f"((professional {software} techniques)), "
                f"((perfect {color_scheme} color palette)), "
                f"((digital art excellence)), ((technical mastery)), "
                f"((artistic sophistication)), ((perfect composition)), "
                f"((color harmony)), 8k resolution"
            )
        
        # Generate effects with enhanced digital elements
        if include_effects == "yes":
            effect = self._get_random_choice("digital_art.effects")
            filter = self._get_random_choice("digital_art.filters")
            texture = self._get_random_choice("digital_art.textures")
            components["effects"] = (
                f"with ((perfect digital {effect})), "
                f"((masterful {filter} filter)), ((beautiful {texture} textures)), "
                f"((professional effects)), ((digital excellence)), "
                f"((artistic finish)), ((visual mastery))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common digital art issues."""
        return (
            "((amateur)), ((poor technique)), ((bad composition)), ((inconsistent style)), "
            "((poor color harmony)), ((pixelated)), ((low resolution)), ((jpeg artifacts)), "
            "((banding)), ((color banding)), ((poor shading)), ((flat colors)), "
            "((poor lighting)), ((bad perspective)), ((anatomical errors)), "
            "((uncanny)), ((artificial looking)), ((oversaturated)), ((undersaturated)), "
            "((poor contrast)), ((muddy colors)), ((harsh edges)), ((poor blending)), "
            "((missing details)), ((lazy brushwork)), ((unrefined)), ((amateurish))"
        )
