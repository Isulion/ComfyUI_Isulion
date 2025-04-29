import random
from typing import Dict
from .base_handler import BaseThemeHandler

class SciFiThemeHandler(BaseThemeHandler):
    """Handler for science fiction themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("scifi")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate sci-fi themed components."""
        components = {}

        # Always use random elements, even with custom_subject
        tech_elements = ["plasma core", "quantum enhancements", "holographic displays", "neural interfaces", "energy fields", "nanotech augmentations"]
        materials = ["chrome", "energy crystal", "nano-alloy", "plasma", "quantum metal", "holographic material"]

        # Generate subject with sci-fi characteristics
        if custom_subject:
            tech = random.choice(tech_elements)
            material = random.choice(materials)
            components["subject"] = (
                f"((masterful sci-fi art)) of {custom_subject}, "
                f"((with {tech})), ((made of {material})), "
                f"((futuristic design)), ((technological excellence)), "
                f"((advanced engineering)), ((sci-fi aesthetics))"
            )
        else:
            subjects = ["advanced robot", "cyborg warrior", "space explorer", "alien being", "tech augmented human", "holographic entity", "quantum being", "cybernetic creature"]
            tech = random.choice(tech_elements)
            material = random.choice(materials)
            subject = random.choice(subjects)
            components["subject"] = (
                f"((masterful sci-fi art)) of ((a {subject})), "
                f"((with {tech})), ((made of {material})), "
                f"((futuristic design)), ((technological excellence)), "
                f"((advanced engineering)), ((sci-fi aesthetics))"
            )

        # Generate environment with sci-fi atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})), "
                    f"((advanced technology)), ((sci-fi atmosphere)), "
                    f"((future world)), ((technological marvels)), "
                    f"((high-tech environment))"
                )
            else:
                environments = ["space station", "cybercity", "quantum realm", "alien world", "tech metropolis", "orbital platform", "research facility", "neon city"]
                tech_features = ["holographic displays", "energy fields", "quantum processors", "plasma reactors", "gravity manipulators", "neural networks"]
                atmospheres = ["neon-lit", "high-tech", "futuristic", "cybernetic", "quantum", "plasma-charged"]

                environment = random.choice(environments)
                feature = random.choice(tech_features)
                atmosphere = random.choice(atmospheres)

                components["environment"] = (
                    f"in ((a {atmosphere} {environment})) with ((advanced {feature})), "
                    f"((sci-fi technology)), ((futuristic architecture)), "
                    f"((technological marvels)), ((future world building)), "
                    f"((high-tech atmosphere))"
                )

        # Generate style with sci-fi techniques
        if include_style == "yes":
            styles = ["cyberpunk", "hard sci-fi", "space opera", "biopunk", "quantum punk", "tech noir"]
            tech_aspects = ["holographic", "quantum", "cybernetic", "plasma-based", "nano-tech", "neural-linked"]
            color_schemes = ["neon-chrome", "quantum plasma", "cyber-tech", "holographic spectrum", "energy pulse", "neural grid"]

            style = random.choice(styles)
            aspect = random.choice(tech_aspects)
            colors = random.choice(color_schemes)

            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aspect} aesthetics)), (({colors} color scheme)), "
                f"((technological precision)), ((futuristic design)), "
                f"((sci-fi excellence)), ((advanced rendering)), "
                f"((future tech details)), ((masterful execution)), "
                f"8k resolution, ultra detailed"
            )

        # Generate effects with sci-fi elements
        if include_effects == "yes":
            effects = ["energy fields", "holographic overlays", "quantum particles", "plasma emissions", "neural patterns", "tech auras"]
            tech_details = ["circuitry patterns", "data streams", "energy flows", "quantum effects", "neural networks", "cyber enhancements"]

            effect = random.choice(effects)
            detail = random.choice(tech_details)

            components["effects"] = (
                f"with ((advanced {effect})), ((intricate {detail})), "
                f"((technological brilliance)), ((futuristic atmosphere)), "
                f"((sci-fi elements)), ((high-tech details)), "
                f"((future tech mastery))"
            )

        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid non-sci-fi elements."""
        return (
            "((medieval)), ((fantasy)), ((ancient)), ((organic)), ((rustic)), "
            "((natural)), ((primitive technology)), ((historical)), "
            "((traditional)), ((vintage)), ((classical)), ((steam-powered)), "
            "low quality, blurry, ugly, deformed, amateur, "
            "((non-technological)), ((outdated)), ((retro))"
        )
