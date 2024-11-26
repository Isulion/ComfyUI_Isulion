import random
from typing import Dict
from .base_handler import BaseThemeHandler

class CyberpunkThemeHandler(BaseThemeHandler):
    """Handler for cyberpunk-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("cyberpunk")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate cyberpunk-themed components with neon-noir aesthetics."""
        components = {}
        
        # Generate subject with cyberpunk characteristics
        if custom_subject:
            components["subject"] = (
                f"((masterful cyberpunk art)) of {custom_subject}, "
                f"((neo-noir aesthetic)), ((cyber-enhanced)), "
                f"((high-tech dystopian)), ((neon-punk style)), "
                f"((cybernetic augmentations)), ((urban tech))"
            )
        else:
            subjects = ["street samurai", "netrunner", "cyber mercenary", "augmented hacker", "rogue AI", "corpo assassin", "cyber detective", "street tech"]
            cyber_mods = ["neural implants", "cybernetic limbs", "holographic HUD", "retinal enhancements", "chrome plating", "bio-digital interface"]
            tech_gear = ["plasma weapons", "neural deck", "holo-projectors", "cyber-ware", "nano-tech gear", "quantum hardware"]
            
            subject = random.choice(subjects)
            mod = random.choice(cyber_mods)
            gear = random.choice(tech_gear)
            
            components["subject"] = (
                f"((masterful cyberpunk art)) of ((a {subject})), "
                f"((equipped with {mod})), ((using {gear})), "
                f"((neo-noir style)), ((cyber-enhanced)), "
                f"((high-tech dystopian)), ((urban tech))"
            )
        
        # Generate environment with cyberpunk atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((neon-lit {custom_location})), "
                    f"((cyberpunk atmosphere)), ((urban dystopia)), "
                    f"((high-tech slums)), ((corporate megastructures)), "
                    f"((cyber-noir environment))"
                )
            else:
                environments = ["megacity slums", "neon streets", "corporate district", "underground hackerspace", "cyber black market", "tech bazaar", "vertical metropolis", "data den"]
                urban_features = ["holographic billboards", "neon signs", "data streams", "cyber cafes", "black markets", "street tech vendors"]
                weather = ["acid rain", "neon fog", "smog-filled", "electric storm", "synthetic snow", "digital haze"]
                
                environment = random.choice(environments)
                feature = random.choice(urban_features)
                atmosphere = random.choice(weather)
                
                components["environment"] = (
                    f"in ((a {atmosphere} {environment})) with ((massive {feature})), "
                    f"((cyberpunk cityscape)), ((neon-lit streets)), "
                    f"((corporate towers)), ((urban decay)), "
                    f"((high-tech low-life))"
                )
        
        # Generate style with cyberpunk techniques
        if include_style == "yes":
            styles = ["neo-noir", "tech noir", "cyber noir", "neon punk", "chrome punk", "digital punk"]
            aesthetics = ["retrofuturistic", "neon-noir", "cyber-gritty", "tech-noir", "digital-decay", "chrome-punk"]
            color_schemes = ["neon-noir", "cyber-chrome", "digital-neon", "tech-glow", "urban-night", "synthetic-pulse"]
            
            style = random.choice(styles)
            aesthetic = random.choice(aesthetics)
            colors = random.choice(color_schemes)
            
            components["style"] = (
                f"((rendered in {style} style)), "
                f"((with {aesthetic} aesthetics)), (({colors} color scheme)), "
                f"((cyberpunk mood)), ((urban tech)), ((neon lighting)), "
                f"((chrome reflections)), ((digital distortion)), "
                f"((masterful execution)), ((cyber-noir atmosphere)), "
                f"8k resolution, ultra detailed, ray tracing, volumetric lighting"
            )
        
        # Generate effects with cyberpunk elements
        if include_effects == "yes":
            effects = ["neon glow", "holographic glitch", "digital artifacts", "cyber distortion", "neural noise", "data corruption"]
            tech_details = ["data streams", "matrix code", "cyber grids", "neural patterns", "digital noise", "tech interference"]
            
            effect = random.choice(effects)
            detail = random.choice(tech_details)
            
            components["effects"] = (
                f"with ((intense {effect})), ((dynamic {detail})), "
                f"((cyberpunk atmosphere)), ((neon accents)), "
                f"((digital distortion)), ((tech noir effects)), "
                f"((urban decay)), ((cyber-noir mastery))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid non-cyberpunk elements."""
        return (
            "((natural landscapes)), ((historical)), ((medieval)), ((fantasy)), "
            "((clean environment)), ((bright daylight)), ((rural setting)), "
            "((organic)), ((traditional)), ((classical)), ((pastoral)), "
            "((clean streets)), ((bright colors)), ((happy mood)), "
            "low quality, blurry, ugly, deformed, amateur"
        )
