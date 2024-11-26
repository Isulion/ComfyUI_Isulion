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
        
        # Generate subject with enhanced fantasy characteristics
        if custom_subject:
            components["subject"] = (
                f"((masterful fantasy art)) of {custom_subject}, "
                f"((perfect fantasy design)), ((magical excellence)), "
                f"((mythical quality)), ((enchanted presence)), "
                f"((fantasy mastery)), ((ethereal beauty))"
            )
        else:
            character = random.choice(self.theme_config.get("characters", []))
            class_type = random.choice(self.theme_config.get("character_classes", []))
            creature = random.choice(self.theme_config.get("creatures", []))
            components["subject"] = (
                f"((masterful fantasy art)) of ((legendary {character})), "
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
                environment = random.choice(self.theme_config.get("environments", []))
                architecture = random.choice(self.theme_config.get("architectural_elements", []))
                weather = random.choice(self.theme_config.get("weather_effects", []))
                components["environment"] = (
                    f"in ((enchanted {environment})) with "
                    f"((majestic {architecture})) during ((mystical {weather})), "
                    f"((perfect fantasy atmosphere)), ((magical realm)), "
                    f"((ethereal surroundings)), ((fantasy excellence))"
                )
        
        # Generate style with enhanced fantasy techniques
        if include_style == "yes":
            style = random.choice(self.theme_config.get("styles", []))
            detail = random.choice(self.theme_config.get("details", []))
            color_scheme = random.choice(self.theme_config.get("color_schemes", []))
            components["style"] = (
                f"((masterfully rendered in {style} style)), "
                f"((with perfect {detail})), ((magical realism)), "
                f"((enchanted {color_scheme} palette)), ((fantasy artistry)), "
                f"((perfect composition)), ((ethereal lighting)), "
                f"((mystical atmosphere)), ((artistic excellence)), "
                f"8k resolution"
            )
        
        # Generate effects with enhanced magical elements
        if include_effects == "yes":
            effect = random.choice(self.theme_config.get("effects", []))
            magic = random.choice(self.theme_config.get("magic", []))
            artifact = random.choice(self.theme_config.get("artifacts", []))
            components["effects"] = (
                f"with ((perfect magical {effect})), ((powerful {magic})), "
                f"((mystical {artifact})), ((ethereal glow)), "
                f"((enchanted elements)), ((magical excellence)), "
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
