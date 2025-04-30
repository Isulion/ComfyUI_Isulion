from typing import Dict, List, Optional
from .base_handler import BaseThemeHandler
import random

class PuzzleDimensionThemeHandler(BaseThemeHandler):
    """Handler for the Puzzle Dimension theme, featuring M.C. Escher-inspired impossible geometries."""

    def generate(self, custom_subject: str = "", 
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate a puzzle dimension themed prompt with impossible geometries and mathematical patterns."""
        
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((masterful geometric rendition)) of {custom_subject}, "
                f"((M.C. Escher style)), ((impossible geometry)), "
                f"((mathematical precision)), ((intricate patterns))"
            )
        else:
            subject = random.choice(self.get_subject_modifiers())
            components["subject"] = (
                f"((masterful geometric {subject})), "
                f"((M.C. Escher style)), ((impossible geometry)), "
                f"((mathematical precision)), ((intricate patterns))"
            )
        
        # Generate environment
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((geometrically impossible {custom_location})) with "
                    f"((recursive patterns)), ((mathematical precision)), "
                    f"((spatial paradox)), ((geometric harmony))"
                )
            else:
                location = random.choice([
                    "impossible space",
                    "geometric void",
                    "mathematical dimension",
                    "recursive realm",
                    "tessellated universe",
                    "paradox chamber"
                ])
                components["environment"] = (
                    f"in ((geometrically impossible {location})) with "
                    f"((recursive patterns)), ((mathematical precision)), "
                    f"((spatial paradox)), ((geometric harmony))"
                )
        
        # Add style elements
        if include_style:
            style = random.choice(self.get_style_modifiers())
            lighting = random.choice(self.get_lighting_modifiers())
            color = random.choice(self.get_color_modifiers())
            composition = random.choice(self.get_composition_modifiers())
            
            components["style"] = (
                f"((masterful {style})), ((perfect {lighting})), "
                f"((beautiful {color})), ((stunning {composition})), "
                f"((high detail)), ((professional quality))"
            )
        
        # Add special effects
        if include_effects:
            effect = random.choice(self.get_special_effects())
            components["effects"] = (
                f"((dramatic {effect})), ((geometric transitions)), "
                f"((mathematical transformations)), ((spatial warping))"
            )
        
        # Add negative prompt
        components["negative"] = ", ".join(random.sample(self.get_negative_prompts(), min(5, len(self.get_negative_prompts()))))
        
        return components

    def get_style_modifiers(self) -> List[str]:
        return [
            "M.C. Escher style",
            "impossible geometry",
            "mathematical art",
            "geometric paradox",
            "optical illusion",
            "recursive patterns",
            "tessellation art",
            "perspective illusion",
            "mathematical beauty",
            "geometric abstraction"
        ]

    def get_subject_modifiers(self) -> List[str]:
        return [
            "impossible staircase",
            "recursive architecture",
            "interlocking shapes",
            "geometric patterns",
            "mathematical structures",
            "tessellated buildings",
            "paradoxical spaces",
            "infinite loops",
            "geometric fractals",
            "spatial illusions"
        ]

    def get_lighting_modifiers(self) -> List[str]:
        return [
            "geometric shadows",
            "paradoxical lighting",
            "recursive reflections",
            "mathematical light patterns",
            "impossible shadows",
            "crystalline lighting",
            "prismatic light",
            "dimensional glow",
            "tessellated shadows",
            "geometric light rays"
        ]

    def get_color_modifiers(self) -> List[str]:
        return [
            "mathematical color patterns",
            "geometric color gradients",
            "recursive color schemes",
            "tessellated colors",
            "impossible color transitions",
            "prismatic patterns",
            "paradoxical color harmony",
            "crystalline color palette",
            "dimensional color shifts",
            "sacred geometry colors"
        ]

    def get_composition_modifiers(self) -> List[str]:
        return [
            "recursive composition",
            "impossible perspective",
            "geometric balance",
            "mathematical symmetry",
            "tessellated layout",
            "paradoxical depth",
            "dimensional framing",
            "sacred geometry composition",
            "geometric golden ratio",
            "spatial paradox arrangement"
        ]

    def get_negative_prompts(self) -> List[str]:
        return [
            "chaotic",
            "messy",
            "organic",
            "natural",
            "realistic",
            "random patterns",
            "asymmetrical",
            "irregular shapes",
            "disordered",
            "unstructured"
        ]

    def get_special_effects(self) -> List[str]:
        return [
            "geometric transitions",
            "recursive portals",
            "impossible doorways",
            "mathematical transformations",
            "tessellation morphing",
            "paradoxical reflections",
            "dimensional rifts",
            "geometric anomalies",
            "spatial warps",
            "crystalline distortions"
        ]
