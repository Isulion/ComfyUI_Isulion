from typing import Dict, List, Optional
from .base_handler import BaseThemeHandler
import random

class CharacterDesignerThemeHandler(BaseThemeHandler):
    """Handler for creating detailed character designs with customizable attributes."""

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate a detailed character design with various customizable elements."""
        
        self.debug_print("Generating new prompt...")
        components = {}
        
        # Generate character base
        if custom_subject:
            base_character = custom_subject
        else:
            base_character = random.choice(self.get_character_types())
        
        self.debug_print(f"Selected base character: {base_character}")
        
        # Add profession and role
        profession = random.choice(self.get_professions())
        role_description = random.choice(self.get_role_descriptions())
        
        self.debug_print(f"Selected profession: {profession}")
        self.debug_print(f"Selected role description: {role_description}")
        
        # Generate clothing and accessories
        era = random.choice(self.get_historical_periods())
        outfit = random.choice(self.get_outfits(era))
        accessories = random.choice(self.get_accessories(era))
        
        self.debug_print(f"Selected era: {era}")
        self.debug_print(f"Selected outfit: {outfit}")
        self.debug_print(f"Selected accessories: {accessories}")
        
        # Combine character elements
        components["subject"] = (
            f"((masterful portrait)) of {base_character} as a {profession}, {role_description}, "
            f"((wearing {era} style {outfit})), ((detailed {accessories})), "
            f"((perfect character design)), ((expressive features)), "
            f"((professional quality)), ((character excellence))"
        )
        
        # Generate environment based on profession and era
        if include_environment:
            if custom_location:
                setting = custom_location
            else:
                setting = random.choice(self.get_settings(era, profession))
            
            self.debug_print(f"Selected setting: {setting}")
            
            time_of_day = random.choice(self.get_times_of_day())
            atmosphere = random.choice(self.get_atmospheres())
            
            self.debug_print(f"Selected time of day: {time_of_day}")
            self.debug_print(f"Selected atmosphere: {atmosphere}")
            
            components["environment"] = (
                f"in ((detailed {setting})) during {time_of_day}, "
                f"((with {atmosphere} atmosphere)), ((period-accurate details)), "
                f"((environmental storytelling)), ((perfect composition))"
            )
        
        # Add style elements
        if include_style:
            art_style = random.choice(self.get_art_styles())
            lighting = random.choice(self.get_lighting_styles())
            color_palette = random.choice(self.get_color_palettes(era))
            
            self.debug_print(f"Selected art style: {art_style}")
            self.debug_print(f"Selected lighting: {lighting}")
            self.debug_print(f"Selected color palette: {color_palette}")
            
            components["style"] = (
                f"((masterful {art_style})), ((perfect {lighting})), "
                f"((beautiful {color_palette} color palette)), "
                f"((high detail)), ((professional quality))"
            )
        
        # Add special effects
        if include_effects:
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
            "Solarpunk", "Atompunk", "Dieselpunk",
            # Fantasy Realms
            "Crystal Age", "Mist Kingdom",
            "Clockwork Empire", "Dream Realm",
            "Ethereal Dynasty", "Void Society",
            # Alternative History
            "Steam Victorian", "Diesel Renaissance",
            "Atomic Medieval", "Electric Baroque",
            "Quantum Victorian", "Neon Gothic",
            # Elemental Civilizations
            "Aqua Society", "Terra Kingdom",
            "Aether Empire", "Flame Dynasty",
            "Crystal Republic", "Storm Nation",
            # Fusion Cultures
            "Cyber-Feudal", "Bio-Victorian",
            "Quantum-Medieval", "Techno-Egyptian",
            "Neo-Byzantium", "Solar-Gothic",
            # Conceptual Ages
            "Harmonic Era", "Quantum Age",
            "Dream Epoch", "Mythic Modern",
            "Cosmic Victorian", "Ethereal Future",
            # Nature-Tech Fusion
            "Mycelium Punk", "Coral Society",
            "Forest-Tech", "Crystal-Digital",
            "Bio-Luminescent Era", "Quantum Nature",
            # Abstract Concepts
            "Fractal Society", "Geometric Age",
            "Paradox Era", "Quantum Dream",
            "Probability Kingdom", "Dimension Flux",
            # Elemental Tech
            "Hydro-Digital", "Geo-Tech",
            "Aero-Punk", "Pyro-Future",
            "Crystal-Pulse", "Plasma Age"
        ]

    def get_outfits(self, era: str) -> List[str]:
        """Get era-appropriate outfits."""
        base_outfits = {
            "ancient": [
                "toga with golden trim",
                "ceremonial robes with sacred symbols",
                "battle-worn armor with divine markings",
                "priestly vestments with mystical emblems",
                "royal garments with historical patterns"
            ],
            "medieval": [
                "ornate plate armor with family crest",
                "noble's attire with heraldic designs",
                "wizard's robes with arcane symbols",
                "ranger's leather with forest patterns",
                "merchant's fine clothes with guild insignia"
            ],
            "victorian": [
                "tailored suit with pocket watch",
                "elaborate dress with mechanical accents",
                "inventor's coat with brass fittings",
                "explorer's outfit with scientific tools",
                "aristocrat's garments with industrial motifs"
            ],
            "modern": [
                "sleek business suit with tech accessories",
                "urban streetwear with digital patterns",
                "tactical gear with smart displays",
                "designer outfit with LED accents",
                "professional attire with modern flair"
            ],
            "futuristic": [
                "nanotech bodysuit with glowing circuits",
                "holographic clothing with dynamic patterns",
                "biomechanical armor with energy cores",
                "quantum fabric outfit with phase shifts",
                "plasma-infused suit with force fields"
            ],
            "fantasy": [
                "enchanted robes with floating runes",
                "dragonscale armor with magical gems",
                "fae silk garments with living patterns",
                "celestial cloth with starlight trim",
                "shadowweave suit with darkness flows"
            ],
            "sci_fi": [
                "advanced exosuit with AI interface",
                "zero-g combat armor with thrust units",
                "xenotech outfit with alien materials",
                "dimensional shift suit with reality anchors",
                "quantum phase armor with time dilation"
            ],
            "nature": [
                "living armor made of ancient bark",
                "flowing robes of woven leaves",
                "crystal-growth suit with mineral patterns",
                "root-system stealth suit with earth connection",
                "flower-pattern formal attire with seasonal shifts"
            ]
        }
        return base_outfits.get(era, [
            "elegant formal wear",
            "professional attire",
            "ceremonial costume",
            "detailed period clothing",
            "character-appropriate outfit"
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
            ],
            # Fantasy Realm Accessories
            "Crystal Age": [
                "prismatic crown with energy focusing gems",
                "light-bending amulet with rainbow refraction",
                "crystal-core power source with geometric patterns",
                "light-weaving tools with prismatic edges",
                "crystal matrix interface with data storage",
                "geometric shield generator with energy fields",
                "rainbow-shift communicator with light signals",
                "crystal-tech weapon with energy focusing",
                "light-pattern scanner with analysis crystals",
                "prismatic meditation device with focus gems",
                "crystal-core data storage with memory matrix",
                "light-bending stealth device with cloaking crystals"
            ],
            "Mist Kingdom": [
                "cloud-form crown with weather control",
                "mist-weaver amulet with vapor manipulation",
                "fog-phase communicator with particle transmission",
                "atmospheric controller with pressure regulation",
                "mist-tech scanner with particle analysis",
                "weather-manipulation device with storm control",
                "vapor-phase shield with particle defense",
                "cloud-tech weapon with condensation control",
                "mist-pattern analyzer with humidity sensing",
                "fog-core navigation device with particle tracking",
                "cloud-form meditation aid with atmospheric harmony",
                "mist-weaving tool with vapor shaping"
            ],
            "Clockwork Empire": [
                "mechanical crown with turning gears",
                "chronograph amulet with time display",
                "gear-work compass with navigation mechanics",
                "time-piece calculator with brass workings",
                "mechanical-core tool set with precision instruments",
                "clockwork weapon with timing mechanisms",
                "gear-pattern shield with mechanical defense",
                "chronometer scanner with time analysis",
                "mechanical communicator with gear transmission",
                "time-keeping meditation device with rhythm gears",
                "gear-core power source with energy transmission",
                "clockwork augmentation with precision parts"
            ],
            "Quantum Victorian": [
                "probability crown with quantum state display",
                "wave-function amulet with state manipulation",
                "quantum-core tool set with probability fields",
                "superposition scanner with state analysis",
                "quantum-pattern shield with probability defense",
                "wave-collapse weapon with quantum targeting",
                "probability-field generator with state control",
                "quantum communicator with entangled pairs",
                "wave-form analyzer with quantum sensing",
                "quantum meditation device with state harmony",
                "probability-tech augmentation with quantum cores",
                "wave-pattern interface with quantum control"
            ],
            "Mycelium Punk": [
                "fungal crown with living network",
                "mycelial amulet with spore control",
                "mushroom-core tool set with organic functions",
                "spore-pattern scanner with life analysis",
                "fungal-tech shield with living defense",
                "mycelial weapon with organic targeting",
                "spore-based communicator with network links",
                "fungal analyzer with growth sensing",
                "mushroom meditation aid with network harmony",
                "mycelial augmentation with living parts",
                "spore-tech interface with organic control",
                "fungal-pattern device with colony connection"
            ],
            "Forest-Tech": [
                "living wood crown with growing circuits",
                "leaf-circuit amulet with data processing",
                "root-network tool set with earth sensing",
                "tree-tech scanner with life analysis",
                "branch-pattern shield with organic defense",
                "forest-matrix weapon with natural targeting",
                "leaf-core communicator with photosynthetic power",
                "root analyzer with earth connection",
                "tree meditation device with forest harmony",
                "branch augmentation with living circuits",
                "leaf-pattern interface with seasonal adaptation",
                "forest-tech device with ecosystem integration"
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
            ],
            # Fantasy Realm Palettes
            "Crystal Age": [
                "prismatic spectrum", "crystal clear",
                "rainbow refractions", "geometric light",
                "pure spectrum", "diamond clarity"
            ],
            "Mist Kingdom": [
                "ethereal fog", "cloud whites",
                "misty grays", "vapor blues",
                "atmospheric haze", "nebula shift"
            ],
            "Clockwork Empire": [
                "brass and copper", "mechanical gold",
                "gear-work bronze", "time-worn silver",
                "steam-age metals", "chronograph patina"
            ],
            # Elemental Civilization Palettes
            "Aqua Society": [
                "deep ocean", "coral reef",
                "tidal blues", "marine depths",
                "aquatic aurora", "wave patterns"
            ],
            "Terra Kingdom": [
                "crystal growth", "mineral veins",
                "earth tones", "gem spectrum",
                "geological layers", "stone patterns"
            ],
            # Nature-Tech Fusion Palettes
            "Mycelium Punk": [
                "fungal glow", "spore patterns",
                "mycelial networks", "organic tech",
                "bio-luminescent", "mushroom spectrum"
            ],
            "Forest-Tech": [
                "living circuits", "digital nature",
                "leaf patterns", "root networks",
                "forest matrix", "organic tech blend"
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
