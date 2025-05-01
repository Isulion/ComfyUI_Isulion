from typing import Dict
from .base_handler import BaseThemeHandler
import random

class StarterPackThemeHandler(BaseThemeHandler):
    """Handler for AI action-figure starter pack meme prompt generation."""

    def generate(self,
                 custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: str = "yes",
                 include_style: str = "yes",
                 include_effects: str = "yes") -> Dict[str, str]:
        components = {}

        # Title
        subject = custom_subject.strip() if custom_subject else self._get_random_choice("starter_pack.names")
        title = f"{subject} Starter Pack"

        # Accessories/items: from custom_location (comma-separated) or random
        if custom_location and custom_location.strip():
            items = [s.strip() for s in custom_location.split(",") if s.strip()]
        else:
            # Pick 4 unique items from various starter_pack fields
            pool = []
            pool += random.sample(self.theme_config.get("attires", []), min(1, len(self.theme_config.get("attires", []))))
            pool += random.sample(self.theme_config.get("items", []), min(1, len(self.theme_config.get("items", []))))
            pool += random.sample(self.theme_config.get("supporting_items", []), min(1, len(self.theme_config.get("supporting_items", []))))
            pool += random.sample(self.theme_config.get("objects", []), min(1, len(self.theme_config.get("objects", []))))
            pool += random.sample(self.theme_config.get("passions", []), min(1, len(self.theme_config.get("passions", []))))
            # Fill up to 4 items, avoid duplicates
            items = []
            for i in pool:
                if i not in items:
                    items.append(i)
                if len(items) >= 4:
                    break
            # If not enough, fill with randoms from any field
            if len(items) < 4:
                all_items = (
                    self.theme_config.get("attires", []) +
                    self.theme_config.get("items", []) +
                    self.theme_config.get("supporting_items", []) +
                    self.theme_config.get("objects", []) +
                    self.theme_config.get("passions", [])
                )
                while len(items) < 4 and all_items:
                    choice = random.choice(all_items)
                    if choice not in items:
                        items.append(choice)

        # Packaging details (logo and badge removed)
        color = self._get_random_choice("starter_pack.colors")
        tagline = f"Includes: {', '.join(items)}"
        style = self._get_random_choice("starter_pack.styles")

        # Compose the action-figure-in-packaging meme prompt (logo and badge removed)
        components["subject"] = (
            f"{title} -- action figure collectible\n"
            f"Depict a glossy, miniature action figure of {subject} in a plastic blister packaging, "
            f"styled like a 1990s/2000s toy shelf product. "
            f"Accessories inside the packaging: {', '.join(items)}. "
            f"Packaging features: bold {color} background and tagline '{tagline}'. "
            f"Figure has plastic-like skin, oversized head, glossy eyes, and is posed heroically. "
            f"Accessories are arranged around the figure in the packaging. "
            f"Design evokes a playful, collectible, meme-inspired starter pack."
        )

        if include_environment == "yes":
            components["environment"] = (
                f"((toy shelf)), ((plastic blister packaging)), ((bold {color} background)), ((studio lighting)), ((meme starter pack layout))"
            )
        if include_style == "yes":
            components["style"] = (
                f"((glossy plastic miniature)), ((action figure style)), ((90s/2000s toy ad aesthetic)), ((bold logo)), ((meme collectible)), (({style}))"
            )
        if include_effects == "yes":
            components["effects"] = (
                "((shiny reflections)), ((plastic textures)), ((glossy highlights)), ((vivid colors)), ((toy-like finish)), ((fun meme vibe))"
            )

        return components
