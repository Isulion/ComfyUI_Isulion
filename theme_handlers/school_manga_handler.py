from typing import Dict
from .base_handler import BaseThemeHandler

class SchoolMangaThemeHandler(BaseThemeHandler):
    """Handler for professional school manga-themed prompt generation with authentic Japanese aesthetics and technical manga mastery."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("school_manga")
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate sophisticated school manga-themed components with authentic Japanese school life elements and professional manga techniques."""
        components = {}
        
        # Generate subject with enhanced manga characteristics
        if custom_subject:
            components["subject"] = (
                f"((professional black and white manga illustration)) of (({custom_subject})), "
                f"((perfect manga character design)), ((authentic japanese school life)), "
                f"((masterful ink technique)), ((dynamic pose)), ((expressive features)), "
                f"((detailed school uniform)), ((clean linework)), ((high contrast rendering)), "
                f"((professional manga quality)), ((technical excellence))"
            )
        else:
            character = self._get_random_choice("school_manga.characters")
            activity = self._get_random_choice("school_manga.activities")
            prop = self._get_random_choice("school_manga.props")
            uniform = self._get_random_choice("school_manga.uniforms")
            expression = self._get_random_choice("school_manga.expressions")
            linework = self._get_random_choice("school_manga.linework")
            components["subject"] = (
                f"((professional black and white manga illustration)) of ((authentic {character})), "
                f"((engaging in {activity})), ((with detailed {prop})), "
                f"((wearing technically detailed {uniform})), ((showing {expression})), "
                f"((with {linework})), ((perfect manga character design)), "
                f"((masterful ink technique)), ((dynamic pose)), ((clean linework)), "
                f"((high contrast rendering)), ((professional manga quality))"
            )
        
        # Generate environment with enhanced architectural detail
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((detailed manga {custom_location})) with ((precise architectural linework)), "
                    f"((perfect perspective control)), ((clean background separation)), "
                    f"((professional environmental detail)), ((masterful spatial depth)), "
                    f"((authentic japanese architecture)), ((sharp background contrast)), "
                    f"((technical background excellence)), ((manga environmental mastery))"
                )
            else:
                location = self._get_random_choice("school_manga.locations")
                event = self._get_random_choice("school_manga.events")
                season = self._get_random_choice("school_manga.seasons")
                time = self._get_random_choice("school_manga.times_of_day")
                components["environment"] = (
                    f"in ((detailed manga {location})) during (({event})), "
                    f"((in {season})), ((during {time})), "
                    f"((with precise architectural linework)), ((perfect perspective control)), "
                    f"((clean background separation)), ((professional environmental detail)), "
                    f"((masterful spatial depth)), ((authentic japanese architecture)), "
                    f"((sharp background contrast)), ((technical excellence))"
                )
        
        # Generate style with enhanced manga techniques
        if include_style == "yes":
            style = self._get_random_choice("school_manga.styles")
            detail = self._get_random_choice("school_manga.details")
            technique = self._get_random_choice("school_manga.techniques")
            shading = self._get_random_choice("school_manga.shading")
            components["style"] = (
                f"((professional manga technique)), ((masterful {style} style)), "
                f"((with perfect {detail})), ((using {technique})), "
                f"((featuring {shading})), ((perfect hatching control)), "
                f"((technical black and white mastery)), ((clean line confidence)), "
                f"((sharp value contrast)), ((professional manga artwork)), "
                f"((authentic japanese manga style)), ((technical excellence)), "
                f"8k resolution, perfect details"
            )
        
        # Generate effects with enhanced technical elements
        if include_effects == "yes":
            effect = self._get_random_choice("school_manga.effects")
            element = self._get_random_choice("school_manga.elements")
            mood = self._get_random_choice("school_manga.moods")
            hatching = self._get_random_choice("school_manga.hatching")
            components["effects"] = (
                f"with ((precise line weight control)), ((perfect {effect})), "
                f"((masterful {element})), ((authentic {mood})), "
                f"((featuring {hatching})), ((perfect shadow definition)), "
                f"((masterful cross-hatching technique)), ((clean edge separation)), "
                f"((professional black and white contrast)), ((technical precision)), "
                f"((sharp detail rendering)), ((clear tonal hierarchy))"
            )
        
        return components

    def get_negative_prompt(self):
        """Generate comprehensive negative prompt for school manga theme."""
        return (
            "((western comic style)), ((amateur art)), ((poor anatomy)), "
            "((inconsistent style)), ((wrong school uniforms)), "
            "((non-japanese school elements)), ((poor manga style)), "
            "((bad composition)), ((stiff poses)), ((emotionless)), "
            "((wrong perspective)), ((missing details)), ((flat shading)), "
            "((poor line quality)), ((amateur hatching)), ((weak contrast)), "
            "((incorrect japanese elements)), ((unrealistic uniforms)), "
            "((poor backgrounds)), ((missing school atmosphere)), "
            "((low quality)), ((blurry)), ((noisy)), ((pixelated)), "
            "((non-school setting)), ((incorrect cultural elements)), "
            "((wrong architectural style)), ((poor character design)), "
            "((messy linework)), ((inconsistent line weights)), "
            "((poor black and white values)), ((amateur inking))"
        )
