from typing import Dict, List, Optional
from .base_handler import BaseThemeHandler
import random

class CharacterDesignerThemeHandler(BaseThemeHandler):
    """Handler for creating detailed character designs with customizable attributes."""

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate a detailed character design with various customizable elements."""
        
        components = {}
        
        # Generate character base
        if custom_subject:
            base_character = custom_subject
        else:
            base_character = random.choice(self.get_character_types())
        
        # Add profession and role
        profession = random.choice(self.get_professions())
        role_description = random.choice(self.get_role_descriptions())
        
        # Generate clothing and accessories
        era = random.choice(self.get_historical_periods())
        outfit = random.choice(self.get_outfits(era))
        accessories = random.choice(self.get_accessories(era))
        
        # Combine character elements
        components["subject"] = (
            f"((masterful portrait)) of {base_character} as a {profession}, {role_description}, "
            f"((wearing {era} style {outfit})), ((detailed {accessories})), "
            f"((perfect character design)), ((expressive features)), "
            f"((professional quality)), ((character excellence))"
        )
        
        # Generate environment based on profession and era
        if include_environment == "yes":
            if custom_location:
                setting = custom_location
            else:
                setting = random.choice(self.get_settings(era, profession))
            
            time_of_day = random.choice(self.get_times_of_day())
            atmosphere = random.choice(self.get_atmospheres())
            
            components["environment"] = (
                f"in ((detailed {setting})) during {time_of_day}, "
                f"((with {atmosphere} atmosphere)), ((period-accurate details)), "
                f"((environmental storytelling)), ((perfect composition))"
            )
        
        # Add style elements
        if include_style == "yes":
            art_style = random.choice(self.get_art_styles())
            lighting = random.choice(self.get_lighting_styles())
            color_palette = random.choice(self.get_color_palettes(era))
            
            components["style"] = (
                f"((masterful {art_style})), ((perfect {lighting})), "
                f"((beautiful {color_palette} color palette)), "
                f"((high detail)), ((professional quality))"
            )
        
        # Add special effects
        if include_effects == "yes":
            effect = random.choice(self.get_special_effects())
            components["effects"] = (
                f"((dramatic {effect})), ((character focus)), "
                f"((subtle details)), ((perfect rendering))"
            )
        
        # Add negative prompt
        components["negative"] = ", ".join([
            "deformed", "distorted", "unrealistic anatomy",
            "bad proportions", "low quality", "blurry",
            "amateur", "poorly drawn", "bad art",
            "anachronistic elements"
        ])
        
        return components

    def get_character_types(self) -> List[str]:
        return [
            # Fantasy/Historical Types
            "noble person", "common folk", "warrior",
            "scholar", "artist", "merchant",
            "adventurer", "royal figure", "mystic",
            "craftsperson", "performer", "diplomat",
            "explorer", "inventor", "healer",
            "sailor", "farmer", "miner",
            "nomad", "hunter", "priest",
            "bard", "alchemist", "spy",
            "knight", "wizard", "rogue",
            "ranger", "paladin", "druid",
            "monk", "barbarian", "sorcerer",
            "warlock", "artificer", "beastmaster",
            "shaman", "necromancer", "illusionist",
            "summoner", "enchanter", "assassin",
            "gladiator", "pirate", "ninja",
            "samurai", "viking", "crusader",
            # Modern Types
            "entrepreneur", "scientist", "programmer",
            "artist", "influencer", "athlete",
            "chef", "designer", "journalist",
            "activist", "researcher", "executive",
            "educator", "filmmaker", "musician",
            "photographer", "architect", "engineer",
            "doctor", "lawyer", "pilot",
            "astronaut", "detective", "firefighter",
            "police officer", "paramedic", "psychologist",
            "veterinarian", "environmentalist", "curator"
        ]

    def get_professions(self) -> List[str]:
        return [
            # Historical Professions
            "master blacksmith", "royal advisor", "skilled physician",
            "renowned artist", "master chef", "expert navigator",
            "master architect", "skilled merchant", "royal guard",
            "court musician", "master jeweler", "skilled diplomat",
            "expert cartographer", "master alchemist", "skilled hunter",
            "master weaver", "expert astronomer", "royal scribe",
            "master glassblower", "expert herbalist", "royal falconer",
            "skilled shipwright", "master perfumer", "expert siege engineer",
            "court jester", "master vintner", "skilled animal trainer",
            "expert geologist", "master clockmaker", "royal food taster",
            "skilled linguist", "master calligrapher", "expert mathematician",
            # Modern Professions
            "AI researcher", "blockchain developer", "quantum physicist",
            "cybersecurity expert", "data scientist", "UX designer",
            "robotics engineer", "biotech researcher", "space engineer",
            "neuroscientist", "ethical hacker", "game developer",
            "sustainability consultant", "drone operator", "VR architect",
            "genetic counselor", "digital artist", "social media strategist",
            "machine learning specialist", "renewable energy expert", "3D printing engineer",
            "cryptocurrency analyst", "cloud architect", "bioinformatician",
            "telemedicine physician", "space tourism guide", "synthetic biologist",
            "quantum computing researcher", "augmented reality designer", "neural interface developer"
        ]

    def get_role_descriptions(self) -> List[str]:
        return [
            "with an air of authority", "exuding confidence",
            "with a mysterious presence", "radiating wisdom",
            "showing great dignity", "with noble bearing",
            "displaying skilled expertise", "emanating creative energy",
            "showing masterful presence", "with diplomatic poise"
        ]

    def get_historical_periods(self) -> List[str]:
        return [
            # Historical Periods
            "Medieval", "Renaissance", "Victorian",
            "Ancient Roman", "Ancient Egyptian", "Byzantine",
            "Baroque", "Rococo", "Art Nouveau",
            "Ancient Greek", "Tudor", "Gothic",
            "Belle Époque", "Edwardian", "Regency",
            # Modern Periods
            "1920s", "1930s", "1940s",
            "1950s", "1960s", "1970s",
            "1980s", "1990s", "2000s",
            "2010s", "2020s", "Contemporary",
            # Future-Inspired
            "Near Future", "Cyberpunk", "Post-Cyberpunk",
            "Solarpunk", "Atompunk", "Dieselpunk"
        ]

    def get_outfits(self, era: str) -> List[str]:
        base_outfits = {
            # Historical Era Outfits
            "Medieval": [
                "ornate royal garments", "noble court dress",
                "decorated armor", "merchant's fine clothing",
                "guild master's attire", "ceremonial robes",
                "monk's humble habit", "jester's colorful costume",
                "knight's polished plate mail", "peasant's simple tunic"
            ],
            "Renaissance": [
                "elaborate court costume", "rich merchant's dress",
                "detailed period gown", "noble's fine doublet",
                "artistic master's garments", "ceremonial outfit",
                "scholar's academic robes", "explorer's practical attire",
                "diplomat's elegant suit", "artisan's work clothes"
            ],
            "Victorian": [
                "formal evening wear", "elaborate day dress",
                "refined gentleman's suit", "formal military uniform",
                "sophisticated lady's gown", "professional attire",
                "industrial worker's outfit", "adventurer's practical gear",
                "scientist's lab coat", "child's miniature adult clothing"
            ],
            "Ancient Roman": [
                "senator's toga", "legionnaire's armor",
                "patrician's fine tunic", "plebeian's simple clothing",
                "emperor's regal attire", "priestess's ceremonial robes"
            ],
            "Ancient Egyptian": [
                "pharaoh's ornate regalia", "noble's linen sheath dress",
                "priest's ceremonial attire", "scribe's simple kilt",
                "soldier's leather armor", "artisan's practical garment"
            ],
            "Byzantine": [
                "emperor's opulent robes", "aristocrat's silk garments",
                "clergy's ornate vestments", "merchant's fine clothing",
                "soldier's lamellar armor", "commoner's simple tunic"
            ],
            # Modern Era Outfits
            "Contemporary": [
                "business casual attire", "smart casual ensemble",
                "tech company casual", "creative professional outfit",
                "startup founder style", "digital nomad wear",
                "sustainable fashion", "minimalist clothing",
                "athleisure ensemble", "modern professional suit"
            ],
            "Near Future": [
                "smart fabric clothing", "biometric suit",
                "climate-adaptive wear", "tech-integrated outfit",
                "sustainable bio-fabric", "modular fashion",
                "augmented reality gear", "eco-conscious attire",
                "neural interface suit", "smart casual tech-wear"
            ],
            "Cyberpunk": [
                "neon-lit street wear", "high-tech body suit",
                "cyber-enhanced clothing", "digital punk fashion",
                "tech-noir ensemble", "neo-tokyo street style",
                "cybernetic combat gear", "hacker's outfit",
                "corporate cyber suit", "street samurai wear"
            ],
            "Solarpunk": [
                "sustainable bio-fashion", "solar-powered suit",
                "eco-tech clothing", "organic tech wear",
                "living plant clothing", "renewable fashion",
                "biomimicry outfit", "green tech ensemble",
                "sustainable luxury wear", "eco-conscious formal"
            ]
        }
        return base_outfits.get(era, [
            "elegant formal wear", "professional attire",
            "ceremonial costume", "detailed period clothing",
            "traditional garments", "refined formal dress"
        ])

    def get_accessories(self, era: str) -> List[str]:
        base_accessories = {
            # Historical Era Accessories
            "Medieval": [
                "ornate jewelry", "ceremonial sword",
                "decorated belt", "noble's crown",
                "symbolic medallion", "embroidered cape",
                "intricate signet ring", "gilded chalice",
                "ornamental dagger", "heraldic shield"
            ],
            "Renaissance": [
                "detailed headdress", "precious jewels",
                "ceremonial chain", "decorated fan",
                "ornate hat", "symbolic scepter",
                "pearl-studded collar", "feathered mask",
                "embellished codpiece", "ornate pocket sundial"
            ],
            "Victorian": [
                "formal hat", "pocket watch",
                "decorative parasol", "ornate brooch",
                "walking stick", "lace gloves",
                "cameo pendant", "monocle",
                "embroidered handkerchief", "ornamental snuff box"
            ],
            "Ancient Roman": [
                "laurel wreath", "signet ring",
                "fibula brooch", "ceremonial bulla",
                "ornate armband", "decorative stylus"
            ],
            "Ancient Egyptian": [
                "elaborate collar", "sacred scarab amulet",
                "ceremonial staff", "ornate headdress",
                "symbolic ankh", "decorative armlet"
            ],
            "Byzantine": [
                "jeweled diadem", "ornate pectoral cross",
                "elaborate belt buckle", "ceremonial orb",
                "bejeweled book cover", "intricate mosaics"
            ],
            # Modern Era Accessories
            "Contemporary": [
                "smart watch", "wireless earbuds",
                "tablet device", "designer bag",
                "eco-friendly accessories", "tech gadgets",
                "sustainable jewelry", "digital accessories",
                "fitness tracker", "modern eyewear"
            ],
            "Near Future": [
                "holographic display", "neural interface",
                "augmented reality lens", "bio-monitor",
                "smart jewelry", "tech implants",
                "digital assistant", "quantum computer",
                "nano-tech accessories", "biometric scanner"
            ],
            "Cyberpunk": [
                "cyber implants", "neural jack",
                "holographic HUD", "tech modifications",
                "digital interface", "neon accessories",
                "cybernetic enhancements", "data port",
                "augmented reality mods", "tech weapons"
            ],
            "Solarpunk": [
                "living jewelry", "solar accessories",
                "bio-luminescent items", "sustainable tech",
                "organic gadgets", "eco-smart wear",
                "renewable power cells", "natural tech",
                "bio-integrated devices", "green energy tools"
            ]
        }
        return base_accessories.get(era, [
            "period accessories", "detailed ornaments",
            "symbolic items", "decorative elements",
            "traditional jewelry", "ceremonial items"
        ])

    def get_settings(self, era: str, profession: str) -> List[str]:
        modern_settings = [
            "high-tech office", "startup incubator",
            "research laboratory", "digital studio",
            "innovation hub", "tech campus",
            "sustainable building", "smart city street",
            "virtual reality space", "eco-friendly complex",
            "modern university", "creative workspace",
            "urban rooftop garden", "smart home interior",
            "renewable energy facility", "digital art gallery",
            "modern medical center", "space research facility"
        ]
        
        future_settings = [
            "vertical city", "space colony",
            "underwater metropolis", "floating city",
            "biodome complex", "orbital station",
            "eco-arcology", "quantum research lab",
            "cyber-enhanced city", "virtual reality hub",
            "solar punk paradise", "tech noir cityscape",
            "neo-tokyo streets", "mars settlement",
            "artificial habitat", "digital dimension"
        ]
        
        if era in ["Contemporary", "2020s", "Near Future"]:
            return modern_settings
        elif era in ["Cyberpunk", "Solarpunk", "Post-Cyberpunk"]:
            return future_settings
        else:
            return [
                f"{era} {setting}" for setting in [
                    "royal court", "grand palace",
                    "noble estate", "guild hall",
                    "workshop", "marketplace",
                    "garden", "library",
                    "cathedral", "city street"
                ]
            ]

    def get_times_of_day(self) -> List[str]:
        return [
            "golden morning", "bright midday",
            "soft afternoon", "golden hour",
            "dramatic sunset", "mysterious twilight",
            "candlelit evening", "moonlit night"
        ]

    def get_atmospheres(self) -> List[str]:
        return [
            "regal", "mysterious", "scholarly",
            "ceremonial", "professional", "artistic",
            "diplomatic", "sophisticated", "traditional"
        ]

    def get_art_styles(self) -> List[str]:
        return [
            "oil painting", "detailed illustration",
            "classical portrait", "realistic rendering",
            "academic style", "fine art",
            "traditional technique", "masterful composition"
        ]

    def get_lighting_styles(self) -> List[str]:
        return [
            "Rembrandt lighting", "dramatic chiaroscuro",
            "soft natural light", "golden hour glow",
            "candlelight", "window light",
            "atmospheric lighting", "professional studio lighting"
        ]

    def get_color_palettes(self, era: str) -> List[str]:
        base_palettes = {
            # Historical Era Palettes
            "Medieval": [
                "rich jewel tones", "royal colors",
                "deep medieval hues", "traditional pigments",
                "muted earth tones", "heraldic colors"
            ],
            "Renaissance": [
                "renaissance palette", "rich earth tones",
                "classical colors", "natural pigments",
                "sfumato shades", "chiaroscuro contrasts"
            ],
            "Victorian": [
                "sophisticated victorian", "refined palette",
                "elegant tones", "period-appropriate colors",
                "muted pastels", "rich jewel hues"
            ],
            "Ancient Roman": [
                "imperial purples", "marble whites",
                "terracotta reds", "golden ochres",
                "mosaic-inspired hues", "fresco palettes"
            ],
            "Ancient Egyptian": [
                "lapis lazuli blues", "golden yellows",
                "turquoise greens", "papyrus beiges",
                "royal reds", "hieroglyph-inspired tones"
            ],
            "Byzantine": [
                "mosaic golds", "imperial purples",
                "rich vermilions", "celestial blues",
                "emerald greens", "ornate metallic accents"
            ],
            # Modern Era Palettes
            "Contemporary": [
                "modern minimalist", "tech company colors",
                "startup vibrancy", "digital age palette",
                "sustainable earth tones", "smart casual colors",
                "professional modern", "creative workspace hues"
            ],
            "Near Future": [
                "holographic spectrum", "tech-minimal palette",
                "bio-digital colors", "smart material hues",
                "quantum computing glow", "augmented reality tints"
            ],
            "Cyberpunk": [
                "neon noir", "digital punk",
                "tech-noir contrast", "cyber glow",
                "matrix green", "digital decay"
            ],
            "Solarpunk": [
                "natural tech blend", "sustainable future",
                "bio-luminescent", "eco-digital",
                "organic technology", "renewable energy hues"
            ]
        }
        return base_palettes.get(era, [
            "harmonious", "period-appropriate",
            "classical", "traditional",
            "refined", "elegant"
        ])

    def get_special_effects(self) -> List[str]:
        return [
            "volumetric lighting", "atmospheric depth",
            "subtle glow", "perfect shadows",
            "fine details", "texture definition",
            "atmospheric perspective", "perfect rendering"
        ]
