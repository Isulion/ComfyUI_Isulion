from typing import Dict
import random
from .base_handler import BaseThemeHandler

class BinetSurrealThemeHandler(BaseThemeHandler):
    """Handler for Binet surreal-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Binet surreal-themed components with enhanced portrait styles."""
        components = {}
        
        # Get custom inputs
        custom_subject = custom_subject.strip()
        custom_location = custom_location.strip()
        
        # Determine if using color or black and white
        is_color = random.random() < 0.9  # 90% chance for color
        portrait_style = self._get_random_choice("binet_surreal.portrait_styles")
        
        if is_color:
            color_scheme = self._get_random_choice("binet_surreal.color_schemes")
            style_prefix = f"sophisticated {portrait_style}"
            color_emphasis = f", {color_scheme}"
        else:
            style_prefix = f"sophisticated black and white {portrait_style}"
            color_emphasis = ", ((dramatic black and white)), ((extreme contrast))"
        
        if custom_subject:
            components["subject"] = (
                f"((surreal anthropomorphic portrait)) of {custom_subject}, "
                f"((aristocratic pose)), ((noble expression)), "
                f"((intricate detail)), ((dramatic studio lighting)){color_emphasis}, "
                f"((dreamlike atmosphere)), ((surreal composition))"
            )
        else:
            # Select a distinguished animal
            animal = self._get_random_choice("binet_surreal.animals")
            character_theme = self._get_random_choice("binet_surreal.character_themes")
            costume = self._get_random_choice("binet_surreal.costumes")
            props = self._get_random_choice("binet_surreal.props")
            
            # Determine if contemporary or classical theme
            if random.random() < 0.3:  # 30% chance for contemporary
                theme_type = "contemporary"
                clothing = self._get_random_choice("binet_surreal.contemporary_clothing")
                elements = self._get_random_choice("binet_surreal.urban_elements")
            else:
                theme_type = "classical"
                clothing = self._get_random_choice("binet_surreal.classical_clothing")
                elements = self._get_random_choice("binet_surreal.classical_elements")
            
            components["subject"] = (
                f"((surreal anthropomorphic {portrait_style} portrait)) of a ((distinguished {animal})) "
                f"as a ((noble {character_theme})), ((wearing {costume})), "
                f"((with {props})), ((dressed in {clothing})), "
                f"((aristocratic pose)), ((noble expression)), "
                f"((intricate detail)), ((dramatic studio lighting)){color_emphasis}, "
                f"((dreamlike atmosphere)), ((surreal composition))"
            )
        
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((surreal {custom_location})) with ((dreamlike setting)), "
                    f"((surreal atmosphere)), ((mystical elements)), "
                    f"((floating objects)), ((impossible architecture))"
                )
            else:
                setting = self._get_random_choice("binet_surreal.settings")
                feature = self._get_random_choice("binet_surreal.features")
                components["environment"] = (
                    f"in ((surreal {setting})) with ((dreamlike {feature})), "
                    f"((surreal atmosphere)), ((mystical elements)), "
                    f"((floating objects)), ((impossible architecture))"
                )
        
        if include_style == "yes":
            style = self._get_random_choice("binet_surreal.styles")
            technique = self._get_random_choice("binet_surreal.techniques")
            components["style"] = (
                f"{style_prefix}, ((masterful composition)), "
                f"((professional studio lighting)), ((sharp focus)), "
                f"((photorealistic detail)), ((cinematic framing)), "
                f"((surreal aesthetics)), ((using {technique} technique)), "
                f"((dreamlike quality)), 8k resolution{color_emphasis}"
            )
        
        if include_effects == "yes":
            effect = self._get_random_choice("binet_surreal.effects")
            mood = self._get_random_choice("binet_surreal.moods")
            components["effects"] = (
                f"with ((surreal {effect} effects)), ((dreamlike {mood} mood)), "
                f"((deep shadows)), ((bright highlights)), "
                f"((dramatic atmosphere)), ((volumetric lighting)), "
                f"((perfect exposure)), ((subtle vignette)), "
                f"((symbolic atmosphere)), ((mystical glow))"
            )
        
        return components
