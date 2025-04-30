import random
from typing import Dict
from .base_handler import BaseThemeHandler

class ImpressionistThemeHandler(BaseThemeHandler):
    """Handler for impressionist-style prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("impressionist")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate impressionist-styled components."""
        components = {}
        
        # Prepare random elements for both branches
        techniques = ["broken color", "visible brushstrokes", "impasto technique", "optical mixing", "pure color application"]
        palette = ["vibrant", "pure", "complementary", "atmospheric", "light-filled"]
        mood = ["serene", "lively", "contemplative", "dynamic", "peaceful"]

        technique = random.choice(techniques)
        color_palette = random.choice(palette)
        painting_mood = random.choice(mood)

        # Generate subject with impressionist characteristics
        if custom_subject:
            components["subject"] = (
                f"((masterful impressionist painting)) of {custom_subject}, "
                f"((with {technique})), (({color_palette} color palette)), "
                f"(({painting_mood} mood)), ((loose brushstrokes)), "
                f"((vibrant color impressionism)), ((light and atmosphere)), "
                f"((impressionist style)), ((artistic excellence)), ((painterly quality))"
            )
        else:
            subjects = ["garden scene", "water lilies", "sunset landscape", "cafe terrace", "flower field", "river scene", "cathedral facade", "people in park"]
            subject = random.choice(subjects)
            technique = random.choice(techniques)
            color_palette = random.choice(palette)
            painting_mood = random.choice(mood)
            components["subject"] = (
                f"((masterful impressionist painting)) of ((a {subject})), "
                f"((with {technique})), (({color_palette} color palette)), "
                f"(({painting_mood} mood)), ((loose brushstrokes)), "
                f"((vibrant color impressionism)), ((light and atmosphere)), "
                f"((impressionist style)), ((artistic excellence)), ((painterly quality))"
            )
        
        # Generate environment with impressionist atmosphere
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((impressionist {custom_location})), "
                    f"((natural light)), ((atmospheric perspective)), "
                    f"((en plein air)), ((changing light effects)), "
                    f"((impressionist scene))"
                )
            else:
                environments = ["garden", "riverside", "countryside", "city street", "park", "seaside", "meadow", "terrace"]
                time_of_day = ["sunset", "midday", "morning light", "afternoon glow", "dusk"]
                weather = ["misty", "sunny", "cloudy", "rainy", "atmospheric"]
                
                environment = random.choice(environments)
                time = random.choice(time_of_day)
                atmosphere = random.choice(weather)
                
                components["environment"] = (
                    f"in ((an impressionist {environment})) during (({time})), "
                    f"((with {atmosphere} atmosphere)), ((natural light)), "
                    f"((atmospheric perspective)), ((en plein air)), "
                    f"((changing light effects)), ((impressionist scene))"
                )
        
        # Generate style with impressionist techniques
        if include_style:
            technique = random.choice(techniques)
            color_palette = random.choice(palette)
            painting_mood = random.choice(mood)
            components["style"] = (
                f"((painted in classic impressionist style)), "
                f"((with {technique})), (({color_palette} color palette)), "
                f"(({painting_mood} mood)), ((masterful brushwork)), "
                f"((light capturing)), ((atmospheric quality)), "
                f"((impressionist excellence)), ((artistic mastery)), "
                f"8k resolution, oil painting, canvas texture"
            )
        
        # Generate effects with impressionist elements
        if include_effects:
            effects = ["light diffusion", "color vibration", "atmospheric haze", "natural reflections", "dappled light"]
            details = ["loose details", "suggestive forms", "spontaneous marks", "textural variety", "gestural strokes"]
            
            effect = random.choice(effects)
            detail = random.choice(details)
            
            components["effects"] = (
                f"with ((masterful {effect})), ((beautiful {detail})), "
                f"((impressionist light)), ((atmospheric depth)), "
                f"((painterly effects)), ((artistic excellence)), "
                f"((impressionist mastery))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate negative prompt to avoid non-impressionist elements."""
        return (
            "((photorealistic)), ((sharp details)), ((precise lines)), "
            "((digital art)), ((cartoon)), ((anime)), ((3d)), ((modern style)), "
            "((flat colors)), ((hard edges)), ((graphic design)), "
            "((pop art)), ((minimalist)), ((abstract)), ((surreal)), "
            "low quality, blurry, ugly, deformed, amateur"
        )
