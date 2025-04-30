from typing import Dict
import random
from .base_handler import BaseThemeHandler

class LogoThemeHandler(BaseThemeHandler):
    """Handler for logo-themed prompt generation."""
    
    # Default fallback values for various style elements
    _3D_STYLE_FALLBACKS = ["metallic", "glossy", "matte", "crystal", "glass", "chrome"]
    _3D_EFFECTS_FALLBACKS = ["reflection", "metallic sheen", "glass refraction", "ambient occlusion"]
    _CHARACTER_EFFECTS_FALLBACKS = ["sparkle", "glow", "soft shadow", "highlight"]
    _MASCOT_OPTIONS = [
        "cute mascot", "friendly character", "abstract character",
        "geometric character", "playful mascot", "simple character",
        "minimalist mascot", "modern character", "unique mascot"
    ]
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate logo-themed components."""
        components = {}
        
        # Determine logo style approach with adjusted weights
        style_approach = random.choices(
            ["classic", "3D", "character", "artistic"],
            weights=[0.6, 0.2, 0.05, 0.15]
        )[0]
        
        # Use custom subject if provided
        logo_text = custom_subject.strip() if custom_subject else "ISULION"
        
        if style_approach == "classic":
            style = self._get_random_choice("logo.styles")
            typography = self._get_random_choice("logo.typography")
            element = self._get_random_choice("logo.elements")
            color_scheme = self._get_random_choice("logo.color_schemes")
            
            components["subject"] = (
                f"((professional {style} logo design)) with the text \"{logo_text}\", "
                f"((using {typography} typography)), ((perfect letter spacing)), "
                f"((masterful font design)), ((vector quality))"
            )
            
        elif style_approach == "3D":
            # Try to get 3D style from config, fallback to default if not available
            try:
                style_3d = self._get_random_choice("logo.3d_styles")
            except:
                style_3d = random.choice(self._3D_STYLE_FALLBACKS)
            
            components["subject"] = (
                f"((highly detailed {style_3d} 3D typography)) of the text \"{logo_text}\", "
                f"((volumetric letters)), ((dimensional depth)), "
                f"((perfect 3D modeling)), ((ultra-detailed materials))"
            )
            
        elif style_approach == "character":
            character = random.choice(self._MASCOT_OPTIONS)
            decorative = self._get_random_choice("logo.elements")
            
            components["subject"] = (
                f"((adorable {character} mascot logo)) with the text \"{logo_text}\", "
                f"((professional {character} logo)) with the text \"{logo_text}\", "
                f"((cute character design)), ((playful typography)), "
                f"((charming illustration)), ((logo style))"
            )
            
        else:  # artistic
            theme = self._get_random_choice("logo.styles")
            decorative = self._get_random_choice("logo.elements")
            
            components["subject"] = (
                f"((creative {theme} logo artwork)) with the text \"{logo_text}\", "
                f"((artistic typography)), ((illustrated elements)), "
                f"((unique design)), ((hand-crafted style))"
            )
        
        # Generate environment if requested
        if include_environment:
            if style_approach == "3D":
                components["environment"] = (
                    f"with ((perfect lighting setup)), ((studio environment)), "
                    f"((professional composition)), ((clean background))"
                )
            elif style_approach == "character":
                decorative = self._get_random_choice("logo.elements")
                components["environment"] = (
                    f"with ((cute {decorative})), ((playful composition)), "
                    f"((charming background)), ((balanced layout))"
                )
            else:
                element = self._get_random_choice("logo.elements")
                components["environment"] = (
                    f"with ((clean {element})), ((perfect composition)), "
                    f"((balanced negative space)), ((professional layout))"
                )
        
        # Generate style if requested
        if include_style:
            if style_approach == "3D":
                components["style"] = (
                    f"((premium 3D rendering)), ((perfect materials)), "
                    f"((professional lighting)), ((high-end finish)), "
                    f"((commercial quality)), ((volumetric effects)), "
                    f"((brand identity)), 8k resolution"
                )
            elif style_approach == "character":
                components["style"] = (
                    f"((kawaii aesthetic)), ((cute color palette)), "
                    f"((playful design)), ((perfect proportions)), "
                    f"((charming style)), ((mascot branding)), "
                    f"((brand identity)), 8k resolution"
                )
            else:
                color_scheme = self._get_random_choice("logo.color_schemes")
                components["style"] = (
                    f"((premium {color_scheme} palette)), ((vector art)), "
                    f"((professional design)), ((perfect proportions)), "
                    f"((commercial quality)), ((scalable graphics)), "
                    f"((brand identity)), 8k resolution"
                )
        
        # Generate effects if requested
        if include_effects:
            if style_approach == "3D":
                try:
                    effect = self._get_random_choice("logo.3d_effects")
                except:
                    effect = random.choice(self._3D_EFFECTS_FALLBACKS)
                    
                components["effects"] = (
                    f"with (({effect})), ((perfect shadows)), "
                    f"((realistic materials)), ((professional rendering)), "
                    f"((3D effects)), ((depth and volume))"
                )
            elif style_approach == "character":
                try:
                    effect = self._get_random_choice("logo.character_effects")
                except:
                    effect = random.choice(self._CHARACTER_EFFECTS_FALLBACKS)
                    
                components["effects"] = (
                    f"with (({effect})), ((sweet details)), "
                    f"((playful elements)), ((charming finish)), "
                    f"((mascot personality)), ((cute aesthetics))"
                )
            else:
                effect = self._get_random_choice("logo.effects")
                components["effects"] = (
                    f"with (({effect})), ((clean edges)), "
                    f"((perfect symmetry)), ((professional finish)), "
                    f"((brand consistency)), ((timeless design))"
                )
        
        return components
