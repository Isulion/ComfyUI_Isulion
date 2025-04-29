import random
from typing import Dict
from .base_handler import BaseThemeHandler

class FantasyThemeHandler(BaseThemeHandler):
    """Handler for fantasy-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("fantasy")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate fantasy-themed components with enhanced magical elements."""
        components = {}

        # Always use random elements, even with custom_subject
        character = random.choice(self.theme_config.get("characters", ["mystical hero", "ancient wizard", "elven warrior"]))
        class_type = random.choice(self.theme_config.get("character_classes", ["mage", "warrior", "druid"]))
        creature = random.choice(self.theme_config.get("creatures", ["dragon", "phoenix", "unicorn"]))

        # Generate subject with enhanced fantasy characteristics
        if custom_subject:
            components["subject"] = (
                f"((epic fantasy art)) of {custom_subject}, "
                f"((as a powerful {class_type})), ((with mystical {creature})), "
                f"((perfect character design)), ((fantasy excellence)), "
                f"((magical presence)), ((mythical mastery))"
            )
        else:
            components["subject"] = (
                f"((epic fantasy art)) of ((legendary {character})), "
                f"((as a powerful {class_type})), ((with mystical {creature})), "
                f"((perfect character design)), ((fantasy excellence)), "
                f"((magical presence)), ((mythical mastery))"
            )

        # Generate environment with enhanced magical atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((enchanted {custom_location})) with "
                    f"((perfect magical atmosphere)), ((fantasy realm)), "
                    f"((mythical environment)), ((ethereal surroundings)), "
                    f"((magical world building)), ((fantasy excellence))"
                )
            else:
                environment = random.choice(self.theme_config.get("environments", ["crystal castle", "enchanted forest", "floating islands"]))
                architecture = random.choice(self.theme_config.get("architectural_elements", ["magical towers", "ancient temples", "crystal spires"]))
                weather = random.choice(self.theme_config.get("weather_effects", ["mystical fog", "magical aurora", "ethereal storm"]))
                components["environment"] = (
                    f"in ((magical {environment})) with "
                    f"((majestic {architecture})) during ((mystical {weather})), "
                    f"((perfect fantasy atmosphere)), ((magical realm)), "
                    f"((ethereal surroundings)), ((fantasy excellence))"
                )

        # Generate style with enhanced fantasy techniques
        if include_style == "yes":
            style = random.choice(self.theme_config.get("styles", ["epic fantasy", "high fantasy", "magical realism"]))
            lighting = random.choice(self.theme_config.get("lighting", ["ethereal glow", "magical radiance", "mystical light"]))
            color_scheme = random.choice(self.theme_config.get("color_schemes", ["magical rainbow", "ethereal pastels", "mystical jewel tones"]))
            components["style"] = (
                f"((masterfully rendered in {style} style)), "
                f"((with {lighting})), ((magical realism)), "
                f"((enchanted {color_scheme})), ((fantasy artistry)), "
                f"((perfect composition)), ((ethereal atmosphere)), "
                f"((mystical quality)), ((artistic excellence)), "
                f"8k resolution, RAW photo"
            )

        # Generate effects with enhanced magical elements
        if include_effects == "yes":
            magic = random.choice(self.theme_config.get("magical_elements", ["ancient spells", "mystical runes", "magical crystals"]))
            artifact = random.choice(self.theme_config.get("artifacts", ["enchanted staff", "magical sword", "mystical orb"]))
            components["effects"] = (
                f"with ((powerful {magic})), ((mystical energy)), "
                f"((legendary {artifact})), ((ethereal glow)), "
                f"((enchanted particles)), ((magical excellence)), "
                f"((fantasy perfection)), ((mystical mastery))"
            )

        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid common fantasy art issues."""
        return (
            "((modern elements)), ((contemporary style)), ((urban setting)), "
            "((mundane objects)), ((technological items)), ((industrial elements)), "
            "((amateur)), ((poor composition)), ((bad lighting)), ((inconsistent style)), "
            "((poor color harmony)), ((flat colors)), ((missing details)), "
            "((unrealistic anatomy)), ((stiff poses)), ((poor perspective)), "
            "((weak magic effects)), ((cheap looking)), ((generic fantasy)), "
            "((poor atmosphere)), ((bland design)), ((weak composition)), "
            "((low quality)), ((blurry)), ((noisy)), ((pixelated)), "
            "((scientific equipment)), ((corporate environment)), ((modern clothing))"
        )
