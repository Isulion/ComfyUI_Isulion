from typing import Dict
from .base_handler import BaseThemeHandler

class AbstractThemeHandler(BaseThemeHandler):
    """Handler for abstract-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate abstract-themed components with enhanced emphasis and detail."""
        components = {}
        
        # Generate subject with enhanced artistic emphasis
        if custom_subject:
            components["subject"] = (
                f"((masterful abstract interpretation)) of {custom_subject}, "
                f"((with dynamic fluid motion)), ((sophisticated minimalist design)), "
                f"((perfect geometric harmony)), ((artistic composition)), "
                f"((abstract excellence))"
            )
        else:
            shape = self._get_random_choice("abstract.shapes")
            motion = self._get_random_choice("abstract.motions")
            color_scheme = self._get_random_choice("abstract.color_schemes")
            components["subject"] = (
                f"((masterful abstract {shape} composition)) with ((dynamic {motion})), "
                f"((featuring harmonious {color_scheme} color scheme)), "
                f"((sophisticated minimalist design)), ((perfect geometric harmony)), "
                f"((artistic excellence)), ((compositional balance))"
            )
        
        # Generate environment with enhanced spatial elements
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((artistically textured {custom_location} space)) with "
                    f"((intricate abstract patterns)), ((perfect spatial composition)), "
                    f"((dimensional harmony)), ((abstract environment mastery))"
                )
            else:
                texture = self._get_random_choice("abstract.textures")
                pattern = self._get_random_choice("abstract.patterns")
                components["environment"] = (
                    f"in ((artistically textured {texture} space)) with "
                    f"((intricate {pattern} elements)), ((perfect spatial composition)), "
                    f"((sophisticated dimensional depth)), ((abstract environment mastery)), "
                    f"((harmonious background))"
                )
        
        # Generate style with enhanced artistic techniques
        if include_style == "yes":
            style = self._get_random_choice("abstract.styles")
            technique = self._get_random_choice("abstract.techniques")
            components["style"] = (
                f"((masterful {style} execution)), ((abstract art excellence)), "
                f"((sophisticated minimalist aesthetic)), ((perfect geometric precision)), "
                f"((enhanced with professional {technique})), ((artistic mastery)), "
                f"((flawless composition)), ((color harmony)), 8k resolution"
            )
        
        # Generate effects with enhanced artistic elements
        if include_effects == "yes":
            effect = self._get_random_choice("abstract.effects")
            components["effects"] = (
                f"with ((dynamic {effect} effect)), ((sophisticated abstract patterns)), "
                f"((perfect geometric flow)), ((harmonious minimalist elements)), "
                f"((masterful artistic finish)), ((visual excellence)), "
                f"((abstract perfection))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common abstract art issues."""
        return (
            "((figurative)), ((representational)), ((realistic)), ((photographic)), "
            "((cluttered)), ((chaotic)), ((messy)), ((unbalanced)), ((amateur)), "
            "((poor composition)), ((muddy colors)), ((harsh contrasts)), "
            "((inconsistent style)), ((busy background)), ((distracting elements)), "
            "((lack of focus)), ((poor technique)), ((unrefined)), ((crude)), "
            "((low resolution)), ((pixelated)), ((blurry)), ((noisy))"
        )
