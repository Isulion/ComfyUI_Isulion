from typing import Dict
import random
from .base_handler import BaseThemeHandler

class BinetSurrealThemeHandler(BaseThemeHandler):
    """Handler for Binet surreal-themed prompt generation in the style of Sylvain Binet's sophisticated animal portraits."""
    
    def get_negative_prompt(self) -> str:
        """Get negative prompt to avoid unwanted styles."""
        negative_elements = self._get_random_choices("binet_surreal.negative_prompts", 8)
        return ", ".join(negative_elements)

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate sophisticated animal portrait components in Sylvain Binet's style."""
        components = {}
        
        # Get custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Core style elements
        portrait_style = self._get_random_choice("binet_surreal.portrait_styles")
        color_scheme = self._get_random_choice("binet_surreal.color_schemes")
        
        if custom_subject:
            # Add randomization to custom subject
            pose = self._get_random_choice("binet_surreal.poses") if hasattr(self, "_get_random_choice") else "aristocratic pose"
            detail = self._get_random_choice("binet_surreal.details") if hasattr(self, "_get_random_choice") else "photorealistic detail"
            lighting = self._get_random_choice("binet_surreal.lighting") if hasattr(self, "_get_random_choice") else "dramatic studio lighting"
            components["subject"] = (
                f"((masterful {portrait_style})) of {custom_subject}, "
                f"(({pose})), ((noble bearing)), "
                f"(({detail})), (({lighting})), "
                f"in {color_scheme} tones, ((professional photography))"
            )
        else:
            # Select animal and character elements
            animal = self._get_random_choice("binet_surreal.animals")
            character_theme = self._get_random_choice("binet_surreal.character_themes")
            costume = self._get_random_choice("binet_surreal.costumes")
            props = self._get_random_choice("binet_surreal.props")
            clothing = self._get_random_choice("binet_surreal.classical_clothing")
            
            components["subject"] = (
                f"((masterful {portrait_style})) of a ((distinguished {animal})) "
                f"as a ((noble {character_theme})), ((wearing {costume} and {clothing})), "
                f"((adorned with {props})), ((aristocratic pose)), ((noble expression)), "
                f"((photorealistic detail)), ((dramatic studio lighting)), "
                f"in {color_scheme} tones, ((professional photography))"
            )
        
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in {custom_location}, ((elegant studio setting)), "
                    f"((subtle gradient background)), ((professional lighting setup)), "
                    f"((clean composition))"
                )
            else:
                elements = self._get_random_choice("binet_surreal.classical_elements")
                components["environment"] = (
                    f"in ((elegant studio setting)) with {elements}, "
                    f"((subtle gradient background)), ((professional lighting setup)), "
                    f"((clean composition))"
                )
        
        if include_style:
            components["style"] = (
                f"((masterful oil painting technique)), ((photorealistic detail)), "
                f"((professional studio photography)), ((sharp focus)), "
                f"((perfect composition)), ((dramatic lighting)), "
                f"((rich color grading)), ((elegant aesthetics)), "
                f"8k resolution, ((award-winning portrait))"
            )
        
        if include_effects:
            components["effects"] = (
                f"with ((dramatic shadows)), ((perfect exposure)), "
                f"((volumetric lighting)), ((subtle vignette)), "
                f"((rich contrast)), ((color harmony)), "
                f"((professional retouching)), ((gallery quality))"
            )
        
        return components
