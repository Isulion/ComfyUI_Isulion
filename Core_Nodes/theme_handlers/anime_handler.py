from typing import Dict
from .base_handler import BaseThemeHandler

class AnimeThemeHandler(BaseThemeHandler):
    """Handler for anime-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate anime-themed components with professional quality and style."""
        components = {}

        # Always use random elements, even with custom_subject
        character = self._get_random_choice("anime.characters")
        expression = self._get_random_choice("anime.expressions")
        pose = self._get_random_choice("anime.poses")
        outfit = self._get_random_choice("anime.outfits")

        if custom_subject:
            components["subject"] = (
                f"((masterful anime rendition)) of {custom_subject}, "
                f"((as {character})), ((perfect {expression} expression)), "
                f"((in dynamic {pose})), ((wearing detailed {outfit})), "
                f"((professional anime style)), ((character appeal)), "
                f"((detailed anime aesthetics)), ((dynamic pose))"
            )
        else:
            components["subject"] = (
                f"((masterful anime {character})) with ((perfect {expression} expression)), "
                f"((in dynamic {pose})), ((wearing detailed {outfit})), "
                f"((professional anime style)), ((perfect character design)), "
                f"((expressive features)), ((anime excellence))"
            )

        # Generate environment with enhanced anime atmosphere
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((beautifully rendered anime {custom_location})) with "
                    f"((perfect background detail)), ((anime atmosphere)), "
                    f"((environmental storytelling)), ((scene composition)), "
                    f"((manga-style background)), ((artistic excellence))"
                )
            else:
                location = self._get_random_choice("anime.locations")
                time = self._get_random_choice("anime.times")
                weather = self._get_random_choice("anime.weather")
                components["environment"] = (
                    f"in ((beautifully rendered anime {location})) during "
                    f"((dramatic {time})) with ((perfect {weather} effects)), "
                    f"((detailed background)), ((anime atmosphere)), "
                    f"((perfect scene composition)), ((artistic excellence))"
                )

        # Generate style with enhanced anime techniques
        if include_style:
            style = self._get_random_choice("anime.styles")
            studio = self._get_random_choice("anime.studios")
            components["style"] = (
                f"((masterfully rendered in {style} anime style)), "
                f"((inspired by {studio} quality)), ((perfect line art)), "
                f"((professional cel shading)), ((vibrant anime colors)), "
                f"((detailed highlights)), ((artistic excellence)), "
                f"((flawless composition)), 8k resolution"
            )

        # Generate effects with enhanced anime elements
        if include_effects:
            effect = self._get_random_choice("anime.effects")
            mood = self._get_random_choice("anime.moods")
            lighting = self._get_random_choice("anime.lighting")
            components["effects"] = (
                f"with ((perfect anime {effect} effects)), "
                f"((masterful {mood} atmosphere)), ((beautiful {lighting})), "
                f"((dramatic shadows)), ((anime visual excellence)), "
                f"((perfect detail)), ((artistic mastery))"
            )

        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common anime art issues."""
        return (
            "((photorealistic)), ((3d render)), ((western cartoon)), ((amateur)), "
            "((poor line art)), ((messy coloring)), ((inconsistent style)), "
            "((bad anatomy)), ((wrong proportions)), ((stiff pose)), "
            "((poor composition)), ((muddy colors)), ((pixelated)), "
            "((low quality)), ((blurry)), ((noisy)), ((rough sketch)), "
            "((missing details)), ((poor shading)), ((bad perspective)), "
            "((deformed features)), ((uncanny)), ((dull colors))"
        )
