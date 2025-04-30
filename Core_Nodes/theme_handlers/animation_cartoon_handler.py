from typing import Dict
from .base_handler import BaseThemeHandler

class AnimationCartoonThemeHandler(BaseThemeHandler):
    """Handler for animation cartoon-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate animation cartoon-themed components with professional quality."""
        components = {}

        # Always use random elements, even with custom_subject
        character = self._get_random_choice("animation_cartoon.characters")
        expression = self._get_random_choice("animation_cartoon.expressions")
        pose = self._get_random_choice("animation_cartoon.poses")

        if custom_subject:
            components["subject"] = (
                f"((masterful cartoon rendition)) of {custom_subject}, "
                f"((as {character})), ((perfect {expression} expression)), "
                f"((in dynamic {pose})), ((professional cartoon style)), "
                f"((character appeal)), ((animation quality))"
            )
        else:
            components["subject"] = (
                f"((masterful cartoon {character})) with ((perfect {expression} expression)), "
                f"((in dynamic {pose})), ((professional animated character)), "
                f"((expert cartoon style)), ((perfect pose execution)), "
                f"((character appeal)), ((animation excellence))"
            )

        # Generate environment with enhanced animation quality
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((masterfully animated {custom_location})) with "
                    f"((perfect cartoon setting)), ((animation excellence)), "
                    f"((environmental storytelling)), ((scene composition)), "
                    f"((background detail))"
                )
            else:
                location = self._get_random_choice("animation_cartoon.locations")
                props = self._get_random_choice("animation_cartoon.props")
                components["environment"] = (
                    f"in ((masterfully animated {location})) with "
                    f"((perfectly detailed {props})), ((expert cartoon environment)), "
                    f"((professional animated setting)), ((whimsical atmosphere)), "
                    f"((perfect background composition)), ((scene detail))"
                )

        # Generate style with enhanced animation techniques
        if include_style:
            style = self._get_random_choice("animation_cartoon.styles")
            technique = self._get_random_choice("animation_cartoon.techniques")
            components["style"] = (
                f"((masterfully rendered in {style} style)), "
                f"((using professional {technique} technique)), "
                f"((perfect cartoon aesthetics)), ((animation mastery)), "
                f"((vibrant color palette)), ((artistic excellence)), "
                f"((flawless composition)), 8k resolution"
            )

        # Generate effects with enhanced cartoon elements
        if include_effects:
            effect = self._get_random_choice("animation_cartoon.effects")
            mood = self._get_random_choice("animation_cartoon.moods")
            components["effects"] = (
                f"with ((perfect cartoon {effect} effects)), "
                f"((masterful {mood} mood)), ((animation energy)), "
                f"((cartoon excellence)), ((visual appeal)), "
                f"((professional finish)), ((artistic mastery))"
            )

        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common animation issues."""
        return (
            "((amateur)), ((poor animation)), ((stiff poses)), ((uncanny)), "
            "((inconsistent style)), ((poor line quality)), ((messy coloring)), "
            "((flat shading)), ((bad proportions)), ((awkward anatomy)), "
            "((poor composition)), ((muddy colors)), ((pixelated)), "
            "((low quality)), ((blurry)), ((noisy)), ((rough sketch)), "
            "((unfinished)), ((poor lighting)), ((bad perspective))"
        )
