import random
import os

class IsulionMegaPromptGenerator:
    def __init__(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config', 'config_mega.txt')
        
        # Load configurations from file
        self.load_config(config_path)

        # Initialize theme_prefixes and enhancements as instance attributes
        self.theme_prefixes = {
            "anime": "minimalist anime artwork with clean lines of",
            "realistic": "professional studio photograph with precise lighting, ultra-sharp focus, minimalist composition of",
            "sci_fi": "sleek and refined futuristic design, premium finish, elegant technological details of",
            "fantasy": "elegant fantasy artwork with refined details of",
            "cute chimera": "adorable kawaii-style digital artwork with soft pastel colors and fluffy details of",
            "cinema": "premium cinematic composition, studio-grade lighting, professional color grading of",
            "cartoon": "refined animation style with smooth gradients and clean lines of",
            "architecture": "architectural visualization with premium materials, clean lines, and precise details of",
            "abstract": "minimalist abstract artwork featuring clean geometric forms of",
            "random": "premium quality digital artwork with refined details of",
            "food": "professional food photography with elegant plating, studio lighting of",
            "interior": "premium interior design photography with architectural precision of",
            "3D": "high-end 3D visualization with premium materials and precise details of",
            "halloween": "elegantly crafted dark atmosphere with refined details of",
            "instagram": "premium lifestyle photography with professional studio lighting of",
            "strange_animal": "professional wildlife photograph with cinematic lighting of",
            "futuristic_city": "ultra-modern architectural visualization with premium materials of",
            "pixar": "highly detailed Pixar-style 3D render with clean geometry and appealing design of",
            "binet": "highly detailed anthropomorphic portrait, digital painting of",
            "vintage_anthro": "ultra-realistic vintage photograph with professional studio lighting of",
            "star_wars": "cinematic Star Wars scene with premium details of",
            "marvel": "epic Marvel Universe scene with cinematic composition of",
            "steampunk": "Victorian-era steampunk artwork with brass and copper details of",
            "post_apocalyptic": "dramatic post-apocalyptic scene with weathered details of",
            "underwater": "bioluminescent deep-sea photograph with crystalline clarity of",
            "microscopic": "electron microscope visualization with precise detail of",
            "bio_organic": "hybrid bio-mechanical artwork with organic integration of",
            "🎭 Peaky Blinders Style": "professional studio photograph with precise lighting, ultra-sharp focus, minimalist composition of",
            "christmas": "magical christmas artwork with festive details of",
            "caricature": "exaggerated cartoon caricature artwork with strong distortion and comic book style of",
            "logo": "professional logo design with clean typography of",
            "village": "professional photography of a picturesque"
        }
        
        self.enhancements = {
            "detail": {
                "subtle": ["precisely detailed", "refined", "elegantly crafted", "clean", "polished"],
                "moderate": ["meticulously detailed", "premium quality", "professionally crafted", "architectural precision", "studio grade"],
                "dramatic": ["ultra-premium quality", "masterfully engineered", "exceptional craftsmanship", "flawless detail", "perfect precision"]
            },
            "composition": {
                "subtle": ["balanced", "harmonious", "precise", "clean layout", "minimalist"],
                "moderate": ["professionally composed", "elegant arrangement", "refined composition", "premium layout", "architectural balance"],
                "dramatic": ["perfect symmetry", "masterful composition", "ultra-premium arrangement", "flawless balance", "exceptional design"]
            },
            "lighting": {
                "subtle": ["clean lighting", "soft illumination", "precise shadows", "refined highlights", "elegant glow"],
                "moderate": ["professional studio lighting", "premium illumination", "architectural lighting", "controlled shadows", "refined atmosphere"],
                "dramatic": ["ultra-premium lighting", "perfect illumination", "exceptional atmosphere", "masterful light control", "flawless shadows"]
            },
            "color": {
                "subtle": ["refined palette", "harmonious colors", "elegant tones", "clean color scheme", "polished hues"],
                "moderate": ["premium colors", "professional palette", "sophisticated tones", "refined chromatic balance", "controlled saturation"],
                "dramatic": ["exceptional color harmony", "masterful palette", "perfect color balance", "flawless tonal range", "supreme chromatic composition"]
            }
        }

        # Add new logo-specific dictionaries
        self.logo_styles = [
            "minimalist", "modern", "vintage", "retro", "geometric", "abstract",
            "corporate", "artistic", "elegant", "bold", "playful", "luxurious",
            "tech-inspired", "organic", "grunge", "clean", "dynamic"
        ]

        self.logo_fonts = [
            "elegant serif", "bold sans-serif", "modern geometric", "classic script",
            "minimalist sans", "decorative display", "clean monospace", "artistic handwritten",
            "professional slab serif", "futuristic tech", "vintage letterpress", "luxury script",
            "bold condensed", "elegant thin", "modern rounded", "sharp angular"
        ]

        self.logo_elements = [
            "geometric shapes", "abstract forms", "clean lines", "organic curves",
            "minimalist icons", "dynamic patterns", "gradient meshes", "textured backgrounds",
            "symmetrical designs", "flowing elements", "angular components", "circular motifs",
            "hexagonal patterns", "wave forms", "crystalline structures", "nested shapes"
        ]

        self.logo_colors = [
            "professional monochrome", "vibrant duotone", "elegant metallic",
            "bold gradient", "subtle pastel", "rich jewel tones", "modern neon",
            "classic earth tones", "minimalist grayscale", "corporate blue",
            "luxury gold and black", "tech-inspired cyan", "organic green",
            "energetic red", "sophisticated purple"
        ]

        self.logo_effects = [
            "subtle shadow", "clean emboss", "metallic finish", "glass effect",
            "neon glow", "gradient overlay", "paper texture", "brushed metal",
            "holographic shine", "matte finish", "glossy surface", "3D extrusion",
            "light reflection", "depth layers", "geometric pattern"
        ]

        # Add these new dictionaries after the existing logo dictionaries

        self.logo_3d_styles = [
            "fluffy 3D", "liquid metal", "balloon-like", "plush toy", "candy-colored",
            "neon-lit", "crystal glass", "metallic chrome", "soft fabric", "paper craft",
            "inflated", "bubble", "jelly", "holographic", "gradient mesh"
        ]

        self.logo_themes = [
            "playful", "professional", "cute", "artistic", "minimalist", "3D typography",
            "character-based", "illustrated", "hand-crafted", "digital art"
        ]

        self.logo_characters = [
            "cute bird", "friendly sloth", "adorable monster", "happy creature",
            "kawaii animal", "charming mascot", "sweet character", "lovely creature"
        ]

        self.logo_decorative_elements = [
            "floral patterns", "magical sparkles", "cute doodles", "organic swirls",
            "celestial elements", "nature motifs", "geometric accents", "playful icons",
            "mystical symbols", "decorative frames"
        ]

        # Add these new dictionaries after other theme-specific dictionaries

        self.village_types = [
            "mountain village", "coastal fishing village", "desert oasis settlement", 
            "tropical island village", "medieval European hamlet", "Nordic fjord settlement",
            "Mediterranean hillside town", "Japanese mountain village", "Alpine ski village",
            "Moroccan desert village", "Greek island settlement", "Tuscan hilltop town",
            "Swiss alpine hamlet", "Himalayan mountain settlement", "Vietnamese floating village",
            "African savanna village", "Peruvian mountain pueblo", "Scottish highland village",
            "Dutch windmill village", "Turkish coastal town", "Irish countryside settlement"
        ]

        self.village_architecture = [
            "traditional stone houses", "thatched-roof cottages", "timber-frame buildings",
            "whitewashed buildings", "terracotta-roofed homes", "stilt houses",
            "adobe dwellings", "wooden chalets", "slate-roofed cottages", "clay brick houses",
            "bamboo structures", "turf-roofed homes", "colorful painted houses",
            "half-timbered buildings", "red-tile roofed homes", "cobblestone streets",
            "wooden boardwalks", "stone pathways", "ancient stone walls"
        ]

        self.village_cultural_elements = [
            "local market stalls", "traditional fishing boats", "ancient water wells",
            "community gathering spaces", "religious temples", "village squares",
            "communal gardens", "historic fountains", "traditional windmills",
            "cultural monuments", "craft workshops", "village church", "prayer flags",
            "ceremonial spaces", "traditional decorations", "folk art displays"
        ]

        self.landscape_features = [
            "rolling hills", "terraced fields", "flowering meadows", "ancient forests",
            "dramatic cliffs", "pristine beaches", "mountain peaks", "flowing rivers",
            "cascading waterfalls", "natural hot springs", "crystal-clear lakes",
            "volcanic formations", "desert dunes", "coral reefs", "glacial valleys",
            "autumn forests", "spring cherry blossoms", "lavender fields", "rice paddies",
            "olive groves", "vineyard slopes", "alpine meadows"
        ]

        self.landscape_atmospheres = [
            "misty morning", "golden sunset", "starlit night", "stormy atmosphere",
            "peaceful dawn", "ethereal fog", "clear mountain air", "tropical breeze",
            "autumn colors", "spring awakening", "summer warmth", "winter silence",
            "monsoon rains", "desert winds", "northern lights", "rainbow after rain"
        ]

    def load_config(self, config_path):
        """Load configurations from the specified file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            config_text = f.read()
            
        # Execute the config file content in a safe local namespace
        namespace = {}
        exec(config_text, {}, namespace)
        
        # Transfer all variables to class attributes
        for key, value in namespace.items():
            setattr(self, key, value)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "theme": ([
                    "🎲 Dynamic Random",  # Keeps Random at top
                    "🎨 Abstract",
                    "📺 Animation Cartoon", 
                    "🎌 Anime",
                    "🏛️ Architectural",
                    "🧬 Bio-Organic Technology",
                    "🖼️ Binet Surreal",
                    "✏️ Caricature",  
                    "🦄 Chimera Animals",
                    "🐰 Chimera Cute Animals",
                    "🎅 Christmas",
                    "🎬 Cinema Studio",
                    "🍳 Culinary/Food",
                    "💠 Dimension 3D",
                    "✨ Enchanted Fantasy",
                    "📸 Essential Realistic",
                    "🌆 Futuristic City Metropolis", 
                    "🚀 Futuristic Sci-Fi",
                    "👻 Halloween Ethereal",
                    "📱 Instagram Lifestyle",
                    "🏠 Interior Spaces",
                    "🦸‍♂️ Marvel Universe",
                    "🔬 Microscopic Universe",
                    "🎭 Peaky Blinders Style",
                    "💫 Pixar Animation",
                    "☢️ Post-Apocalyptic Wasteland",
                    "⭐ Star Wars Universe",
                    "⚙️ Steampunk Cities",
                    "🌊 Underwater Civilization",
                    "🎩 Vintage Anthropomorphic",
                    "🏷️ Logo",
                    "🏘️ Village Of the World"
                ], {"default": "🎲 Dynamic Random"}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "use_custom_subject": (["yes", "no"], {"default": "no"}),
                "include_subject": (["yes", "no"], {"default": "yes"}),
                "include_action": (["yes", "no"], {"default": "yes"}),
                "include_environment": (["yes", "no"], {"default": "yes"}),
                "include_style": (["yes", "no"], {"default": "yes"}),
                "include_effects": (["yes", "no"], {"default": "yes"}),
                "enhancement_level": (["subtle", "moderate", "dramatic"], {"default": "moderate"}),
                "enhancement_focus": (["detail", "composition", "lighting", "color"], {"default": "detail"}),
            }
        }
    
    RETURN_TYPES = (
        "STRING",  # combined prompt
        "STRING",  # subject
        "STRING",  # action
        "STRING",  # environment
        "STRING",  # style
        "STRING",  # effects
        "INT",     # seed
    )
    RETURN_NAMES = (
        "prompt",
        "subject",
        "action",
        "environment",
        "style",
        "effects",
        "seed",
    )
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, theme, complexity, randomize, seed=0, 
                custom_subject="", use_custom_subject="no",
                include_subject="yes", include_action="yes", 
                include_environment="yes", include_style="yes",
                include_effects="yes", enhancement_level="moderate",
                enhancement_focus="detail"):
        
        # Move theme_prefixes and enhancements from class attributes to instance attributes
        if not hasattr(self, 'theme_prefixes'):
            self.__init__()

        # Create a mapping between new and old theme names
        theme_mapping = {
            "🎨 Abstract": "abstract",
            "🎌 Anime": "anime",
            "📺 Animation Cartoon": "cartoon",
            "🏛️ Architectural": "architecture",
            "🖼️ Binet Surreal": "binet",
            "🧬 Bio-Organic Technology": "bio_organic", 
            "✏️ Caricature": "caricature",
            "🦄 Chimera Animals": "strange_animal",
            "🐰 Chimera Cute Animals": "cute chimera",
            "🎬 Cinema Studio": "cinema",
            "🎅 Christmas": "christmas",
            "🍳 Culinary/Food": "food",
            "💠 Dimension 3D": "3D",
            "🎲 Dynamic Random": "random",
            "📸 Essential Realistic": "realistic",
            "✨ Enchanted Fantasy": "fantasy",
            "🚀 Futuristic Sci-Fi": "sci_fi",
            "🌆 Futuristic City Metropolis": "futuristic_city",
            "👻 Halloween Ethereal": "halloween",
            "🏠 Interior Spaces": "interior",
            "📱 Instagram Lifestyle": "instagram",
            "🦸‍♂️ Marvel Universe": "marvel",
            "🔬 Microscopic Universe": "microscopic",
            "🎭 Peaky Blinders Style": "peaky_blinders",
            "💫 Pixar Animation": "pixar",
            "☢️ Post-Apocalyptic Wasteland": "post_apocalyptic",
            "⭐ Star Wars Universe": "star_wars",
            "⚙️ Steampunk Cities": "steampunk",
            "🌊 Underwater Civilization": "underwater",
            "🎩 Vintage Anthropomorphic": "vintage_anthro",
            "🏷️ Logo": "logo",
            "🏘️ Village Of the World": "village"
        }

        # Convert new theme name to old theme name for internal processing
        internal_theme = theme_mapping.get(theme, theme)

        if randomize == "enable":
            seed = random.randint(0, 0xffffffffffffffff) if seed == 0 else seed
            random.seed(seed)

        # Handle logo theme before other processing
        if internal_theme == "logo":
            # Determine logo style approach
            style_approach = random.choice([
                "classic", "3D", "character", "artistic"  # Different approaches to logo design
            ])
            
            # Create the main subject with custom text
            if use_custom_subject == "yes" and custom_subject.strip():
                logo_text = custom_subject.strip()
            else:
                logo_text = "BRAND"
            
            if style_approach == "classic":
                # Original classic logo style
                style = random.choice(self.logo_styles)
                font = random.choice(self.logo_fonts)
                element = random.choice(self.logo_elements)
                color_scheme = random.choice(self.logo_colors)
                
                subject_text = (
                    f"((professional {style} logo design)) with the text \"{logo_text}\", "
                    f"((using {font} typography)), ((perfect letter spacing)), "
                    f"((masterful font design)), ((vector quality))"
                )
            
            elif style_approach == "3D":
                # 3D typography style
                style_3d = random.choice(self.logo_3d_styles)
                color_scheme = random.choice(self.logo_colors)
                
                subject_text = (
                    f"((highly detailed {style_3d} 3D typography)) of the text \"{logo_text}\", "
                    f"((volumetric letters)), ((dimensional depth)), "
                    f"((perfect 3D modeling)), ((ultra-detailed materials))"
                )
            
            elif style_approach == "character":
                # Character-based logo style
                character = random.choice(self.logo_characters)
                decorative = random.choice(self.logo_decorative_elements)
                
                subject_text = (
                    f"((adorable {character} mascot logo)) with the text \"{logo_text}\", "
                    f"((cute character design)), ((playful typography)), "
                    f"((charming illustration)), ((kawaii style))"
                )
            
            else:  # artistic
                # Artistic illustrated logo style
                theme = random.choice(self.logo_themes)
                decorative = random.choice(self.logo_decorative_elements)
                
                subject_text = (
                    f"((creative {theme} logo artwork)) with the text \"{logo_text}\", "
                    f"((artistic typography)), ((illustrated elements)), "
                    f"((unique design)), ((hand-crafted style))"
                )
            
            # Initialize components with subject
            components = [subject_text]
            
            # Add environment/background if enabled
            if include_environment == "yes":
                if style_approach == "3D":
                    environment_text = (
                        f"with ((perfect lighting setup)), ((studio environment)), "
                        f"((professional composition)), ((clean background))"
                    )
                elif style_approach == "character":
                    environment_text = (
                        f"with ((cute {decorative})), ((playful composition)), "
                        f"((charming background)), ((balanced layout))"
                    )
                else:
                    element = random.choice(self.logo_elements)
                    environment_text = (
                        f"with ((clean {element})), ((perfect composition)), "
                        f"((balanced negative space)), ((professional layout))"
                    )
                components.append(environment_text)
            
            # Add style elements
            if include_style == "yes":
                if style_approach == "3D":
                    style_text = (
                        f"((premium 3D rendering)), ((perfect materials)), "
                        f"((professional lighting)), ((high-end finish)), "
                        f"((commercial quality)), ((volumetric effects)), "
                        f"((brand identity)), 8k resolution"
                    )
                elif style_approach == "character":
                    style_text = (
                        f"((kawaii aesthetic)), ((cute color palette)), "
                        f"((playful design)), ((perfect proportions)), "
                        f"((charming style)), ((mascot branding)), "
                        f"((brand identity)), 8k resolution"
                    )
                else:
                    color_scheme = random.choice(self.logo_colors)
                    style_text = (
                        f"((premium {color_scheme} palette)), ((vector art)), "
                        f"((professional design)), ((perfect proportions)), "
                        f"((commercial quality)), ((scalable graphics)), "
                        f"((brand identity)), 8k resolution"
                    )
                components.append(style_text)
            
            # Add effects
            if include_effects == "yes":
                if style_approach == "3D":
                    effect = random.choice([
                        "subsurface scattering", "metallic reflections", "glossy finish",
                        "ambient occlusion", "volumetric lighting", "depth of field",
                        "material roughness", "displacement mapping"
                    ])
                    effects_text = (
                        f"with (({effect})), ((perfect shadows)), "
                        f"((realistic materials)), ((professional rendering)), "
                        f"((3D effects)), ((depth and volume))"
                    )
                elif style_approach == "character":
                    effect = random.choice([
                        "cute shadows", "playful highlights", "soft glow",
                        "charming details", "kawaii effects", "adorable accents"
                    ])
                    effects_text = (
                        f"with (({effect})), ((sweet details)), "
                        f"((playful elements)), ((charming finish)), "
                        f"((mascot personality)), ((cute aesthetics))"
                    )
                else:
                    effect = random.choice(self.logo_effects)
                    effects_text = (
                        f"with (({effect})), ((clean edges)), "
                        f"((perfect symmetry)), ((professional finish)), "
                        f"((brand consistency)), ((timeless design))"
                    )
                components.append(effects_text)

            # Join components and add enhancement
            prompt = ", ".join(components)
            if enhancement_level in self.enhancements[enhancement_focus]:
                enhancement = random.choice(self.enhancements[enhancement_focus][enhancement_level])
                prompt = f"{prompt}, {enhancement}"
                effects_text = f"{effects_text}, {enhancement}"

            return (prompt, subject_text, "", environment_text, style_text, effects_text, seed)

        # For all other themes, continue with existing logic...
        components = []
        
        # Add theme prefix at the start
        prefix = self.theme_prefixes.get(internal_theme, "")
        if prefix:
            components.append(prefix)

        subject_text = ""
        action_text = ""
        environment_text = ""
        style_text = ""
        effects_text = ""

        if internal_theme == "caricature":
            # Use custom subject if provided, otherwise default to "Donald Trump"
            if use_custom_subject == "yes" and custom_subject.strip():
                subject = custom_subject.strip()
            else:
                subject = "Donald Trump"
            
            # Select cartoon elements
            style = random.choice(self.caricature_styles)
            features = random.choice(self.caricature_features)
            expression = random.choice(self.caricature_expressions)
            
            subject_text = (
                f"((highly exaggerated cartoon caricature)) of {subject}, "  # Added 'highly' and 'cartoon'
                f"with ((extremely {features})), "  # Added 'extremely'
                f"((showing a {expression})), "
                f"((cartoon-style exaggeration)), "  # Added this
                f"((comic book distortion)), "  # Added this
                f"((animated caricature style))"  # Added this
            )
            
            # Initialize components with subject
            components = [subject_text]
            
            # Add environment if enabled
            if include_environment == "yes":
                elements = random.choice(self.caricature_elements)
                setting = random.choice(self.caricature_settings)
                weather = random.choice(self.weather)
                time = random.choice(self.times)
                environment_text = (
                    f"in a ((detailed {setting})) during {weather} {time}, "
                    f"with ((meaningful {elements})), ((caricature composition)), "
                    f"((artistic atmosphere)), ((contextual details))"
                )
                components.append(environment_text)
            
            # Add style elements
            if include_style == "yes":
                style_text = (
                    f"((cartoon caricature style)), ((extreme exaggeration)), "  # Modified
                    f"((comic book interpretation)), ((animated style)), "  # Modified
                    f"((cartoon artwork)), ((exaggerated features)), "  # Modified
                    f"((non-realistic style)), ((cartoon distortion)), "  # Added these
                    f"8k resolution"
                )
                components.append(style_text)
            
            # Add effects if enabled
            if include_effects == "yes":
                effect = random.choice(self.caricature_effects)
                additional_effect = random.choice([
                    "personality highlighting", "character emphasis",
                    "mood enhancement", "emotional resonance",
                    "distinctive portrayal", "unique interpretation"
                ])
                effects_text = (
                    f"with {effect}, ((cartoon effects)), "  # Added 'cartoon effects'
                    f"((animated style)), ((comic book shading)), "  # Added these
                    f"((exaggerated proportions)), ((cartoon physics)), "  # Added these
                    f"((non-photorealistic rendering)), ((cartoon coloring)), "  # Added these
                    f"(({additional_effect})), ((distinctive style))"
                )
                components.append(effects_text)
                
            # Return early for caricature theme to avoid default handling
            prompt = ", ".join(components)
            if enhancement_level in self.enhancements[enhancement_focus]:
                enhancement = random.choice(self.enhancements[enhancement_focus][enhancement_level])
                prompt = f"{prompt}, {enhancement}"
                effects_text = f"{effects_text}, {enhancement}"
            return (prompt, subject_text, action_text, environment_text, style_text, effects_text, seed)
            
        elif internal_theme == "abstract":
            # Special handling for abstract theme - completely separate from other themes
            abstract_components = [prefix] if prefix else []
            
            # Core abstract elements
            primary = random.choice([
                "geometric", "organic", "linear", "circular", "angular",
                "fluid", "crystalline", "prismatic", "recursive", "fractal"
            ])
            element = random.choice(self.abstract_elements)
            style = random.choice(self.abstract_styles)
            
            abstract_components.append(f"{style} {primary} composition with {element}")
            
            # Abstract-specific effects
            effect1 = random.choice([
                "intersecting", "overlapping", "radiating", "repeating",
                "dissolving", "merging", "fragmenting", "tessellating",
                "undulating", "oscillating", "bifurcating", "converging"
            ])
            effect2 = random.choice([
                "forms", "shapes", "patterns", "structures",
                "compositions", "arrangements", "configurations",
                "constructions", "formations", "geometries"
            ])
            
            abstract_components.append(f"with {effect1} {effect2}")
            
            prompt = ", ".join(abstract_components)
            return (prompt, abstract_components[1], "", "", "", abstract_components[2], seed)

        # Subject generation
        if include_subject == "yes":
            if use_custom_subject == "yes" and custom_subject.strip():
                subject_text = custom_subject.strip()
                
                # Special handling for strange_animal theme with custom subject
                if internal_theme == "strange_animal":
                    def get_animal_family(animal):
                        animal_lower = animal.lower()
                        for family, members in self.animal_families.items():
                            if any(member in animal_lower for member in members):
                                return family
                        return None

                    # Use the custom subject as the head animal (changed from body)
                    head = subject_text
                    
                    # Get a body animal and ensure it's from a different family
                    max_attempts = 20
                    while max_attempts > 0:
                        head = random.choice(self.animals)
                        body = random.choice(self.animals)
                        
                        # Check if they're from different families
                        head_family = get_animal_family(head)
                        body_family = get_animal_family(body)
                        
                        if (head_family != body_family and 
                            head_family is not None and 
                            body_family is not None and 
                            head.lower() != body.lower()):
                            break
                            
                        max_attempts -= 1
                    
                    subject_text = f"a complex raw photograph of an intricated chimerical fantastical creature with ((the body of a {body})) and ((the head of a {head})), bokeh background, cinematic lighting, shallow depth of field, 35mm wide angle lens, sharp focus, cinematic film still, dynamic angle, Photography, 8k, masterfully detailed"
                
                components.append(subject_text)
            else:
                if internal_theme == "futuristic_city":
                    # Select base elements
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for aerial cityscape
                        architecture = random.choice(self.futuristic_city_elements["architecture"])
                        infrastructure = random.choice(self.futuristic_city_elements["infrastructure"])
                        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
                        subject_text = (
                            f"((epic aerial view)) of a ((massive futuristic megacity)) with "
                            f"((towering {architecture})) and ((advanced {infrastructure})), "
                            f"((in {atmosphere} atmosphere)), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for street level
                        architecture = random.choice(self.futuristic_city_elements["architecture"])
                        infrastructure = random.choice(self.futuristic_city_elements["infrastructure"])
                        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
                        subject_text = (
                            f"((immersive street-level view)) of a ((futuristic metropolis)) with "
                            f"((detailed {architecture})) and ((intricate {infrastructure})), "
                            f"((in {atmosphere} atmosphere)), {composition}"
                        )
                    else:  # 30% chance for establishing shot
                        architecture = random.choice(self.futuristic_city_elements["architecture"])
                        infrastructure = random.choice(self.futuristic_city_elements["infrastructure"])
                        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
                        subject_text = (
                            f"((epic establishing shot)) of a ((vast futuristic city)) with "
                            f"((majestic {architecture})) and ((complex {infrastructure})), "
                            f"((in {atmosphere} atmosphere)), {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice(self.futuristic_city_elements["time"])
                        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
                        environment_text = (
                            f"during {time}, ((with {atmosphere} atmosphere)), "
                            f"((advanced technology)), ((cyberpunk elements)), "
                            f"((futuristic urban landscape))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((ultra detailed cityscape)), ((sci-fi aesthetic)), "
                            f"((futuristic architecture)), ((advanced technology)), "
                            f"((cinematic scale)), ((urban complexity)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((neon lighting)), ((holographic displays)), "
                            f"((volumetric fog)), ((light rays)), ((energy effects)), "
                            f"((reflective surfaces)), ((atmospheric perspective))"
                        )
                        components.append(effects_text)
                elif internal_theme == "strange_animal":
                    def get_animal_family(animal):
                        animal_lower = animal.lower()
                        for family, members in self.animal_families.items():
                            if any(member in animal_lower for member in members):
                                return family
                        return None

                    # Get animals from different families
                    max_attempts = 20
                    head = None
                    body = None
                    
                    while max_attempts > 0:
                        head_candidate = random.choice(self.animals)
                        body_candidate = random.choice(self.animals)
                        
                        # Check if they're from different families and not the same animal
                        head_family = get_animal_family(head_candidate.lower())
                        body_family = get_animal_family(body_candidate.lower())
                        
                        if (head_family != body_family and 
                            head_family is not None and 
                            body_family is not None and 
                            head_candidate.lower() != body_candidate.lower()):
                            head = head_candidate
                            body = body_candidate
                            break
                            
                        max_attempts -= 1
                    
                    # If we couldn't find a valid combination, use fallback animals
                    if head is None or body is None:
                        head = "Lion"  # From felines family
                        body = "Eagle"  # From birds family
                    
                    # Create a more detailed and structured prompt
                    subject_text = (
                        f"a complex raw photograph of an intricated chimerical fantastical creature with "
                        f"((the body of a {body})) and ((the head of a {head})), "
                        f"bokeh background, cinematic lighting, shallow depth of field, "
                        f"35mm wide angle lens, sharp focus, cinematic film still, "
                        f"dynamic angle, Photography, 8k, masterfully detailed, hyper-realistic"
                    )
                    
                    # Add the subject to components list
                    components = [subject_text]
                    
                elif internal_theme == "fantasy":
                    # Select base elements
                    race = random.choice(self.races)
                    profession = random.choice(self.professions)
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for warrior/combat scene
                        weapon = random.choice(self.artifacts["weapon"])
                        armor = random.choice(self.artifacts["armor"])
                        magic = random.choice(self.magical_effects["arcane"])
                        subject_text = (
                            f"epic fantasy scene of a {race} {profession} "
                            f"wielding ((legendary {weapon})), wearing ((enchanted {armor})), "
                            f"channeling {magic}, {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for magical/mystical scene
                        jewelry = random.choice(self.artifacts["jewelry"])
                        magic_nature = random.choice(self.magical_effects["nature"])
                        magic_fire = random.choice(self.magical_effects["fire"])
                        subject_text = (
                            f"mystical portrait of a {race} {profession} "
                            f"wearing ((magical {jewelry})), conjuring {magic_nature} "
                            f"and {magic_fire}, {composition}"
                        )
                    else:  # 30% chance for exploration/adventure scene
                        armor = random.choice(self.artifacts["armor"])
                        magic_ice = random.choice(self.magical_effects["ice"])
                        subject_text = (
                            f"fantasy adventure scene of a {race} {profession} "
                            f"wearing ((mystical {armor})), surrounded by {magic_ice}, "
                            f"{composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        location = random.choice(self.mythical_locations)
                        weather = random.choice(self.weather)
                        time = random.choice(self.times)
                        magic_lightning = random.choice(self.magical_effects["lightning"])
                        environment_text = (
                            f"in a ((magical {location})) during {weather} {time}, "
                            f"with {magic_lightning} in the sky, "
                            f"((fantasy atmosphere)), ((mythical realm))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((epic fantasy art)), ((magical atmosphere)), "
                            f"((detailed fantasy illustration)), ((dramatic lighting)), "
                            f"((mythical quality)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        magic_arcane = random.choice(self.magical_effects["arcane"])
                        effects_text = (
                            f"with {magic_arcane}, ((magical particles)), "
                            f"((glowing runes)), ((ethereal atmosphere)), "
                            f"((mystical energy)), ((fantasy effects))"
                        )
                        components.append(effects_text)
                elif internal_theme == "abstract":
                    # More pure abstract elements
                    primary = random.choice([
                        "geometric", "organic", "linear", "circular", "angular",
                        "fluid", "crystalline", "prismatic", "recursive", "fractal"
                    ])
                    element = random.choice(self.abstract_elements)
                    style = random.choice(self.abstract_styles)
                    subject_text = f"{style} {primary} composition with {element}"
                elif internal_theme == "cartoon":
                    # Select base elements
                    character = random.choice(self.cartoon_characters)
                    composition = random.choice(self.compositions)
                    
                    # Create dynamic cartoon action
                    action = random.choice([
                        "in a wacky chase scene",
                        "performing slapstick comedy",
                        "in a funny situation",
                        "with exaggerated expression",
                        "in a comedic moment",
                        "doing silly antics",
                        "in classic cartoon style",
                        "with cartoon physics",
                        "in animated mayhem",
                        "with classic cartoon expressions"
                    ])
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((classic cartoon animation)) of {character} {action}, "
                        f"((animated style)), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment = random.choice([
                            "cartoon world", "animated landscape", "classic cartoon background",
                            "wacky environment", "cartoon city", "animated forest",
                            "cartoon household", "silly cartoon setting", "animated playground",
                            "cartoon wonderland"
                        ])
                        environment_text = (
                            f"in a ((vibrant {environment})), "
                            f"((cartoon physics)), ((animated atmosphere))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((classic animation style)), ((cartoon art)), "
                            f"((hand-drawn animation)), ((bold colors)), "
                            f"((exaggerated features)), ((smooth animation)), "
                            f"((cartoon shading)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((cartoon effects)), ((animation smears)), "
                            f"((impact stars)), ((speed lines)), ((cartoon physics)), "
                            f"((exaggerated motion)), ((animated expressions))"
                        )
                        components.append(effects_text)
                elif internal_theme == "cute chimera":
                    def get_animal_family(animal):
                        animal_lower = animal.lower()
                        for family, members in self.animal_families.items():
                            if any(member in animal_lower for member in members):
                                return family
                        return None

                    # Get animals from different families
                    max_attempts = 20
                    head = None
                    body = None
                    
                    while max_attempts > 0:
                        # Select from cute_animals list
                        head_candidate = random.choice(self.cute_animals)
                        body_candidate = random.choice(self.cute_animals)
                        
                        # Clean up the animal names - remove age/size indicators
                        head_clean = head_candidate.lower()
                        body_clean = body_candidate.lower()
                        
                        # Remove age/size indicators and clean up names
                        for prefix in ['baby ', 'cub', 'puppy', 'kitten', 'kit', 'young ', 'little ']:
                            head_clean = head_clean.replace(prefix, '')
                            body_clean = body_clean.replace(prefix, '')
                        
                        # Check if they're from different families and not the same animal
                        head_family = get_animal_family(head_clean)
                        body_family = get_animal_family(body_clean)
                        
                        if (head_family != body_family and 
                            head_family is not None and 
                            body_family is not None and 
                            head_clean != body_clean):
                            head = head_candidate  # Use original cute names
                            body = body_candidate
                            break
                            
                        max_attempts -= 1
                    
                    # Fallback to ensure we always have valid animals from different families
                    if head is None or body is None:
                        head = "Baby Red Panda"  # Cute default head from one family
                        body = "Arctic Fox Kit"  # Cute default body from different family
                    
                    behavior = random.choice(self.behaviors)
                    subject_text = (
                        f"adorable chimerical fantastical creature with "
                        f"((the body of a {body})) and ((the head of a {head})), "
                        f"{behavior}, ((kawaii style)), ((soft lighting)), "
                        f"((pastel colors)), ((cute expression)), ((fluffy texture)), "
                        f"((chibi proportions)), ((sparkly eyes)), ultra detailed, 8k"
                    )
                    
                    # Add the subject text to components immediately after creating it
                    components = [subject_text]  # Initialize components with subject_text
                elif internal_theme == "cinema":
                    # Select character and base elements
                    character = random.choice(self.cinema_characters)
                    composition = random.choice(self.compositions)
                    
                    # Create action with more cinematic flair
                    action = random.choice([
                        "in an epic action sequence",
                        "in a dramatic confrontation",
                        "in a tense standoff",
                        "performing a signature move",
                        "making a dramatic entrance",
                        "in a climactic battle",
                        "in a stealth mission",
                        "in pursuit",
                        "preparing for combat",
                        "defending against enemies"
                    ])
                    
                    # Create detailed subject description
                    subject_text = f"cinematic shot of {character} {action}, {composition}"
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice(self.times)
                        weather = random.choice(self.weather)
                        habitat = random.choice(self.habitats)
                        environment_text = f"in {habitat} during {weather} {time}"
                        components.append(environment_text)
                    
                    # Add style elements specific to cinema
                    if include_style == "yes":
                        style_text = (
                            f"((cinematic lighting)), ((movie quality)), "
                            f"((professional cinematography)), ((dramatic framing)), "
                            f"((photorealistic)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((lens flare)), ((atmospheric haze)), "
                            f"((volumetric lighting)), ((dramatic shadows)), "
                            f"((depth of field)), ((film grain))"
                        )
                        components.append(effects_text)
                elif internal_theme == "anime":
                    # Select base elements with better utilization of anime-specific classes
                    style = random.choice(self.anime_styles)
                    character = random.choice(self.anime_characters)
                    expression = random.choice(self.anime_expressions)
                    emotion = random.choice(self.anime_emotions)
                    action = random.choice(self.anime_actions)
                    environment = random.choice(self.anime_environments)
                    effect = random.choice(self.anime_effects)
                    composition = random.choice(self.anime_compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((high quality {style})) of {character} with {expression} showing {emotion}"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add action if enabled
                    if include_action == "yes":
                        action_text = f"{action}, {composition}"
                        components.append(action_text)
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice(["sunset", "dawn", "golden hour", "night", "afternoon"])
                        environment_text = f"in {environment} during {time}"
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((masterful anime artwork)), ((detailed line art)), "
                            f"((perfect anime illustration)), ((high quality anime key visual)), "
                            f"vibrant colors, beautiful lighting, expert composition"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with {effect}, ((anime aesthetic)), ((manga style)), "
                            f"detailed shading, clean lines, perfect anatomy"
                        )
                        components.append(effects_text)
                elif internal_theme == "architecture":
                    # Select base elements
                    style = random.choice(self.architecture_styles)
                    element = random.choice(self.architecture_elements)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((architectural photography)) of ((detailed {style} {element})), "
                        f"((masterful composition)), {composition}"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice(self.times)
                        weather = random.choice(self.weather)
                        environment_text = (
                            f"during {time} with {weather}, "
                            f"((perfect natural lighting)), ((architectural details)), "
                            f"((premium materials)), ((dramatic perspective))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((professional architectural photography)), ((ultra sharp focus)), "
                            f"((perfect exposure)), ((dramatic angles)), "
                            f"((architectural visualization)), ((premium quality)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((volumetric lighting)), ((perfect shadows)), "
                            f"((detailed textures)), ((reflective surfaces)), "
                            f"((architectural materials)), ((precise geometry))"
                        )
                        components.append(effects_text)
                elif internal_theme == "sci_fi":
                    # Select base elements
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type with expanded probabilities
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for character
                        # Character-focused scene
                        tech_augment = random.choice(self.technology["augments"])
                        tech_gadget = random.choice(self.technology["gadgets"])
                        clothing = random.choice(self.clothing["sci_fi"])
                        subject_text = (
                            f"futuristic character with ((advanced {tech_augment})) and "
                            f"((high-tech {tech_gadget})), wearing {clothing}, {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for spacecraft
                        # Spacecraft scene
                        ship = random.choice(self.spacecraft["military"])
                        tech_weapon = random.choice(self.technology["weapons"])
                        subject_text = (
                            f"advanced ((sci-fi {ship})) equipped with {tech_weapon}, "
                            f"((detailed mechanical design)), {composition}"
                        )
                    else:  # 30% chance for cityscape
                        # Cityscape scene
                        atmosphere = random.choice(self.alien_world_elements["atmospheres"])
                        terrain = random.choice(self.alien_world_elements["terrains"])
                        feature = random.choice(self.alien_world_elements["features"])
                        subject_text = (
                            f"futuristic cityscape with {atmosphere} atmosphere, "
                            f"featuring {terrain} and {feature}, {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        # Use alien world elements for environment
                        color = random.choice(self.alien_world_elements["colors"])
                        feature = random.choice(self.alien_world_elements["features"])
                        environment_text = (
                            f"in a {color} alien world with {feature}, "
                            f"((advanced technology)), ((futuristic architecture))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((sci-fi aesthetic)), ((futuristic design)), "
                            f"((high-tech details)), ((advanced technology)), "
                            f"((cyberpunk elements)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((holographic displays)), ((energy effects)), "
                            f"((neon lighting)), ((technological glow)), "
                            f"((volumetric fog)), ((metallic reflections))"
                        )
                        components.append(effects_text)
                elif internal_theme == "food":
                    # Select base elements
                    food = random.choice(self.food_types)
                    style = random.choice(self.food_styles)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"professional food photograph of {style} {food}, "
                        f"((mouth-watering details)), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        setting = random.choice([
                            "rustic wooden table", "marble counter", "elegant plate",
                            "vintage dish", "modern platter", "chef table", 
                            "restaurant setting", "professional studio setup",
                            "minimalist white surface", "artisanal ceramic plate",
                            "luxury dining table", "gourmet presentation"
                        ])
                        environment_text = (
                            f"on {setting}, ((perfect composition)), "
                            f"((professional food styling)), ((studio lighting))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((professional food photography)), ((ultra sharp focus)), "
                            f"((commercial quality)), ((perfect exposure)), "
                            f"((culinary photography)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((soft depth of field)), ((perfect color balance)), "
                            f"((steam effects)), ((fresh ingredients)), "
                            f"((appetizing highlights)), ((natural textures))"
                        )
                        components.append(effects_text)
                elif internal_theme == "interior":
                    # Select base elements
                    style = random.choice(self.interior_styles)
                    space = random.choice(self.interior_spaces)
                    element = random.choice(self.interior_elements)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"professional interior design photograph of a ((luxury {style} {space})) "
                        f"with ((premium {element})), ((masterful composition)), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice([
                            "morning", "midday", "afternoon", "golden hour",
                            "blue hour", "evening", "twilight"
                        ])
                        lighting = random.choice([
                            "natural sunlight", "soft diffused light", "dramatic window light",
                            "ambient lighting", "accent lighting", "architectural lighting",
                            "indirect lighting", "spotlighting"
                        ])
                        environment_text = (
                            f"during {time} with ((perfect {lighting})), "
                            f"((architectural details)), ((premium materials)), "
                            f"((sophisticated atmosphere))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((professional interior photography)), ((ultra sharp focus)), "
                            f"((luxury interior design)), ((perfect exposure)), "
                            f"((architectural visualization)), ((premium quality)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((volumetric light rays)), ((soft shadows)), "
                            f"((perfect reflections)), ((material textures)), "
                            f"((depth of field)), ((color harmony)), ((interior ambiance))"
                        )
                        components.append(effects_text)
                elif internal_theme == "3D":
                    # Select base elements
                    style = random.choice(self.threed_styles)
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for architectural
                        subject = random.choice(self.architecture_elements)
                        subject_text = (
                            f"{style} of {subject}, ((detailed 3D modeling)), "
                            f"((architectural visualization)), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for character
                        race = random.choice(self.races)
                        tech = random.choice(self.technology["gadgets"])
                        subject_text = (
                            f"{style} of {race} character with {tech}, "
                            f"((character modeling)), ((detailed textures)), {composition}"
                        )
                    else:  # 30% chance for sci-fi/tech
                        gadget = random.choice(self.technology["gadgets"])
                        subject_text = (
                            f"{style} of futuristic {gadget}, "
                            f"((product visualization)), ((technical details)), {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"in a ((professionally lit 3D environment)), "
                            f"((perfect studio lighting)), ((HDRI background)), "
                            f"((ambient occlusion)), ((global illumination))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((octane render)), ((ultra high poly)), "
                            f"((physically based rendering)), ((subsurface scattering)), "
                            f"((ray tracing)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((perfect reflections)), ((realistic materials)), "
                            f"((depth of field)), ((volumetric lighting)), "
                            f"((ambient occlusion)), ((perfect shadows))"
                        )
                        components.append(effects_text)
                elif internal_theme == "halloween":
                    # Select base elements
                    creature = random.choice(self.halloween_elements["creatures"])
                    prop = random.choice(self.halloween_elements["props"])
                    setting = random.choice(self.halloween_elements["settings"])
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((spooky {creature})) with ((haunted {prop})), "
                        f"((eerie atmosphere)), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice([
                            "midnight", "witching hour", "full moon night", 
                            "foggy twilight", "dark evening", "stormy night"
                        ])
                        weather = random.choice([
                            "misty", "stormy", "cloudy", "windy",
                            "thunderous", "eerily calm"
                        ])
                        environment_text = (
                            f"in a ((haunted {setting})) during {weather} {time}, "
                            f"((gothic atmosphere)), ((supernatural ambiance))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((dark fantasy)), ((horror atmosphere)), "
                            f"((dramatic lighting)), ((gothic style)), "
                            f"((haunting mood)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((ghostly mist)), ((eerie glow)), "
                            f"((dark shadows)), ((moonlight rays)), "
                            f"((supernatural effects)), ((ominous atmosphere))"
                        )
                        components.append(effects_text)
                elif internal_theme == "instagram":
                    # Select base elements
                    influencer = random.choice(self.influencer_types)
                    activity = random.choice(self.influencer_activities)
                    location = random.choice(self.influencer_locations)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"professional lifestyle photograph of {influencer} {activity}, "
                        f"((instagram aesthetic)), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice([
                            "golden hour", "sunset", "blue hour", "morning light",
                            "magic hour", "soft daylight", "dusk", "twilight"
                        ])
                        environment_text = (
                            f"at {location} during {time}, "
                            f"((lifestyle setting)), ((perfect ambiance)), "
                            f"((instagram worthy location))"
                        )  # Add closing parenthesis here
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((professional lifestyle photography)), ((social media aesthetic)), "
                            f"((influencer style)), ((perfect exposure)), "
                            f"((trendy composition)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((natural bokeh)), ((soft skin glow)), "
                            f"((perfect golden light)), ((lifestyle colors)), "
                            f"((subtle vignette)), ((instagram filter))"
                        )
                        components.append(effects_text)
                elif internal_theme == "realistic":
                    # Select base elements
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for professional portrait
                        profession = random.choice(self.professions)
                        clothing = random.choice(self.clothing["realistic"])
                        pose = random.choice([
                            "professional headshot", "environmental portrait",
                            "candid moment", "dramatic portrait", "profile portrait",
                            "three-quarter view portrait", "full body portrait"
                        ])
                        lighting = random.choice([
                            "natural window lighting", "professional studio lighting",
                            "dramatic rim lighting", "soft diffused lighting",
                            "golden hour sunlight", "dramatic chiaroscuro lighting"
                        ])
                        subject_text = (
                            f"((professional photograph)) of {profession} wearing {clothing}, "
                            f"((in {pose})), ((with {lighting})), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for wildlife/nature
                        animal = random.choice(self.animals)
                        behavior = random.choice(self.behaviors)
                        habitat = random.choice(self.habitats)
                        subject_text = (
                            f"((wildlife photograph)) of {animal} {behavior} in {habitat}, "
                            f"((national geographic style)), ((telephoto lens)), {composition}"
                        )
                    else:  # 30% chance for landscape/architecture
                        subject = random.choice([
                            f"((landscape photograph)) of {random.choice(self.habitats)}",
                            f"((architectural photograph)) of {random.choice(self.architecture_elements)}",
                            f"((macro photograph)) of {random.choice(['water droplets', 'flower petals', 'butterfly wings', 'crystal formations', 'natural patterns'])}"
                        ])
                        subject_text = f"{subject}, ((professional photography)), {composition}"
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice(self.times)
                        weather = random.choice(self.weather)
                        environment_text = (
                            f"during {time} with {weather}, "
                            f"((natural atmosphere)), ((perfect lighting conditions))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((photorealistic)), ((professional photography)), "
                            f"((sharp focus)), ((perfect exposure)), ((high detail)), "
                            f"((color accurate)), ((professional camera)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((shallow depth of field)), ((perfect bokeh)), "
                            f"((natural lighting)), ((subtle vignette)), "
                            f"((professional color grading)), ((high dynamic range))"
                        )
                        components.append(effects_text)
                elif internal_theme == "pixar":
                    # Generate Pixar-style subject
                    style = random.choice(self.pixar_styles)
                    character_trait = random.choice(self.pixar_characteristics)
                    material = random.choice(self.pixar_materials)
                    environment = random.choice(self.pixar_environments)
                    lighting = random.choice(self.pixar_lighting)
                    
                    if random.random() < 0.7:  # 70% chance for character
                        if random.random() < 0.5:  # 50% chance for existing character
                            character = random.choice(self.cartoon_characters)
                            subject_text = (
                                f"{style} of an adorable {character} with {character_trait}, "
                                f"made of {material}, in a {environment}, "
                                f"featuring {lighting}, ultra detailed 3D model, "
                                f"subsurface scattering, perfect composition"
                            )
                        else:  # 50% chance for original character
                            character_type = random.choice([
                                "cute robot", "adorable toy", "charming creature",
                                "lovable monster", "friendly animal", "sweet character",
                                "endearing helper", "magical companion", "delightful friend"
                            ])
                            subject_text = (
                                f"{style} of an original {character_type} with {character_trait}, "
                                f"made of {material}, in a {environment}, "
                                f"featuring {lighting}, ultra detailed 3D model, "
                                f"subsurface scattering, perfect composition"
                            )
                    else:  # 30% chance for scene/object
                        scene_type = random.choice([
                            "magical toy", "charming household object", "cute robot helper",
                            "adorable vehicle", "friendly kitchen appliance", "sweet desk lamp",
                            "lovable musical instrument", "delightful garden tool", "magical book",
                            "charming clock", "cute mailbox", "friendly umbrella"
                        ])
                        subject_text = (
                            f"{style} of a {scene_type} with {character_trait}, "
                            f"made of {material}, in a {environment}, "
                            f"featuring {lighting}, ultra detailed 3D model, "
                            f"subsurface scattering, perfect composition"
                        )
                    
                    style_text = (
                        f"octane render quality, perfect lighting, soft shadows, "
                        f"ambient occlusion, global illumination, 8k resolution"
                    )
                    
                    effects_text = (
                        f"with subtle depth of field, gentle color grading, "
                        f"perfect exposure, subtle film grain, gentle vignette"
                    )

                    # Add components based on inclusion flags
                    components = [subject_text]
                    if include_style == "yes":
                        components.append(style_text)
                    if include_effects == "yes":
                        components.append(effects_text)
                elif internal_theme == "binet":
                    # Determine if we're doing color or black and white
                    is_color = random.random() < 0.9  # 90% chance for color, 10% for B&W
                    
                    # Define style_prefix and color_emphasis based on color choice
                    if is_color:
                        color_scheme = random.choice(self.binet_color_schemes)  # Now using binet_color_schemes
                        style_prefix = "sophisticated portrait"
                        color_emphasis = f", {color_scheme}"
                    else:
                        style_prefix = "sophisticated black and white portrait"
                        color_emphasis = ", ((dramatic black and white)), ((extreme contrast))"
                    
                    # Select a distinguished animal
                    animal = random.choice([
                        "wolf", "fox", "lion", "tiger", "leopard", "panther", "lynx",
                        "eagle", "hawk", "falcon", "owl",
                        "deer", "horse", "elk",
                        "bear", "gorilla",
                        "raccoon", "red panda"
                    ])
                    
                    # Determine if it's a contemporary or classical theme
                    is_contemporary = random.random() < 0.3  # 30% chance for contemporary
                    
                    if is_contemporary:
                        # Use contemporary themes and elements
                        character_theme = random.choice(self.binet_contemporary_themes)
                        costume = random.choice(self.binet_sports_gear)
                        props = random.choice(self.binet_urban_elements)
                        celebration = random.choice(self.binet_celebration_elements)
                        
                        subject_text = (
                            f"anthropomorphic portrait of a distinguished {animal} as a {character_theme}, "
                            f"((wearing {costume})), "
                            f"((with {props})), "
                            f"((in {celebration})), "
                            f"((aristocratic pose)), ((noble expression)), "
                            f"((intricate fur detail)), ((dramatic studio lighting))"
                        )
                    else:
                        # Use classical themes and elements
                        character_theme = random.choice(self.binet_character_themes)
                        costume = random.choice(self.binet_costume_elements)
                        props = random.choice(self.binet_props_and_weapons)
                        clothing_type = random.choice(["luxury", "professional"])
                        specific_clothing = random.choice(self.binet_clothing[clothing_type])
                        
                        subject_text = (
                            f"anthropomorphic portrait of a distinguished {animal} as a {character_theme}, "
                            f"((wearing {costume})), ((with {props})), "
                            f"((dressed in {specific_clothing})), "
                            f"((aristocratic pose)), ((noble expression)), "
                            f"((intricate fur detail)), ((dramatic studio lighting))"
                        )
                    
                    # Add sophisticated environment elements
                    environment_text = random.choice([
                        "in an elegant portrait studio setting",
                        "against a dark dramatic backdrop",
                        "in a distinguished study with leather-bound books",
                        "in a classical portrait setting",
                        "against a sophisticated dark background",
                        "in a noble chamber with subtle details",
                        "in a vintage photography studio"
                    ])
                    
                    # Enhanced photographic style elements
                    style_text = (
                        f"{style_prefix}, ((masterful composition)), "
                        f"((professional studio lighting)), ((sharp focus)), "
                        f"((photorealistic detail)), ((cinematic framing)), "
                        f"8k resolution{color_emphasis}"
                    )
                    
                    # Specific effects for the Binet style
                    effects_text = (
                        "with ((deep shadows)), ((bright highlights)), "
                        "((dramatic atmosphere)), ((volumetric lighting)), "
                        "((perfect exposure)), ((subtle vignette))"
                    )
                    
                    # Construct the components with proper emphasis
                    components = [subject_text]
                    if include_environment == "yes":
                        components.append(environment_text)
                    if include_style == "yes":
                        components.append(style_text)
                    if include_effects == "yes":
                        components.append(effects_text)
                elif internal_theme == "vintage_anthro":
                    # Generate base anthropomorphic character
                    animal = random.choice(self.animals)
                    profession = random.choice(self.vintage_anthro_professions)
                    clothing = random.choice(self.vintage_anthro_clothing)
                    activity = random.choice(self.vintage_anthro_activities)
                    prop = random.choice(self.vintage_anthro_props)
                    setting = random.choice(self.vintage_anthro_settings)
                    
                    # Create detailed subject description with emphasis on photorealism
                    subject_text = f"hyper-realistic anthropomorphic {animal} with detailed fur texture and human-like expressions, as a {profession}"
                    action_text = f"{activity}, wearing ((highly detailed {clothing})), holding {prop}"
                    environment_text = f"in a {setting}, vintage Victorian era atmosphere, volumetric lighting"
                    style_text = "professional vintage photography, ultra-realistic textures, detailed fabric and fur rendering, studio lighting setup, sharp focus, 8k resolution, photorealistic details"
                    effects_text = "with cinematic color grading, subtle film grain, perfect exposure, volumetric lighting, detailed shadows, and period-accurate details"
                    
                    # Add components based on inclusion flags
                    components.extend([subject_text])
                    if include_action == "yes":
                        components.append(action_text)
                    if include_environment == "yes":
                        components.append(environment_text)
                    if include_style == "yes":
                        components.append(style_text)
                    if include_effects == "yes":
                        components.append(effects_text)
                elif internal_theme == "star_wars":
                    # Select base elements
                    character = random.choice(self.star_wars_characters)
                    prop = random.choice(self.star_wars_props)
                    vehicle = random.choice(self.star_wars_vehicles)
                    location = random.choice(self.star_wars_locations)
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for character-focused scene
                        subject_text = (
                            f"epic Star Wars scene of ((detailed {character})) "
                            f"wielding ((glowing {prop})), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for vehicle-focused scene
                        subject_text = (
                            f"dramatic Star Wars shot of ((detailed {vehicle})) "
                            f"with {character} visible, {composition}"
                        )
                    else:  # 30% chance for battle/action scene
                        subject_text = (
                            f"epic Star Wars battle scene with {character} "
                            f"using {prop} near a {vehicle}, {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"in ((detailed {location})), "
                            f"((Star Wars universe)), ((sci-fi atmosphere)), "
                            f"((epic scale))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((Star Wars movie quality)), ((cinematic lighting)), "
                            f"((photorealistic)), ((ILM VFX quality)), "
                            f"((epic movie scene)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effect = random.choice(self.star_wars_effects)
                        effects_text = (
                            f"with {effect}, ((lens flares)), ((volumetric lighting)), "
                            f"((dramatic shadows)), ((space atmosphere)), "
                            f"((cinematic color grading))"
                        )
                        components.append(effects_text)
                elif internal_theme == "marvel":
                    character = random.choice(self.marvel_characters)
                    comic_style = random.choice(self.marvel_comic_styles)
                    comic_effect = random.choice(self.marvel_comic_effects)
                    comic_composition = random.choice(self.marvel_comic_compositions)
                    
                    if random.random() < 0.7:  # 70% chance for action scene
                        action = random.choice([
                            "locked in epic battle", "performing heroic feat",
                            "unleashing super powers", "defending against villains",
                            "leading fellow heroes", "in dramatic confrontation"
                        ])
                        subject_text = (
                            f"((classic Marvel comic book art)) of {character} {action}, "
                            f"in {comic_style}, {comic_composition}, "
                            f"((vintage comic book illustration)), ((comic book art))"
                        )
                    else:  # 30% chance for character portrait
                        pose = random.choice([
                            "heroic comic book pose", "dramatic character moment",
                            "classic superhero stance", "iconic comic book pose",
                            "powerful hero shot", "legendary comic cover pose"
                        ])
                        subject_text = (
                            f"((classic Marvel comic book art)) of {character} in {pose}, "
                            f"in {comic_style}, {comic_composition}, "
                            f"((vintage comic book illustration)), ((comic book art))"
                        )
                    
                    # Marvel comics-specific environment handling
                    if include_environment == "yes":
                        location = random.choice(self.marvel_locations)
                        environment_text = (
                            f"in {location}, with classic comic book background, "
                            f"dramatic comic perspective"
                        )
                    
                    # Marvel comics-specific style handling
                    if include_style == "yes":
                        style_text = (
                            f"((Silver Age Marvel style)), bold comic colors, "
                            f"detailed comic book linework, dramatic comic shading, "
                            f"vintage comic book quality"
                        )
                    
                    # Marvel comics-specific effects handling
                    if include_effects == "yes":
                        effects_text = (
                            f"with {comic_effect}, bold comic inking, "
                            f"vintage comic book printing style, classic comic color palette"
                        )

                    # Add components based on inclusion flags
                    components = [subject_text]
                    if include_environment == "yes":
                        components.append(environment_text)
                    if include_style == "yes":
                        components.append(style_text)
                    if include_effects == "yes":
                        components.append(effects_text)
                elif internal_theme == "steampunk":
                    # Select base elements
                    machine = random.choice(self.steampunk_elements["machines"])
                    accessory = random.choice(self.steampunk_elements["accessories"])
                    environment = random.choice(self.steampunk_elements["environments"])
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for cityscape
                        subject_text = (
                            f"((epic steampunk cityscape)) with ((massive {machine})) and "
                            f"((intricate {accessory})), in a ((detailed {environment})), "
                            f"((Victorian industrial atmosphere)), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for street level
                        subject_text = (
                            f"((immersive steampunk street scene)) with ((detailed {machine})) and "
                            f"((ornate {accessory})), in a ((bustling {environment})), "
                            f"((Victorian era atmosphere)), {composition}"
                        )
                    else:  # 30% chance for industrial interior
                        subject_text = (
                            f"((detailed steampunk interior)) with ((complex {machine})) and "
                            f"((elaborate {accessory})), in a ((grand {environment})), "
                            f"((industrial Victorian style)), {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice([
                            "foggy morning", "industrial twilight", "gaslit evening",
                            "steam-filled dawn", "coal-smoke dusk", "brass-lit night"
                        ])
                        weather = random.choice([
                            "steam clouds", "industrial haze", "coal smoke",
                            "mechanical fog", "brass-tinted clouds", "copper sunset"
                        ])
                        environment_text = (
                            f"during {time} with {weather}, "
                            f"((Victorian industrial era)), ((steampunk atmosphere)), "
                            f"((mechanical complexity))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((steampunk aesthetic)), ((Victorian industrial)), "
                            f"((brass and copper details)), ((mechanical intricacy)), "
                            f"((ornate engineering)), ((vintage technology)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((steam effects)), ((mechanical glow)), "
                            f"((brass reflections)), ((gear mechanisms)), "
                            f"((industrial smoke)), ((copper highlights)), "
                            f"((vintage patina))"
                        )
                        components.append(effects_text)
                elif internal_theme == "post_apocalyptic":
                    # Select base elements
                    composition = random.choice(self.compositions)
                    
                    # Determine scene type
                    scene_type = random.random()
                    if scene_type < 0.4:  # 40% chance for wasteland scene
                        environment = random.choice(self.post_apocalyptic_elements["environments"])
                        prop = random.choice(self.post_apocalyptic_elements["props"])
                        atmosphere = random.choice(self.post_apocalyptic_elements["atmosphere"])
                        subject_text = (
                            f"((epic post-apocalyptic vista)) of a ((devastated {environment})) with "
                            f"((weathered {prop})), ((in {atmosphere} atmosphere)), {composition}"
                        )
                    elif scene_type < 0.7:  # 30% chance for survival scene
                        prop = random.choice([
                            "makeshift shelter", "salvaged vehicle", "improvised weapons",
                            "scavenged supplies", "survival gear", "fortified base",
                            "wasteland camp", "trading outpost", "survivor's hideout"
                        ])
                        subject_text = (
                            f"((post-apocalyptic survival scene)) with ((detailed {prop})), "
                            f"((wasteland atmosphere)), ((survival elements)), {composition}"
                        )
                    else:  # 30% chance for ruins scene
                        ruins = random.choice([
                            "abandoned skyscrapers", "collapsed highway", "ruined metropolis",
                            "decaying shopping mall", "destroyed factory", "fallen monuments",
                            "overgrown stadium", "derelict train station", "crumbling bridges"
                        ])
                        subject_text = (
                            f"((dramatic post-apocalyptic scene)) of ((decaying {ruins})), "
                            f"((signs of civilization's fall)), {composition}"
                        )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        time = random.choice([
                            "toxic dawn", "nuclear sunset", "perpetual dusk",
                            "radioactive twilight", "acid rain storm", "dusty noon",
                            "contaminated evening", "fallout night"
                        ])
                        weather = random.choice([
                            "radioactive storm", "acid rain", "toxic fog",
                            "nuclear winter", "dust storm", "chemical haze",
                            "contaminated clouds", "burning sky"
                        ])
                        environment_text = (
                            f"during {time} with {weather}, "
                            f"((post-apocalyptic atmosphere)), ((devastated landscape)), "
                            f"((signs of destruction))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((post-apocalyptic aesthetic)), ((dystopian atmosphere)), "
                            f"((weathered textures)), ((decay and destruction)), "
                            f"((survival horror)), ((cinematic scale)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((volumetric toxic fog)), ((dust particles)), "
                            f"((radiation effects)), ((environmental decay)), "
                            f"((atmospheric contamination)), ((dramatic lighting))"
                        )
                        components.append(effects_text)
                elif internal_theme == "underwater":
                    structure = random.choice(self.underwater_elements["structures"])
                    life_form = random.choice(self.underwater_elements["life_forms"])
                    tech = random.choice(self.underwater_elements["technology"])
                    culture = random.choice(self.underwater_elements["cultural_elements"])
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((epic underwater civilization)) with {structure} and "
                        f"{life_form}, featuring {tech} and {culture}, "
                        f"((ultra detailed oceanic metropolis))"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"in ((deep ocean waters)) with ((bioluminescent lighting)), "
                            f"((crystal clear water visibility)), ((schools of exotic fish))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((cinematic underwater photography)), ((perfect clarity)), "
                            f"((volumetric god rays)), ((dynamic composition)), "
                            f"((ultra sharp focus)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((water caustics)), ((bioluminescent glow)), "
                            f"((floating particles)), ((underwater atmospheric perspective)), "
                            f"((gentle water currents))"
                        )
                        components.append(effects_text)
                elif internal_theme == "microscopic":
                    structure = random.choice(self.microscopic_elements["structures"])
                    process = random.choice(self.microscopic_elements["processes"])
                    environment = random.choice(self.microscopic_elements["environments"])
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((electron microscope visualization)) of {structure} during {process}, "
                        f"((scientific detail)), ((molecular precision))"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"in a {environment}, ((microscopic scale)), "
                            f"((cellular detail)), ((quantum effects))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((scientific visualization)), ((precise detail)), "
                            f"((molecular clarity)), ((ultra sharp focus)), "
                            f"((microscopic accuracy)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((quantum effects)), ((molecular interactions)), "
                            f"((microscopic patterns)), ((cellular structures)), "
                            f"((atomic detail)), ((scientific accuracy))"
                        )
                        components.append(effects_text)
                elif internal_theme == "bio_organic":
                    structure = random.choice(self.bio_organic_elements["structures"])
                    process = random.choice(self.bio_organic_elements["processes"])
                    aesthetic = random.choice(self.bio_organic_elements["aesthetics"])
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((hybrid bio-mechanical artwork)) of {structure} performing {process}, "
                        f"((organic integration)), ((seamless fusion))"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"featuring {aesthetic}, ((living technology)), "
                            f"((organic machinery)), ((bio-digital fusion))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((organic integration)), ((seamless fusion)), "
                            f"((living technology)), ((ultra sharp focus)), "
                            f"((bio-mechanical detail)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((bioluminescent highlights)), ((organic patterns)), "
                            f"((technological elements)), ((flowing energy)), "
                            f"((living circuits)), ((pulsing mechanisms))"
                        )
                        components.append(effects_text)
                elif internal_theme == "peaky_blinders":
                    # Select core elements
                    animal = random.choice(self.peaky_blinders_animals)
                    outfit = random.choice(self.peaky_blinders_outfits)
                    accessory = random.choice(self.peaky_blinders_accessories)
                    setting = random.choice(self.peaky_blinders_settings)
                    furniture = random.choice(self.peaky_blinders_furniture)
                    atmosphere = random.choice(self.peaky_blinders_atmospheres)
                    prop = random.choice(self.peaky_blinders_props)
                    
                    # Create the main subject description
                    subject_text = (
                        f"((Anthropomorphic {animal} in 1920s Peaky Blinders style)), "
                        f"((wearing {outfit})), {accessory}, "
                        f"((ultra-detailed fur texture)),  "  # Removed "noble expression"
                        f"((masterful character design))"
                    )
                    
                    # Environment description
                    environment_text = (
                        f"in a {setting} with {furniture}, "
                        f"surrounded by {prop}, {atmosphere}"
                    )
                    
                    # Style elements
                    style_text = (
                        f"((1920s period accurate)), ((cinematic composition)), "
                        f"((masterful photography)), ((ultra-realistic)), "
                        f"((detailed textures)), 8k resolution"
                    )
                    
                    # Effects
                    effects_text = (
                        f"with ((dramatic lighting)), ((volumetric atmosphere)), "
                        f"((perfect exposure)), ((cinematic color grading)), "
                        f"((detailed shadows)), ((period-accurate details))"
                    )

                    # Add components based on inclusion flags
                    components = [subject_text]
                    if include_environment == "yes":
                        components.append(environment_text)
                    if include_style == "yes":
                        components.append(style_text)
                    if include_effects == "yes":
                        components.append(effects_text)
                elif internal_theme == "christmas":
                    # Select base elements
                    character = random.choice(self.christmas_elements["characters"])
                    setting = random.choice(self.christmas_elements["settings"])
                    decoration = random.choice(self.christmas_elements["decorations"])
                    activity = random.choice(self.christmas_elements["activities"])
                    style = random.choice(self.christmas_styles)
                    mood = random.choice(self.christmas_moods)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((magical christmas scene)) of {character} {activity} near a ((festive {decoration})), "
                        f"((christmas magic)), {composition}"
                    )
                    
                    # Initialize components with subject first
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        weather = random.choice(self.christmas_elements["weather"])
                        magical_effect = random.choice(self.christmas_elements["magical_effects"])
                        environment_text = (
                            f"in a ((magical {setting})) during {weather}, "
                            f"with ((enchanted {magical_effect})), ((festive atmosphere))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((christmas {style})), (({mood} atmosphere)), "
                            f"((festive lighting)), ((holiday magic)), "
                            f"((seasonal charm)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects if enabled
                    if include_effects == "yes":
                        food = random.choice(self.christmas_elements["foods"])
                        effects_text = (
                            f"with ((twinkling lights)), ((magical snow effects)), "
                            f"((warm glow)), ((festive decorations)), "
                            f"((holiday ambiance)), ((scent of {food})))"
                        )
                        components.append(effects_text)
                elif internal_theme == "village":
                    # Select base elements
                    village = random.choice(self.village_types)
                    architecture = random.choice(self.village_architecture)
                    cultural = random.choice(self.village_cultural_elements)
                    landscape = random.choice(self.landscape_features)
                    atmosphere = random.choice(self.landscape_atmospheres)
                    composition = random.choice(self.compositions)
                    
                    # Create detailed subject description
                    subject_text = (
                        f"((breathtaking {village})) with ((traditional {architecture})) "
                        f"and ((authentic {cultural})), {composition}"
                    )
                    
                    # Initialize components with subject
                    components = [subject_text]
                    
                    # Add environment if enabled
                    if include_environment == "yes":
                        environment_text = (
                            f"surrounded by ((majestic {landscape})) during {atmosphere}, "
                            f"((natural beauty)), ((cultural heritage)), "
                            f"((traditional lifestyle))"
                        )
                        components.append(environment_text)
                    
                    # Add style elements
                    if include_style == "yes":
                        style_text = (
                            f"((professional travel photography)), ((perfect exposure)), "
                            f"((cultural authenticity)), ((architectural details)), "
                            f"((dramatic landscape)), ((rich colors)), 8k resolution"
                        )
                        components.append(style_text)
                    
                    # Add effects
                    if include_effects == "yes":
                        effects_text = (
                            f"with ((natural lighting)), ((atmospheric depth)), "
                            f"((perfect composition)), ((rich textures)), "
                            f"((cultural details)), ((environmental harmony))"
                        )
                        components.append(effects_text)
                else:  # random theme handling
                    if random.random() < 0.7:  # 70% chance for human subject
                        profession = random.choice(self.professions)
                        clothing = random.choice(self.clothing["realistic"])
                        subject_text = f"professional photograph of {profession} wearing {clothing}"
                    else:  # 30% chance for nature/animal
                        animal = random.choice(self.animals)
                        behavior = random.choice(self.behaviors)
                        subject_text = f"professional wildlife photograph of {animal} {behavior}"
                    components.append(subject_text)

        # Action and composition
        if include_action == "yes" and internal_theme != "abstract":
            action = random.choice(self.actions)
            composition = random.choice(self.compositions)
            action_text = f"{action}, {composition}"
            components.append(action_text)

        # Environment
        if include_environment == "yes" and internal_theme != "abstract":
            if internal_theme == "fantasy":
                location = random.choice(self.mythical_locations)
                weather_cond = random.choice(self.weather)
                time = random.choice(self.times)
                environment_text = f"in a {location} during {weather_cond} {time}"
            elif internal_theme == "sci_fi":
                atmos = random.choice(self.alien_world_elements["atmospheres"])
                terrain = random.choice(self.alien_world_elements["terrains"])
                feature = random.choice(self.alien_world_elements["features"])
                environment_text = f"on an alien world with {atmos} atmosphere, {terrain}, and {feature}"
            elif internal_theme == "architecture":
                weather_cond = random.choice(self.weather)
                time = random.choice(self.times)
                environment_text = f"during {weather_cond} {time}"
            elif internal_theme == "food":
                environment_text = f"on {random.choice(['rustic wooden table', 'marble counter', 'elegant plate', 'vintage dish', 'modern platter', 'chef table', 'restaurant setting'])}"
            elif internal_theme == "interior":
                time = random.choice(self.times)
                environment_text = f"during {time} with {random.choice(['natural lighting', 'ambient lighting', 'mood lighting', 'spot lighting', 'indirect lighting'])}"
            elif internal_theme == "3D":
                environment_text = f"in {random.choice(['studio lighting setup', 'environmental lighting', 'dramatic lighting', 'realistic environment', 'abstract space', 'geometric background'])}"
            elif internal_theme == "halloween":
                setting = random.choice(self.halloween_elements["settings"])
                time = random.choice(["midnight", "witching hour", "full moon night", "foggy twilight"])
                weather = random.choice(["misty", "stormy", "cloudy", "windy"])
                environment_text = f"in a {setting} during {weather} {time}"
            elif internal_theme == "instagram":
                location = random.choice(self.influencer_locations)
                time = random.choice(["golden hour", "sunset", "blue hour", "morning light"])
                environment_text = f"at {location} during {time}"
            elif internal_theme == "christmas":
                setting = random.choice(self.christmas_elements["settings"])
                time = random.choice(["Christmas Eve", "Christmas Day", "Boxing Day", "New Year's Eve"])
                weather = random.choice(self.christmas_elements["weather"])
                environment_text = f"on {time} in a {setting}, with {random.choice(self.christmas_elements['decorations'])} and {random.choice(self.christmas_elements['activities'])}"
            else:
                habitat = random.choice(self.habitats)
                weather_cond = random.choice(self.weather)
                time = random.choice(self.times)
                environment_text = f"in a {habitat} during {weather_cond} {time}"
            components.append(environment_text)

        # Style and mood
        if include_style == "yes" and internal_theme != "abstract":
            art_style = random.choice(self.art_styles)
            emotion = random.choice(self.emotions)
            style_text = f"{art_style} with {emotion} mood"
            components.append(style_text)

        # Special effects
        if include_effects == "yes":
            if internal_theme == "abstract":
                # More abstract-specific effects
                effect1 = random.choice([
                    "intersecting", "overlapping", "radiating", "repeating",
                    "dissolving", "merging", "fragmenting", "tessellating",
                    "undulating", "oscillating", "bifurcating", "converging"
                ])
                effect2 = random.choice([
                    "forms", "shapes", "patterns", "structures",
                    "compositions", "arrangements", "configurations",
                    "constructions", "formations", "geometries"
                ])
                effects_text = f"with {effect1} {effect2}"
                components.append(effects_text)
            elif internal_theme == "strange_animal":
                # For chimera animals, use only lighting and atmosphere effects, no artifacts
                effects_text = "with natural lighting and atmospheric depth"
                # Only append if not already in components
                if effects_text not in components:
                    components.append(effects_text)
            elif internal_theme == "fantasy":
                effect = random.choice(self.magical_effects["fire"])
                artifact = random.choice(self.artifacts["weapon"])
                effects_text = f"with {effect} and {artifact}"
            elif internal_theme == "sci_fi":
                tech = random.choice(self.technology["weapons"])
                ship = random.choice(self.spacecraft["military"])
                effects_text = f"with {tech} and {ship} in background"
            elif internal_theme == "halloween":
                effect1 = random.choice([
                    "eerie glow", "ghostly mist", "dark shadows", "moonlight rays",
                    "spectral aura", "mysterious fog", "sinister atmosphere",
                    "supernatural lighting", "ominous clouds", "creepy ambiance"
                ])
                effect2 = random.choice(self.halloween_elements["props"])
                effects_text = f"with {effect1} and {effect2}"
            elif internal_theme == "instagram":
                effect = random.choice([
                    "perfect lighting", "bokeh effect", "lens flare", "natural glow",
                    "soft focus", "golden light", "backlit", "rim lighting",
                    "professional lighting", "studio lighting"
                ])
                effects_text = f"with {effect} and lifestyle aesthetic"
            elif internal_theme == "christmas":
                effect = random.choice(self.christmas_elements["magical_effects"])
                effects_text = f"with {effect} and festive {random.choice(self.christmas_elements['decorations'])}"
            else:  # realistic or mixed
                if random.choice([True, False]):
                    effect = random.choice(self.magical_effects["nature"])
                    effects_text = f"with {effect}"
                else:
                    art = random.choice(self.artifacts["jewelry"])
                    effects_text = f"with {art}"
            components.append(effects_text)  # Single append for all cases

        prompt = ", ".join(components)

        # Add enhancement
        if enhancement_level in self.enhancements[enhancement_focus]:
            enhancement = random.choice(self.enhancements[enhancement_focus][enhancement_level])
            prompt = f"{prompt}, {enhancement}"
            effects_text = f"{effects_text}, {enhancement}"

        return (prompt, subject_text, action_text, environment_text, style_text, effects_text, seed)