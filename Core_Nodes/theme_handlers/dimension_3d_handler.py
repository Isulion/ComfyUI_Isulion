from typing import Dict
from .base_handler import BaseThemeHandler

class Dimension3DThemeHandler(BaseThemeHandler):
    """Handler for 3D dimension-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate 3D dimension-themed components."""
        components = {}

        # Always use random elements, even with custom_subject
        style = self._get_random_choice("dimension_3d.styles")
        feature = self._get_random_choice("dimension_3d.features")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((3D {custom_subject} in {style} style)), "
                f"((featuring {feature})), ((3D modeling)), "
                f"((dimensional design)), ((3D rendering))"
            )
        else:
            subject = self._get_random_choice("dimension_3d.subjects")
            style = self._get_random_choice("dimension_3d.styles")
            feature = self._get_random_choice("dimension_3d.features")
            components["subject"] = (
                f"((3D {subject} in {style} style)), "
                f"((featuring {feature})), ((3D modeling)), "
                f"((dimensional design)), ((3D rendering))"
            )

        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((3D {custom_location})) with "
                    f"((3D environment)), ((dimensional space))"
                )
            else:
                setting = self._get_random_choice("dimension_3d.settings")
                element = self._get_random_choice("dimension_3d.elements")
                components["environment"] = (
                    f"in ((3D {setting})) with "
                    f"((3D {element})), "
                    f"((dimensional environment)), ((3D space)), "
                    f"((rendered world))"
                )

        # Generate style if requested
        if include_style:
            render_style = self._get_random_choice("dimension_3d.render_styles")
            technique = self._get_random_choice("dimension_3d.techniques")
            components["style"] = (
                f"((rendered in {render_style} style)), "
                f"((using {technique} technique)), "
                f"((3D quality)), ((dimensional artistry)), "
                f"((professional 3D))"
            )

        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("dimension_3d.effects")
            lighting = self._get_random_choice("dimension_3d.lighting")
            components["effects"] = (
                f"with ((3D {effect} effects)), "
                f"((dimensional {lighting} lighting)), "
                f"((3D finish)), ((render quality))"
            )

        return components
