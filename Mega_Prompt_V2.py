import random
import os
from typing import Dict, List, Tuple, Optional

class MegaPromptV2:
    """
    Enhanced version of the Mega Prompt Generator with improved organization and features.
    """
    
    def __init__(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'Core_Nodes', 'config', 'config_mega.txt')
        
        # Load configurations from file
        self.load_config(config_path)
        
        # Initialize theme mappings
        self.theme_mappings = {
            "🎲 Dynamic Random": "random",
            "🎨 Abstract": "abstract",
            "📺 Animation Cartoon": "cartoon", 
            "🎌 Anime": "anime",
            "🏛️ Architectural": "architecture",
            "🧬 Bio-Organic Technology": "bio_organic",
            "🖼️ Binet Surreal": "binet",
            "✏️ Caricature": "caricature",
            "🦄 Chimera Animals": "strange_animal", 
            "🐰 Chimera Cute Animals": "cute_chimera",
            "🎅 Christmas": "christmas",
            "🎬 Cinema Studio": "cinema",
            "🍳 Culinary/Food": "food",
            "👗 Curvy Fashion": "curvy_girl",
            "💠 Dimension 3D": "3d",
            "✨ Enchanted Fantasy": "fantasy",
            "📸 Essential Realistic": "realistic",
            "🌆 Futuristic City Metropolis": "futuristic_city",
            "🚀 Futuristic Sci-Fi": "scifi",
            "👻 Halloween Ethereal": "halloween",
            "👙 Instagram Lifestyle": "instagram",
            "🏠 Interior Spaces": "interior",
            "🏷️ Logo": "logo",
            "📖 Manga Panel": "manga_panel",
            "🦸‍♂️ Marvel Universe": "marvel",
            "🔬 Microscopic Universe": "microscopic",
            "🎭 Peaky Blinders Style": "peaky_blinders",
            "💫 Pixar Animation": "pixar",
            "☢️ Post-Apocalyptic Wasteland": "post_apocalyptic",
            "🏫 School Manga": "school_manga",
            "🖤 Star Wars Universe": "star_wars",
            "⚙️ Steampunk Cities": "steampunk",
            "🌊 Underwater Civilization": "underwater",
            "🏘️ Village Of the World": "village",
            "🧸 Vintage Anthropomorphic": "vintage_anthro",
            "📱 Selfie": "selfie",  # Add this line
        }

    def load_config(self, config_path: str) -> None:
        """Load configurations from the specified file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_text = f.read()
                
            # Execute the config file content in a safe local namespace
            namespace = {}
            exec(config_text, {}, namespace)
            
            # Transfer all variables to class attributes
            for key, value in namespace.items():
                setattr(self, key, value)
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """Define input types for the node."""
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
                    "👗 Curvy Fashion",
                    "💠 Dimension 3D",
                    "✨ Enchanted Fantasy",
                    "📸 Essential Realistic",
                    "🌆 Futuristic City Metropolis", 
                    "🚀 Futuristic Sci-Fi",
                    "👻 Halloween Ethereal",
                    "👙 Instagram Lifestyle",   
                    "🏠 Interior Spaces",
                    "🏷️ Logo",
                    "📖 Manga Panel",
                    "🦸‍♂️ Marvel Universe",
                    "🔬 Microscopic Universe",
                    "🎭 Peaky Blinders Style",
                    "💫 Pixar Animation",
                    "☢️ Post-Apocalyptic Wasteland",
                    "🏫 School Manga",
                    "📱 Selfie",  # Add this line
                    "🖤 Star Wars Universe",
                    "⚙️ Steampunk Cities",
                    "🌊 Underwater Civilization",
                    "🏘️ Village Of the World",
                    "🧸 Vintage Anthropomorphic",
                ], {"default": "🎲 Dynamic Random"}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "include_environment": (["yes", "no"], {"default": "yes"}),
                "include_style": (["yes", "no"], {"default": "yes"}),
                "include_effects": (["yes", "no"], {"default": "yes"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "subject", "environment", "style", "effects", "seed")
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def get_theme_handler(self, theme: str) -> callable:
        """Get the appropriate theme handler function."""
        internal_theme = self.theme_mappings.get(theme, theme)
        handler_name = f"_handle_{internal_theme}_theme"
        return getattr(self, handler_name, self._handle_default_theme)

    def generate(self, theme: str, complexity: str, randomize: str, seed: int = 0, 
                custom_subject: str = "", include_environment: str = "yes", 
                include_style: str = "yes", include_effects: str = "yes") -> Tuple[str, str, str, str, str, int]:
        """
        Generate a prompt based on the given parameters.
        """
        # Handle randomization
        if randomize == "enable":
            seed = random.randint(0, 0xffffffffffffffff) if seed == 0 else seed
            random.seed(seed)

        # Get internal theme name
        internal_theme = self.theme_mappings.get(theme, theme)
        
        # If theme is random, select a random theme
        if internal_theme == "random":
            available_themes = list(self.theme_mappings.values())
            available_themes.remove("random")  # Remove random from options
            internal_theme = random.choice(available_themes)

        # Get theme handler and generate components
        handler = self.get_theme_handler(internal_theme)
        components = handler(
            custom_subject=custom_subject.strip(),
            include_environment=include_environment,
            include_style=include_style,
            include_effects=include_effects
        )

        # Extract components
        subject_text = components.get("subject", "")
        environment_text = components.get("environment", "")
        style_text = components.get("style", "")
        effects_text = components.get("effects", "")

        # Build prompt
        prompt_parts = []
        if subject_text:  # Always include subject if it exists
            prompt_parts.append(subject_text)
        if environment_text and include_environment == "yes":
            prompt_parts.append(environment_text)
        if style_text and include_style == "yes":
            prompt_parts.append(style_text)
        if effects_text and include_effects == "yes":
            prompt_parts.append(effects_text)

        # Join components and add maximum enhancements
        prompt = ", ".join(prompt_parts)
        
        # Always add maximum enhancements
        detail_enhancement = random.choice(self.enhancements["detail"]["dramatic"])
        composition_enhancement = random.choice(self.enhancements["composition"]["dramatic"])
        lighting_enhancement = random.choice(self.enhancements["lighting"]["dramatic"])
        color_enhancement = random.choice(self.enhancements["color"]["dramatic"])
        
        prompt = f"{prompt}, {detail_enhancement}, {composition_enhancement}, {lighting_enhancement}, {color_enhancement}"
        effects_text = f"{effects_text}, {detail_enhancement}, {composition_enhancement}, {lighting_enhancement}, {color_enhancement}"

        return (prompt, subject_text, environment_text, style_text, effects_text, seed)

    def _handle_default_theme(self, **kwargs) -> Dict[str, str]:
        """Default theme handler for undefined themes."""
        components = {}  # Initialize empty dictionary
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = f"professional photograph of {custom_subject}"
        else:
            if random.random() < 0.7:  # 70% chance for human subject
                profession = random.choice(self.professions)
                clothing = random.choice(self.clothing["realistic"])
                components["subject"] = f"professional photograph of {profession} wearing {clothing}"
            else:  # 30% chance for nature/animal
                animal = random.choice(self.animals)
                behavior = random.choice(self.behaviors)
                components["subject"] = f"professional wildlife photograph of {animal} {behavior}"

        if kwargs.get("include_environment") == "yes":
            habitat = random.choice(self.habitats)
            weather = random.choice(self.weather)
            time = random.choice(self.times)
            components["environment"] = f"in a {habitat} during {weather} {time}"

        if kwargs.get("include_style") == "yes":
            art_style = random.choice(self.art_styles)
            emotion = random.choice(self.emotions)
            components["style"] = f"{art_style} with {emotion} mood"

        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.magical_effects["nature"])
            components["effects"] = f"with {effect}"

        return components  # Always return the dictionary

    def _handle_abstract_theme(self, **kwargs) -> Dict[str, str]:
        """Abstract theme handler with enhanced geometric and color elements."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((abstract interpretation of {custom_subject})), "
                f"((with dynamic motion)), ((featuring {random.choice(self.color_schemes)} color scheme)), "
                f"((minimalist design)), ((geometric harmony))"
            )
        else:
            # Original abstract theme logic...
            effect1 = random.choice(self.effect1_options)
            effect2 = random.choice(self.effect2_options)
            shape = random.choice(self.geometric_shapes)
            color_scheme = random.choice(self.color_schemes)
            motion = random.choice(self.abstract_motions)
            components["subject"] = (
                f"((abstract {shape} composition)) with ((dynamic {motion})), "
                f"((featuring {color_scheme} color scheme)), "
                f"((with {effect1} {effect2})), "
                f"((minimalist design)), ((geometric harmony))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"on ((textured {random.choice(self.textures)} background)) with "
                f"((intricate {random.choice(self.patterns)} elements)), "
                f"((abstract space)), ((dimensional depth))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.abstract_styles)
            digital_technique = random.choice(self.digital_art_techniques)
            workflow = random.choice(self.digital_art_workflows)  # Using digital_art_workflows
            components["style"] = (
                f"((professional {style})), ((abstract art)), "
                f"((minimalist aesthetic)), ((geometric precision)), "
                f"((enhanced with {digital_technique})), "
                f"((using {workflow})), "
                f"((perfect composition)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            digital_effect = random.choice(self.digital_art_effects)
            components["effects"] = (
                f"with ((dynamic {random.choice(self.abstract_effects)} effect)), ((abstract patterns)), "
                f"((geometric flow)), ((minimalist elements)), "
                f"((subtle {digital_effect})), ((artistic finish))"
            )
        
        return components

    def _handle_anime_theme(self, **kwargs) -> Dict[str, str]:
        """Anime theme handler with enhanced details."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        character = custom_subject if custom_subject else random.choice(self.anime_characters)
        
        outfit = random.choice(self.anime_outfits)
        pose = random.choice(self.anime_poses)
        expression = random.choice(self.anime_expressions)
        emotion = random.choice(self.anime_emotions)
        action = random.choice(self.anime_actions)
        composition = random.choice(self.compositions)
        
        components["subject"] = (
            f"((masterful anime artwork)) of ((detailed {character})) "
            f"((wearing {outfit})), ((in {pose})), "
            f"((with {expression} expression)), ((showing {emotion})), "
            f"((ultra detailed)), ((perfect anime proportions)), "
            f"((professional quality)), {composition}"
        )
        
        if kwargs.get("include_action") == "yes":
            components["action"] = (
                f"((dynamically {action})), ((with dramatic movement)), "
                f"((fluid motion)), ((perfect timing)), ((emotional impact))"
            )

        if kwargs.get("include_environment") == "yes":
            location = random.choice(self.anime_locations)
            time = random.choice(self.times)
            weather = random.choice(self.weather)
            components["environment"] = (
                f"in ((detailed {location})) during ((atmospheric {weather} {time})), "
                f"((perfect lighting)), ((dramatic atmosphere)), "
                f"((stunning background detail)), ((masterful scene composition))"
            )

        if kwargs.get("include_style") == "yes":
            style = random.choice(self.anime_styles)
            components["style"] = (
                f"((professional {style})), ((crisp linework)), "
                f"((perfect shading)), ((vibrant colors)), "
                f"((dramatic lighting)), ((cinematic composition)), "
                f"((high production value)), ((studio quality)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.anime_effects)
            components["effects"] = (
                f"with ((masterful {effect})), ((perfect visual effects)), "
                f"((dynamic impact frames)), ((emotional particles)), "
                f"((flowing movement)), ((dramatic camera angles)), "
                f"((stunning visual polish)), ((professional finish))"
            )

        return components

    def _handle_scifi_theme(self, **kwargs) -> Dict[str, str]:
        """Enhanced Sci-fi theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        subject = custom_subject if custom_subject else random.choice(self.scifi_subjects)
        
        tech = random.choice(self.technologies)
        action = random.choice(self.scifi_actions)
        setting = random.choice(self.scifi_settings)
        atmosphere = random.choice(self.scifi_atmospheres)
        
        components["subject"] = (
            f"((ultra detailed {subject})) with ((advanced {tech})), "
            f"((futuristic design)), ((sci-fi aesthetic)), "
            f"((high-tech details)), ((cybernetic elements))"
        )
        
        if kwargs.get("include_action") == "yes":
            components["action"] = (
                f"((dynamically {action})), ((technological precision)), "
                f"((advanced movement)), ((future tech interaction))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a ((detailed {setting})) with ((dramatic {atmosphere})), "
                f"((futuristic atmosphere)), ((high-tech environment)), "
                f"((advanced technology)), ((sci-fi setting))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.scifi_styles)
            components["style"] = (
                f"((professional {style})), ((futuristic aesthetic)), "
                f"((technological precision)), ((sci-fi quality)), "
                f"((advanced rendering)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.scifi_effects)
            components["effects"] = (
                f"with ((dramatic {effect})), ((tech glow)), "
                f"((energy effects)), ((holographic elements)), "
                f"((future tech visualization)), ((advanced lighting))"
            )
        
        return components

    def _handle_logo_theme(self, **kwargs) -> Dict[str, str]:
        """Logo theme handler."""
        components = {}
        
        # Determine logo style approach
        style_approach = random.choice(["classic", "3D", "character", "artistic"])
        
        # Use custom subject if provided and not empty
        custom_subject = kwargs.get("custom_subject", "").strip()
        logo_text = custom_subject if custom_subject else "ISULION"
        
        if style_approach == "classic":
            style = random.choice(self.logo_styles)
            font = random.choice(self.logo_fonts)
            element = random.choice(self.logo_elements)
            color_scheme = random.choice(self.logo_colors)
            
            components["subject"] = (
                f"((professional {style} logo design)) with the text \"{logo_text}\", "
                f"((using {font} typography)), ((perfect letter spacing)), "
                f"((masterful font design)), ((vector quality))"
            )
            
        elif style_approach == "3D":
            style_3d = random.choice(self.logo_3d_styles)
            color_scheme = random.choice(self.logo_colors)
            
            components["subject"] = (
                f"((highly detailed {style_3d} 3D typography)) of the text \"{logo_text}\", "
                f"((volumetric letters)), ((dimensional depth)), "
                f"((perfect 3D modeling)), ((ultra-detailed materials))"
            )
            
        elif style_approach == "character":
            character = random.choice(self.logo_characters)
            decorative = random.choice(self.logo_decorative_elements)
            
            components["subject"] = (
                f"((adorable {character} mascot logo)) with the text \"{logo_text}\", "
                f"((cute character design)), ((playful typography)), "
                f"((charming illustration)), ((kawaii style))"
            )
            
        else:  # artistic
            theme = random.choice(self.logo_themes)
            decorative = random.choice(self.logo_decorative_elements)
            
            components["subject"] = (
                f"((creative {theme} logo artwork)) with the text \"{logo_text}\", "
                f"((artistic typography)), ((illustrated elements)), "
                f"((unique design)), ((hand-crafted style))"
            )

        if kwargs.get("include_environment") == "yes":
            if style_approach == "3D":
                components["environment"] = (
                    f"with ((perfect lighting setup)), ((studio environment)), "
                    f"((professional composition)), ((clean background))"
                )
            elif style_approach == "character":
                components["environment"] = (
                    f"with ((cute {decorative})), ((playful composition)), "
                    f"((charming background)), ((balanced layout))"
                )
            else:
                element = random.choice(self.logo_elements)
                components["environment"] = (
                    f"with ((clean {element})), ((perfect composition)), "
                    f"((balanced negative space)), ((professional layout))"
                )

        if kwargs.get("include_style") == "yes":
            if style_approach == "3D":
                components["style"] = (
                    f"((premium 3D rendering)), ((perfect materials)), "
                    f"((professional lighting)), ((high-end finish)), "
                    f"((commercial quality)), ((volumetric effects)), "
                    f"((brand identity)), 8k resolution"
                )
            elif style_approach == "character":
                components["style"] = (
                    f"((kawaii aesthetic)), ((cute color palette)), "
                    f"((playful design)), ((perfect proportions)), "
                    f"((charming style)), ((mascot branding)), "
                    f"((brand identity)), 8k resolution"
                )
            else:
                color_scheme = random.choice(self.logo_colors)
                components["style"] = (
                    f"((premium {color_scheme} palette)), ((vector art)), "
                    f"((professional design)), ((perfect proportions)), "
                    f"((commercial quality)), ((scalable graphics)), "
                    f"((brand identity)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            if style_approach == "3D":
                effect = random.choice(self.logo_3d_effects)
                components["effects"] = (
                    f"with (({effect})), ((perfect shadows)), "
                    f"((realistic materials)), ((professional rendering)), "
                    f"((3D effects)), ((depth and volume))"
                )
            elif style_approach == "character":
                effect = random.choice(self.logo_character_effects)
                components["effects"] = (
                    f"with (({effect})), ((sweet details)), "
                    f"((playful elements)), ((charming finish)), "
                    f"((mascot personality)), ((cute aesthetics))"
                )
            else:
                effect = random.choice(self.logo_effects)
                components["effects"] = (
                    f"with (({effect})), ((clean edges)), "
                    f"((perfect symmetry)), ((professional finish)), "
                    f"((brand consistency)), ((timeless design))"
            )

        return components

    def _handle_caricature_theme(self, **kwargs) -> Dict[str, str]:
        """Caricature theme handler."""
        components = {}
        
        # Use custom subject if provided and not empty
        custom_subject = kwargs.get("custom_subject", "").strip()
        subject = custom_subject if custom_subject else "Donald Trump"
        
        style = random.choice(self.caricature_styles)
        features = random.choice(self.caricature_features)
        expression = random.choice(self.caricature_expressions)
        elements = random.choice(self.caricature_elements)
        setting = random.choice(self.caricature_settings)
        
        components["subject"] = (
            f"((highly exaggerated cartoon caricature)) of {subject}, "
            f"with ((extremely {features})), "
            f"((showing a {expression})), "
            f"((cartoon-style exaggeration)), "
            f"((comic book distortion)), "
            f"((animated caricature style))"
        )
        
        if kwargs.get("include_environment") == "yes":
            elements = random.choice(self.caricature_elements)
            setting = random.choice(self.caricature_settings)
            weather = random.choice(self.weather)
            time = random.choice(self.times)
            components["environment"] = (
                f"in a ((detailed {setting})) during {weather} {time}, "
                f"with ((meaningful {elements})), ((caricature composition)), "
                f"((artistic atmosphere)), ((contextual details)))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((cartoon caricature style)), ((extreme exaggeration)), "
                f"((comic book interpretation)), ((animated style)), "
                f"((cartoon artwork)), ((exaggerated features)), "
                f"((non-realistic style)), ((cartoon distortion)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with {random.choice(self.cartoon_effects)}, ((cartoon effects)), "
                f"((animated style)), ((comic book shading)), "
                f"((exaggerated proportions)), ((cartoon physics)), "
                f"((non-photorealistic rendering)), ((cartoon coloring)), "
                f"(({random.choice(self.personality_emphasis)})), ((distinctive style))"
            )

        return components

    def _handle_futuristic_city_theme(self, **kwargs) -> Dict[str, str]:
        """Futuristic city theme handler."""
        components = {}
        
        # Select base elements first
        composition = random.choice(self.compositions)
        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((futuristic cityscape)) featuring {custom_subject}, "
                f"((with advanced technology)), ((sci-fi architecture)), "
                f"((cyberpunk elements)), ((ultra modern design)), "
                f"((in {atmosphere} atmosphere)), {composition}"
            )
        else:
            components["subject"] = (
                f"((futuristic metropolis)) with "
                f"((towering architecture)) and ((advanced infrastructure)), "
                f"((in {atmosphere} atmosphere)), {composition}"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.futuristic_city_elements["time"])
            components["environment"] = (
                f"during {time}, ((with {atmosphere} atmosphere)), "
                f"((advanced technology)), ((cyberpunk elements)), "
                f"((futuristic urban landscape))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((ultra detailed cityscape)), ((sci-fi aesthetic)), "
                f"((futuristic architecture)), ((advanced technology)), "
                f"((cinematic scale)), ((urban complexity)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((neon lighting)), ((holographic displays)), "
                f"((volumetric fog)), ((light rays)), ((energy effects)), "
                f"((reflective surfaces)), ((atmospheric perspective))"
            )
        
        return components

    def _handle_strange_animal_theme(self, **kwargs) -> Dict[str, str]:
        """Strange animal (chimera) theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"a complex raw photograph of an intricated chimerical fantastical creature based on {custom_subject}, "
                f"bokeh background, cinematic lighting, shallow depth of field, "
                f"35mm wide angle lens, sharp focus, cinematic film still, "
                f"dynamic angle, Photography, 8k, masterfully detailed"
            )
        else:
            # Original strange animal logic...
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
            
            # Fallback if no valid combination found
            if head is None or body is None:
                head = "Lion"
                body = "Eagle"
            
            components["subject"] = (
                f"a complex raw photograph of an intricated chimerical fantastical creature with "
                f"((the body of a {body})) and ((the head of a {head})), "
                f"bokeh background, cinematic lighting, shallow depth of field, "
                f"35mm wide angle lens, sharp focus, cinematic film still, "
                f"dynamic angle, Photography, 8k, masterfully detailed"
            )
        
        if kwargs.get("include_environment") == "yes":
            habitat = random.choice(self.habitats)
            weather = random.choice(self.weather)
            time = random.choice(self.times)
            components["environment"] = (
                f"in a ((detailed {habitat})) during {weather} {time}, "
                f"((natural atmosphere)), ((perfect lighting conditions))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((photorealistic)), ((professional photography)), "
                f"((sharp focus)), ((perfect exposure)), ((high detail)), "
                f"((color accurate)), ((professional camera)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((natural lighting)), ((atmospheric depth)), "
                f"((perfect composition)), ((rich textures)), "
                f"((environmental harmony))"
            )
        
        return components

    def _handle_fantasy_theme(self, **kwargs) -> Dict[str, str]:
        """Fantasy theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"epic fantasy scene of {custom_subject}, "
                f"((in magical setting)), ((fantasy atmosphere)), "
                f"((mystical elements)), ((enchanted scene))"
            )
        else:
            # Original fantasy theme logic...
            race = random.choice(self.races)
            profession = random.choice(self.professions)
            composition = random.choice(self.compositions)
            
            # Rest of the existing logic...
            scene_type = random.random()
            if scene_type < 0.4:  # 40% chance for warrior/combat scene
                weapon = random.choice(self.artifacts["weapon"])
                armor = random.choice(self.artifacts["armor"])
                magic = random.choice(self.magical_effects["arcane"])
                components["subject"] = (
                    f"epic fantasy scene of a {race} {profession} "
                    f"wielding ((legendary {weapon})), wearing ((enchanted {armor})), "
                    f"channeling {magic}, {composition}"
                )
            elif scene_type < 0.7:  # 30% chance for magical/mystical scene
                jewelry = random.choice(self.artifacts["jewelry"])
                magic_nature = random.choice(self.magical_effects["nature"])
                magic_fire = random.choice(self.magical_effects["fire"])
                components["subject"] = (
                    f"mystical portrait of a {race} {profession} "
                    f"wearing ((magical {jewelry})), conjuring {magic_nature} "
                    f"and {magic_fire}, {composition}"
                )
            else:  # 30% chance for exploration/adventure scene
                armor = random.choice(self.artifacts["armor"])
                magic_ice = random.choice(self.magical_effects["ice"])
                components["subject"] = (
                    f"fantasy adventure scene of a {race} {profession} "
                    f"wearing ((mystical {armor})), surrounded by {magic_ice}, "
                    f"{composition}"
                )
            
            if kwargs.get("include_environment") == "yes":
                location = random.choice(self.mythical_locations)
                weather = random.choice(self.weather)
                time = random.choice(self.times)
                magic_lightning = random.choice(self.magical_effects["lightning"])
                components["environment"] = (
                    f"in a ((magical {location})) during {weather} {time}, "
                    f"with {magic_lightning} in the sky, "
                    f"((fantasy atmosphere)), ((mythical realm)))"
                )
            
            if kwargs.get("include_style") == "yes":
                components["style"] = (
                    f"((epic fantasy art)), ((magical atmosphere)), "
                    f"((detailed fantasy illustration)), ((dramatic lighting)), "
                    f"((mythical quality)), 8k resolution"
                )
            
            if kwargs.get("include_effects") == "yes":
                magic_arcane = random.choice(self.magical_effects["arcane"])
                components["effects"] = (
                    f"with {magic_arcane}, ((magical particles)), "
                    f"((glowing runes)), ((ethereal atmosphere)), "
                    f"((mystical energy)), ((fantasy effects))"
                )
        
        return components

    def _handle_cartoon_theme(self, **kwargs) -> Dict[str, str]:
        """Cartoon theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((professional cartoon artwork)) of {custom_subject}, "
                f"((animated style)), ((cartoon character design)), "
                f"((expressive animation))"
            )
        else:
            character = random.choice(self.cartoon_characters)
            effect = random.choice(self.cartoon_effects)
            action = random.choice(self.cinema_actions)
            
            components["subject"] = (
                f"((professional cartoon artwork)) of {character}, "
                f"((animated style)), ((cartoon character design)), "
                f"((expressive animation))"
            )
        
        if kwargs.get("include_environment") == "yes":
            cartoon_environment = random.choice([
                "cartoon world", "animated landscape", "classic cartoon background",
                "wacky environment", "cartoon city", "animated forest",
                "cartoon household", "silly cartoon setting", "animated playground",
                "cartoon wonderland"
            ])
            components["environment"] = (
                f"in a ((detailed {cartoon_environment})), "
                f"((cartoon world)), ((animated atmosphere))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional animation style)), ((cartoon art)), "
                f"((dynamic composition)), ((expressive animation)), "
                f"((perfect character design)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.cartoon_effects)
            components["effects"] = (
                f"with (({effect})), ((animation effects)), "
                f"((cartoon physics)), ((dynamic movement)), "
                f"((expressive animation))"
            )
        
        return components

    def _handle_cute_chimera_theme(self, **kwargs) -> Dict[str, str]:
        """Enhanced cute chimera theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((adorable kawaii creature)) inspired by {custom_subject}, "
                f"((ultra cute features)), ((super fluffy fur)), "
                f"((big sparkly eyes)), ((tiny paws)), ((sweet expression)), "
                f"((chibi style)), ((kawaii proportions))"
            )
        else:
            # Original cute chimera logic...
            head = random.choice(self.cute_animals)
            body = random.choice(self.cute_animals)
            while head == body:  # Ensure different animals for head and body
                body = random.choice(self.cute_animals)
            
            components["subject"] = (
                f"((adorable kawaii creature)) with ((the fluffy body of a {body})) "
                f"and ((the cute head of a {head})), ((ultra cute features)), "
                f"((super fluffy fur)), ((big sparkly eyes)), ((tiny paws)), "
                f"((sweet expression)), ((chibi style)), ((kawaii proportions))"
            )
        
        if kwargs.get("include_action") == "yes":
            action = random.choice(self.cute_chimera_actions)
            components["action"] = (
                f"((kawaii {action})), ((adorable movement)), "
                f"((sweet animation)), ((playful pose)), "
                f"((cute character animation))"
            )
        
        if kwargs.get("include_environment") == "yes":
            habitat = random.choice(self.cute_chimera_habitats)
            weather = random.choice(self.cute_chimera_weather)
            components["environment"] = (
                f"in a ((magical {habitat})) during ((enchanted {weather})), "
                f"((with sparkles and magic)), ((pastel colors)), "
                f"((soft lighting)), ((kawaii atmosphere)), "
                f"((dreamy background)), ((magical elements))"
            )
        
        if kwargs.get("include_style") == "yes":
            art_style = random.choice(self.cute_chimera_art_styles)
            emotion = random.choice(self.cute_chimera_emotions)
            components["style"] = (
                f"((kawaii {art_style})) with (({emotion} mood)), "
                f"((soft shading)), ((pastel colors)), "
                f"((cute details)), ((adorable design)), "
                f"((perfect kawaii proportions)), ((chibi aesthetic)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((magical sparkles)), ((soft pastel glow)), "
                f"((floating hearts)), ((twinkling stars)), "
                f"((rainbow highlights)), ((cute bubbles)), "
                f"((fluffy texture)), ((kawaii effects)), "
                f"((dreamy atmosphere)), ((adorable finish)))"
            )
        
        return components

    def _handle_cinema_theme(self, **kwargs) -> Dict[str, str]:
        """Cinema theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((cinematic scene)) of {custom_subject}, "
                f"((movie quality)), ((professional cinematography)), "
                f"((dramatic framing)), ((photorealistic))"
            )
        else:
            # Original cinema theme logic...
            character = random.choice(self.cinema_characters)
            composition = random.choice(self.compositions)
            action = random.choice(self.cinema_specific_actions)
            
            components["subject"] = (
                f"((cinematic scene)) of {character} {action}, "
                f"((movie quality)), ((professional cinematography)), "
                f"((dramatic framing)), ((photorealistic)), {composition}"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.times)
            weather = random.choice(self.weather)
            habitat = random.choice(self.habitats)
            components["environment"] = f"in {habitat} during {weather} {time}"
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.cinema_styles)  # Using config list
            components["style"] = (
                f"(({style})), ((professional cinematography)), "
                f"((dramatic framing)), ((photorealistic)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.cinema_effects)  # Using config list
            components["effects"] = (
                f"with (({effect})), ((atmospheric haze)), "
                f"((volumetric lighting)), ((dramatic shadows)), "
                f"((depth of field)), ((film grain))"
            )
        
        return components

    def _handle_architecture_theme(self, **kwargs) -> Dict[str, str]:
        """Architecture theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((architectural photography)) of {custom_subject}, "
                f"((masterful composition)), ((architectural detail)), "
                f"((professional quality))"
            )
        else:
            # Original architecture theme logic
            style = random.choice(self.architecture_styles)
            element = random.choice(self.architecture_elements)
            composition = random.choice(self.compositions)
            components["subject"] = (
                f"((architectural photography)) of ((detailed {style} {element})), "
                f"((masterful composition)), {composition}"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.times)
            weather = random.choice(self.weather)
            components["environment"] = (
                f"during {time} with {weather}, "
                f"((perfect natural lighting)), ((architectural details)), "
                f"((premium materials)), ((dramatic perspective))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional architectural photography)), ((ultra sharp focus)), "
                f"((perfect exposure)), ((dramatic angles)), "
                f"((architectural visualization)), ((premium quality)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((volumetric lighting)), ((perfect shadows)), "
                f"((detailed textures)), ((reflective surfaces)), "
                f"((architectural materials)), ((precise geometry))"
            )
        
        return components

    def _handle_food_theme(self, **kwargs) -> Dict[str, str]:
        """Food theme handler with enhanced settings."""
        components = {}
        
        # Use custom subject if provided, otherwise select random food type
        custom_subject = kwargs.get("custom_subject", "").strip()
        food = custom_subject if custom_subject else random.choice(self.food_types)
        
        style = random.choice(self.food_styles)
        setting = random.choice(self.food_settings)
        
        components["subject"] = (
            f"professional food photograph of {style} {food}, "
            f"((mouth-watering details)), ((perfect composition))"
        )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"on {setting}, ((perfect composition)), "
                f"((professional food styling)), ((studio lighting))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional food photography)), ((ultra sharp focus)), "
                f"((commercial quality)), ((perfect exposure)), "
                f"((culinary photography)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((soft depth of field)), ((perfect color balance)), "
                f"((steam effects)), ((fresh ingredients)), "
                f"((appetizing highlights)), ((natural textures))"
            )
        
        return components

    def _handle_interior_theme(self, **kwargs) -> Dict[str, str]:
        """Interior theme handler with enhanced lighting."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"professional interior design photograph of {custom_subject}, "
                f"((luxury interior)), ((masterful composition)), "
                f"((architectural detail)), ((premium quality))"
            )
        else:
            # Original interior theme logic...
            style = random.choice(self.interior_styles)
            space = random.choice(self.interior_spaces)
            element = random.choice(self.interior_elements)
            
            components["subject"] = (
                f"professional interior design photograph of a ((luxury {style} {space})) "
                f"with ((premium {element})), ((masterful composition))"
            )
        
        if kwargs.get("include_environment") == "yes":
            # Define time and lighting before using them
            time = random.choice(self.interior_times)
            lighting = random.choice(self.interior_lighting)
            components["environment"] = (
                f"during {time} with ((perfect {lighting})), "
                f"((luxury interior design)), ((perfect exposure)), "
                f"((architectural visualization)), ((premium quality))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional interior photography)), ((ultra sharp focus)), "
                f"((luxury interior design)), ((perfect exposure)), "
                f"((architectural visualization)), ((premium quality)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((volumetric light rays)), ((soft shadows)), "
                f"((perfect reflections)), ((material textures)), "
                f"((depth of field)), ((color harmony)), ((interior ambiance))"
            )
        
        return components

    def _handle_3d_theme(self, **kwargs) -> Dict[str, str]:
        """Enhanced 3D theme handler."""
        components = {}
        
        # Select base elements
        style = random.choice(self.threed_styles)
        material = random.choice(self.threed_materials)
        effect = random.choice(self.threed_effects)
        composition = random.choice(self.compositions)
        
        components["subject"] = (
            f"((professional 3D {style})), ((ultra-detailed {material} materials)), "
            f"((perfect 3D modeling)), ((ultra-detailed geometry)), "
            f"((volumetric detail)), ((3D masterpiece)), {composition}"
        )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a ((professionally lit 3D environment)), "
                f"((perfect studio lighting)), ((HDRI background)), "
                f"((ambient occlusion)), ((global illumination)), "
                f"((perfect shadows)), ((depth of field))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((octane render)), ((ultra high poly)), "
                f"((physically based rendering)), ((subsurface scattering)), "
                f"((ray tracing)), ((perfect materials)), "
                f"((professional 3D quality)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with (({effect})), ((perfect reflections)), "
                f"((realistic materials)), ((depth of field)), "
                f"((volumetric lighting)), ((ambient occlusion)), "
                f"((perfect shadows)), ((3D post-processing))"
            )
        
        return components

    def _handle_halloween_theme(self, **kwargs) -> Dict[str, str]:
        """Halloween theme handler with enhanced effects."""
        components = {}
        
        # Select base elements
        creature = random.choice(self.halloween_elements["creatures"])
        prop = random.choice(self.halloween_elements["props"])
        setting = random.choice(self.halloween_elements["settings"])
        time = random.choice(self.halloween_times)
        weather = random.choice(self.halloween_weather)
        effect = random.choice(self.halloween_effects)  # Using new halloween_effects
        
        components["subject"] = (
            f"((spooky {creature})) with ((haunted {prop})), "
            f"((eerie atmosphere)), ((halloween theme)), "
            f"((with {effect}))"  # Added halloween effect
        )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a ((haunted {setting})) during {weather} {time}, "
                f"((gothic atmosphere)), ((supernatural ambiance))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((dark fantasy)), ((horror atmosphere)), "
                f"((dramatic lighting)), ((gothic style)), "
                f"((haunting mood)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((ghostly mist)), ((eerie glow)), "
                f"((dark shadows)), ((moonlight rays)), "
                f"((supernatural effects)), ((ominous atmosphere))"
            )
        
        return components

    def _handle_instagram_theme(self, **kwargs) -> Dict[str, str]:
        """Instagram theme handler with enhanced lighting effects."""
        components = {}
        
        # Select base elements
        influencer = random.choice(self.influencer_types)
        activity = random.choice(self.influencer_activities)
        location = random.choice(self.influencer_locations)
        lighting_effect = random.choice(self.instagram_lighting_effects)  # Using new lighting effects
        
        components["subject"] = (
            f"professional lifestyle photograph of {influencer} {activity}, "
            f"((with {lighting_effect})), "  # Added lighting effect
            f"((instagram aesthetic)), ((social media style))"
        )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.instagram_times)
            components["environment"] = (
                f"at {location} during {time}, "
                f"((lifestyle setting)), ((perfect ambiance)), "
                f"((instagram worthy location)), ((premium environment)), "
                f"((social media backdrop)), ((influencer location))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional lifestyle photography)), ((social media aesthetic)), "
                f"((influencer style)), ((perfect exposure)), ((trendy composition)), "
                f"((premium quality)), ((fashion forward)), ((lifestyle brand)), "
                f"((editorial quality)), ((commercial grade)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.instagram_lighting_effects)
            components["effects"] = (
                f"with ((natural bokeh)), ((soft skin glow)), "
                f"((perfect {effect})), ((lifestyle colors)), "
                f"((subtle {effect})), ((instagram filter)), "
                f"((professional retouching)), ((perfect color grading)), "
                f"((social media finish)), ((influencer aesthetic))"
            )
        
        return components

    def _handle_marvel_theme(self, **kwargs) -> Dict[str, str]:
        """Marvel theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        character = custom_subject if custom_subject else random.choice(self.marvel_characters)
        
        if random.random() < 0.7:  # 70% chance for action scene
            action = random.choice(self.marvel_action_scenes)
            components["subject"] = (
                f"((classic Marvel comic book art)) of {character} {action}, "
                f"((vintage comic book illustration)), ((comic book art))"
            )
        else:  # 30% chance for character portrait
            pose = random.choice(self.marvel_poses)
            components["subject"] = (
                f"((classic Marvel comic book art)) of {character} in {pose}, "
                f"((vintage comic book illustration)), ((comic book art))"
            )
        
        if kwargs.get("include_environment") == "yes":
            location = random.choice(self.marvel_locations)
            components["environment"] = (
                f"in {location}, with classic comic book background, "
                f"dramatic comic perspective"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((Silver Age Marvel style)), bold comic colors, "
                f"detailed comic book linework, dramatic comic shading, "
                f"vintage comic book quality"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with {random.choice(self.marvel_comic_effects)}, bold comic inking, "
                f"vintage comic book printing style, classic comic color palette"
            )
        
        return components

    def _handle_microscopic_theme(self, **kwargs) -> Dict[str, str]:
        """Microscopic theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((electron microscope visualization)) of {custom_subject}, "
                f"((scientific detail)), ((molecular precision))"
            )
        else:
            structure = random.choice(self.microscopic_elements["structures"])
            process = random.choice(self.microscopic_elements["processes"])
            components["subject"] = (
                f"((electron microscope visualization)) of {structure} during {process}, "
                f"((scientific detail)), ((molecular precision))"
            )
        
        if kwargs.get("include_environment") == "yes":
            # Select environment separately for environment section
            microscopic_environment = random.choice(self.microscopic_elements["environments"])
            components["environment"] = (
                f"in a {microscopic_environment}, ((microscopic scale)), "
                f"((cellular detail)), ((quantum effects))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((scientific visualization)), ((precise detail)), "
                f"((molecular clarity)), ((ultra sharp focus)), "
                f"((microscopic accuracy)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((quantum effects)), ((molecular interactions)), "
                f"((microscopic patterns)), ((cellular structures)), "
                f"((atomic detail)), ((scientific accuracy))"
            )
        
        return components  # Always return the dictionary

    def _handle_peaky_blinders_theme(self, **kwargs) -> Dict[str, str]:
        """Peaky Blinders theme handler."""
        components = {}
        
        # Select common elements needed for both paths
        setting = random.choice(self.peaky_blinders_settings)
        furniture = random.choice(self.peaky_blinders_furniture)
        prop = random.choice(self.peaky_blinders_props)
        atmosphere = random.choice(self.peaky_blinders_atmospheres)
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((Anthropomorphic character in 1920s Peaky Blinders style)) of {custom_subject}, "
                f"((ultra-detailed texture)), ((masterful character design)), "
                f"((period-accurate styling))"
            )
        else:
            animal = random.choice(self.peaky_blinders_animals)
            outfit = random.choice(self.peaky_blinders_outfits)
            accessory = random.choice(self.peaky_blinders_accessories)
            
            components["subject"] = (
                f"((Anthropomorphic {animal} in 1920s Peaky Blinders style)), "
                f"((wearing {outfit})), ((stylish {accessory})), "
                f"((ultra-detailed fur texture)), "
                f"((masterful character design))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a {setting} with {furniture}, "
                f"surrounded by {prop}, {atmosphere}"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((1920s period accurate)), ((cinematic composition)), "
                f"((masterful photography)), ((ultra-realistic)), "
                f"((detailed textures)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((dramatic lighting)), ((volumetric atmosphere)), "
                f"((perfect exposure)), ((cinematic color grading)), "
                f"((detailed shadows)), ((period-accurate details))"
            )
        
        return components

    def _handle_pixar_theme(self, **kwargs) -> Dict[str, str]:
        """Pixar theme handler with enhanced storytelling elements."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base elements
        style = random.choice(self.pixar_styles)
        character_trait = random.choice(self.pixar_characteristics)
        
        if custom_subject:
            components["subject"] = (
                f"{style} of {custom_subject}, "
                f"with {character_trait}, "
                f"((ultra detailed 3D model)), ((Pixar animation style)), "
                f"((charming character design)), ((appealing features))"
            )
        else:
            # Generate a character-based subject
            if random.random() < 0.7:  # 70% chance for character
                if random.random() < 0.5:
                    character = random.choice(self.cartoon_characters)
                    components["subject"] = (
                        f"{style} of an adorable {character}, "
                        f"with {character_trait}, "
                        f"((ultra detailed 3D model)), ((Pixar animation style)), "
                        f"((charming character design)), ((appealing features))"
                    )
                else:
                    character_type = random.choice([
                        "cute robot", "adorable toy", "charming creature",
                        "lovable monster", "friendly animal", "sweet character"
                    ])
                    components["subject"] = (
                        f"{style} of an original {character_type}, "
                        f"with {character_trait}, "
                        f"((ultra detailed 3D model)), ((Pixar animation style)), "
                        f"((charming character design)), ((appealing features))"
                    )
            else:  # 30% chance for non-character scene
                scene_type = random.choice([
                    "magical toy store", "whimsical bedroom", "colorful playground",
                    "charming kitchen", "cozy living room", "enchanted workshop",
                    "friendly neighborhood", "bustling city street", "peaceful park",
                    "adventurous backyard", "mysterious attic", "magical school"
                ])
                components["subject"] = (
                    f"{style} of a charming {scene_type}, "
                    f"with {character_trait}, "
                    f"((ultra detailed 3D model)), ((Pixar animation style)), "
                    f"((magical atmosphere)), ((appealing environment))"
                )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a ((charming environment)), ((magical atmosphere)), "
                f"((colorful setting)), ((playful scene)), "
                f"((perfect lighting)), ((detailed background))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((Pixar animation style)), ((3D rendering)), "
                f"((charming design)), ((appealing aesthetic)), "
                f"((perfect lighting)), ((high detail)), "
                f"((professional 3D)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((subsurface scattering)), ((ambient occlusion)), "
                f"((volumetric lighting)), ((soft shadows)), "
                f"((perfect reflections)), ((subtle depth of field)), "
                f"((color grading)), ((cinematic effects))"
            )
        
        return components

    def _handle_post_apocalyptic_theme(self, **kwargs) -> Dict[str, str]:
        """Post-apocalyptic theme handler."""
        components = {}
        composition = random.choice(self.compositions)
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Determine scene type
        if custom_subject:
            components["subject"] = (
                f"((post-apocalyptic scene)) of {custom_subject} in "
                f"((wasteland atmosphere)), ((survival elements)), "
                f"((dramatic lighting)), {composition}"
            )
        else:
            scene_type = random.random()
            if scene_type < 0.4:  # 40% chance for wasteland scene
                environment = random.choice(self.post_apocalyptic_elements["environments"])
                prop = random.choice(self.post_apocalyptic_props)
                atmosphere = random.choice(self.post_apocalyptic_elements["atmosphere"])
                components["subject"] = (
                    f"((epic post-apocalyptic vista)) of a ((devastated {environment})) with "
                    f"((weathered {prop})), ((in {atmosphere} atmosphere)), {composition}"
                )
            elif scene_type < 0.7:  # 30% chance for survival scene
                prop = random.choice(self.post_apocalyptic_props)
                components["subject"] = (
                    f"((post-apocalyptic survival scene)) with ((detailed {prop})), "
                    f"((wasteland atmosphere)), ((survival elements)), {composition}"
                )
            else:  # 30% chance for ruins scene
                ruins = random.choice(self.post_apocalyptic_ruins)
                components["subject"] = (
                    f"((dramatic post-apocalyptic scene)) of ((decaying {ruins})), "
                    f"((signs of civilization's fall)), {composition}"
                )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.post_apocalyptic_times)
            weather = random.choice(self.post_apocalyptic_weather)
            components["environment"] = (
                f"during {time} with {weather}, "
                f"((post-apocalyptic atmosphere)), ((devastated landscape)), "
                f"((signs of destruction))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((post-apocalyptic aesthetic)), ((dystopian atmosphere)), "
                f"((weathered textures)), ((decay and destruction)), "
                f"((survival horror)), ((cinematic scale)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((volumetric toxic fog)), ((dust particles)), "
                f"((radiation effects)), ((environmental decay)), "
                f"((atmospheric contamination)), ((dramatic lighting))"
            )
        
        return components

    def _handle_school_manga_theme(self, **kwargs) -> Dict[str, str]:
        """School manga theme handler."""
        components = {}
        
        # Select base elements
        character = random.choice(self.school_manga_characters)
        uniform = random.choice(self.school_manga_uniforms)
        accessory = random.choice(self.school_manga_accessories)
        linework = random.choice(self.school_manga_linework)
        shading = random.choice(self.school_manga_shading)
        
        components["subject"] = (
            f"((professional black and white manga illustration)) of a {character}, "
            f"wearing ((technically detailed {uniform})), with ((masterfully rendered {accessory})), "
            f"((perfect manga linework)), ((professional ink technique)), "
            f"((high contrast black and white rendering)), ((clean technical execution))"
        )
        
        if kwargs.get("include_environment") == "yes":
            location = random.choice(self.school_manga_locations)
            components["environment"] = (
                f"in a ((technically rendered {location})) with ((precise architectural linework)), "
                f"((perfect perspective control)), ((clean background separation)), "
                f"((professional environmental detail)), ((masterful spatial depth)), "
                f"((sharp background contrast))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional manga technique)), ((masterful ink application)), "
                f"((perfect hatching control)), (({linework})), (({shading})), "
                f"((technical black and white mastery)), ((clean line confidence)), "
                f"((sharp value contrast)), ((professional manga artwork)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((precise line weight control)), ((perfect shadow definition)), "
                f"((masterful cross-hatching technique)), ((clean edge separation)), "
                f"((professional black and white contrast)), ((technical precision)), "
                f"((sharp detail rendering)), ((clear tonal hierarchy))"
            )
        
        return components

    def _handle_star_wars_theme(self, **kwargs) -> Dict[str, str]:
        """Star Wars theme handler."""
        components = {}
        
        # Select common elements needed for both paths
        location = random.choice(self.star_wars_locations)  # Added this line
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((epic Star Wars universe scene)) of {custom_subject}, "
                f"((Star Wars aesthetic)), ((cinematic quality)), "
                f"((epic scale)), ((movie quality))"
            )
        else:
            # Determine scene type
            scene_type = random.random()
            if scene_type < 0.4:  # 40% chance for character-focused scene
                character = random.choice(self.star_wars_characters)
                prop = random.choice(self.star_wars_props)
                components["subject"] = (
                    f"((epic Star Wars cinematic scene)) of ((highly detailed {character})) "
                    f"wielding ((glowing {prop})), ((dramatic pose)), ((epic scale)), "
                    f"((Star Wars universe)), ((movie quality))"
                )
            elif scene_type < 0.7:  # 30% chance for vehicle-focused scene
                vehicle = random.choice(self.star_wars_vehicles)
                character = random.choice(self.star_wars_characters)
                components["subject"] = (
                    f"((dramatic Star Wars shot)) of ((highly detailed {vehicle})) "
                    f"with ((detailed {character})) visible, ((epic space battle scene)), "
                    f"((Star Wars universe)), ((cinematic quality))"
                )
            else:  # 30% chance for battle/action scene
                character = random.choice(self.star_wars_characters)
                prop = random.choice(self.star_wars_props)
                vehicle = random.choice(self.star_wars_vehicles)
                components["subject"] = (
                    f"((epic Star Wars battle scene)) with ((detailed {character})) "
                    f"using ((powerful {prop})) near ((massive {vehicle})), "
                    f"((intense action)), ((Star Wars universe))"
                )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in ((detailed {location})), ((Star Wars atmosphere)), "
                f"((epic sci-fi environment)), ((massive scale)), "
                f"((otherworldly vista)), ((space fantasy setting)), "
                f"((dramatic lighting)), ((cinematic environment))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((Star Wars movie quality)), ((ILM VFX style)), "
                f"((cinematic lighting)), ((photorealistic detail)), "
                f"((professional cinematography)), ((epic movie scene)), "
                f"((high production value)), ((dramatic composition)), "
                f"((professional color grading)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.star_wars_effects)
            components["effects"] = (
                f"with ((dramatic {effect})), ((lens flares)), "
                f"((volumetric lighting)), ((dynamic shadows)), "
                f"((space atmosphere)), ((energy effects)), "
                f"((cinematic color grading)), ((epic scale)), "
                f"((professional VFX)), ((movie quality effects))"
            )
        
        return components

    def _handle_steampunk_theme(self, **kwargs) -> Dict[str, str]:
        """Steampunk theme handler with enhanced color palettes."""
        components = {}
        
        # Select color palettes
        metal_color = random.choice(self.steampunk_color_palettes["metals"])
        wood_color = random.choice(self.steampunk_color_palettes["woods"])
        accent_color = random.choice(self.steampunk_color_palettes["accents"])
        environment = random.choice(self.steampunk_elements["environments"])  # Added missing variable
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((steampunk masterpiece)) of {custom_subject}, "
                f"((featuring rich {wood_color} elements)), "
                f"((Victorian industrial atmosphere))"
            )
        else:
            machine = random.choice(self.steampunk_elements["machines"])
            accessory = random.choice(self.steampunk_elements["accessories"])
            components["subject"] = (
                f"((steampunk masterpiece)) with ((massive {machine} in {metal_color})) and "
                f"((intricate {accessory} with {accent_color} details)), "
                f"((featuring rich {wood_color} elements)), "
                f"((Victorian industrial atmosphere))"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(self.steampunk_times)
            weather = random.choice(self.steampunk_weather)
            components["environment"] = (
                f"in a ((detailed {environment})) during {time} with {weather}, "
                f"((Victorian industrial era)), ((steampunk atmosphere)), "
                f"((mechanical complexity)), ((featuring {metal_color} and {accent_color} tones))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((steampunk aesthetic)), ((Victorian industrial)), "
                f"((detailed {metal_color} machinery)), ((intricate mechanical design)), "
                f"((ornate {wood_color} elements)), ((vintage technology)), "
                f"((with {accent_color} highlights)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((steam effects)), ((mechanical glow)), "
                f"(({metal_color} reflections)), ((gear mechanisms)), "
                f"((industrial smoke)), (({accent_color} accents)), "
                f"((vintage patina)), ((atmospheric depth))"
            )
        
        return components

    def _handle_underwater_theme(self, **kwargs) -> Dict[str, str]:
        """Underwater theme handler with enhanced color schemes."""
        components = {}
        
        # Select color schemes
        depth_color = random.choice(self.underwater_color_schemes["depths"])
        shallow_color = random.choice(self.underwater_color_schemes["shallows"])
        biolum_color = random.choice(self.underwater_color_schemes["bioluminescence"])
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((epic underwater scene)) of {custom_subject}, "
                f"((in {depth_color} waters)), "
                f"((ultra detailed oceanic environment))"
            )
        else:
            structure = random.choice(self.underwater_elements["structures"])
            life_form = random.choice(self.underwater_elements["life_forms"])
            tech = random.choice(self.underwater_elements["technology"])
            components["subject"] = (
                f"((epic underwater civilization)) with ((massive {structure})) and "
                f"((exotic {life_form})), ((in {depth_color} waters)), "
                f"((featuring advanced {tech})), ((ultra detailed oceanic metropolis))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in ((deep ocean waters)) with ((mesmerizing {biolum_color} lighting)), "
                f"((crystal clear {shallow_color} visibility)), ((schools of exotic fish)), "
                f"((mysterious aquatic atmosphere)), ((underwater currents))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((cinematic underwater photography)), ((perfect clarity)), "
                f"((volumetric god rays)), ((dynamic composition)), "
                f"((ultra sharp focus)), ((aquatic color palette)), "
                f"((professional underwater lighting)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((water caustics)), ((bioluminescent {biolum_color} glow)), "
                f"((floating particles)), ((underwater atmospheric perspective)), "
                f"((gentle water currents)), ((refracted light beams)), "
                f"((bubbles and foam)), ((aquatic depth of field))"
            )
        
        return components

    def _handle_bio_organic_theme(self, **kwargs) -> Dict[str, str]:
        """Bio-organic technology theme handler."""
        components = {}
        
        # Select common elements needed for both paths
        aesthetic = random.choice(self.bio_organic_elements["aesthetics"])  # Moved outside if/else
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((hybrid bio-mechanical artwork)) of {custom_subject}, "
                f"((organic integration)), ((seamless fusion)), "
                f"((bio-digital harmony))"
            )
        else:
            # Original bio-organic theme logic
            structure = random.choice(self.bio_organic_elements["structures"])
            process = random.choice(self.bio_organic_elements["processes"])
            
            components["subject"] = (
                f"((hybrid bio-mechanical artwork)) of ((living {structure})) "
                f"((performing {process})), ((organic integration)), "
                f"((seamless fusion)), ((bio-digital harmony))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"featuring ((intricate {aesthetic})), ((living technology)), "
                f"((organic machinery)), ((bio-digital fusion)), "
                f"((technological symbiosis)), ((natural integration))"
            )
        
        if kwargs.get("include_style") == "yes":
            digital_technique = random.choice(self.digital_art_techniques)
            components["style"] = (
                f"((organic integration)), ((seamless fusion)), "
                f"((living technology)), ((ultra sharp focus)), "
                f"((bio-mechanical detail)), ((enhanced with {digital_technique})), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            digital_effect = random.choice(self.digital_art_effects)
            components["effects"] = (
                f"with ((bioluminescent highlights)), ((organic patterns)), "
                f"((technological elements)), ((flowing energy)), "
                f"((living circuits)), ((pulsing mechanisms)), "
                f"((subtle {digital_effect})), ((bio-digital effects))"
            )
        
        return components

    def _handle_binet_theme(self, **kwargs) -> Dict[str, str]:
        """Binet theme handler with enhanced portrait styles."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((anthropomorphic portrait)) of {custom_subject}, "
                f"((aristocratic pose)), ((noble expression)), "
                f"((intricate fur detail)), ((dramatic studio lighting))"
            )
        else:
            # Original binet theme logic...
            is_color = random.random() < 0.9  # 90% chance for color
            portrait_style = random.choice(self.binet_portrait_styles)
            
            # Initialize style_prefix and color_emphasis
            if is_color:
                color_scheme = random.choice(self.binet_color_schemes)
                style_prefix = f"sophisticated {portrait_style}"
                color_emphasis = f", {color_scheme}"
            else:
                style_prefix = f"sophisticated black and white {portrait_style}"
                color_emphasis = ", ((dramatic black and white)), ((extreme contrast))"
            
            # Select a distinguished animal
            animal = random.choice([
                "wolf", "fox", "lion", "tiger", "leopard", "panther", "lynx",
                "eagle", "hawk", "falcon", "owl", "deer", "horse", "elk",
                "bear", "gorilla", "raccoon", "red panda"
            ])
            
            # Determine if it's a contemporary or classical theme
            is_contemporary = random.random() < 0.3  # 30% chance for contemporary
            
            # Select clothing type
            clothing_type = random.choice(["sports", "urban", "formal"])
            
            if is_contemporary:
                # Use contemporary themes and elements
                character_theme = random.choice(self.binet_contemporary_themes)
                costume = random.choice(self.binet_sports_gear)
                props = random.choice(self.binet_urban_elements)
                celebration = random.choice(self.binet_celebration_elements)
                
                components["subject"] = (
                    f"((anthropomorphic {portrait_style} portrait)) of a ((distinguished {animal})) "
                    f"as a ((noble {character_theme})), "
                    f"((wearing {costume})), ((with {props})), "
                    f"((dressed in {random.choice(self.specific_clothing[clothing_type])})), "
                    f"((aristocratic pose)), ((noble expression)), "
                    f"((intricate fur detail)), ((dramatic studio lighting)){color_emphasis}"
                )
            else:
                # Use classical themes and elements
                character_theme = random.choice(self.binet_character_themes)
                costume = random.choice(self.binet_costume_elements)
                props = random.choice(self.binet_props_and_weapons)
                
                components["subject"] = (
                    f"((anthropomorphic {portrait_style} portrait)) of a ((distinguished {animal})) "
                    f"as a ((noble {character_theme})), "
                    f"((wearing {costume})), ((with {props})), "
                    f"((dressed in {random.choice(self.specific_clothing[clothing_type])})), "
                    f"((aristocratic pose)), ((noble expression)), "
                    f"((intricate fur detail)), ((dramatic studio lighting)){color_emphasis}"
                )
        
        if kwargs.get("include_environment") == "yes":
            environment = random.choice(self.binet_environments)
            components["environment"] = environment
        
        if kwargs.get("include_style") == "yes":
            # Only use style_prefix if it was defined (i.e., if custom_subject wasn't used)
            if custom_subject:
                components["style"] = (
                    f"((masterful composition)), ((professional studio lighting)), "
                    f"((sharp focus)), ((photorealistic detail)), "
                    f"((cinematic framing)), 8k resolution"
                )
            else:
                components["style"] = (
                    f"{style_prefix}, ((masterful composition)), "
                    f"((professional studio lighting)), ((sharp focus)), "
                    f"((photorealistic detail)), ((cinematic framing)), "
                    f"8k resolution{color_emphasis}"
                )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                "with ((deep shadows)), ((bright highlights)), "
                "((dramatic atmosphere)), ((volumetric lighting)), "
                "((perfect exposure)), ((subtle vignette))"
            )
        
        return components

    def _handle_curvy_girl_theme(self, **kwargs) -> Dict[str, str]:
        """Curvy fashion theme handler."""
        components = {}
        
        # Select base elements first so they're available for all paths
        style = random.choice(self.curvy_fashion_styles)
        pose = random.choice(self.curvy_fashion_poses)
        clothing = random.choice(self.curvy_fashion_clothing)
        composition = random.choice(self.compositions)
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((professional fashion photograph)) of {custom_subject}, "
                f"((body positive)), ((fashion editorial)), "
                f"((elegant pose)), ((high-end fashion))"
            )
        else:
            components["subject"] = (
                f"((professional fashion photograph)) of a ((confident curvy model)) in a "
                f"((graceful {pose})), wearing ((elegant {clothing})), "
                f"((body positive)), ((fashion editorial)), {composition}"
            )
        
        if kwargs.get("include_environment") == "yes":
            setting = random.choice(self.curvy_fashion_settings)
            components["environment"] = (
                f"in a ((premium {setting})), ((professional studio setup)), "
                f"((fashion photography lighting)), ((elegant atmosphere))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((high-end {style})), ((professional fashion photography)), "
                f"((magazine quality)), ((editorial style)), ((perfect exposure)), "
                f"((fashion lighting)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((professional retouching)), ((perfect color grading)), "
                f"((studio lighting)), ((fashion magazine quality)), "
                f"((editorial finish)), ((high-end post-processing))"
            )
        
        return components

    def _handle_manga_panel_theme(self, **kwargs) -> Dict[str, str]:
        """Manga panel theme handler with enhanced storytelling elements."""
        components = {}
        
        # Select base elements
        style = random.choice(self.manga_panel_styles)
        composition = random.choice(self.manga_panel_compositions)
        effect = random.choice(self.manga_panel_effects)
        expression = random.choice(self.manga_panel_expressions)
        emotion = random.choice(self.manga_storytelling_elements["emotions"])
        background = random.choice(self.manga_panel_backgrounds)  # Added missing variable
        layout = random.choice(self.manga_storytelling_elements["layouts"])  # Added missing variable
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((professional manga artwork)) of {custom_subject}, "
                f"((featuring {expression})), ((clean linework)), "
                f"((conveying {emotion})), ((manga panel composition)), "
                f"{composition}"
            )
        else:
            components["subject"] = (
                f"((professional manga artwork)) in {style} style, "
                f"((featuring {expression})), ((clean linework)), "
                f"((conveying {emotion})), ((manga panel composition)), "
                f"{composition}"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"with ((detailed {background})), ((manga aesthetics)), "
                f"((in {layout})), ((panel layout)), ((dramatic perspective))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional manga style)), ((sharp inking)), "
                f"((dynamic composition)), ((emotional impact)), "
                f"((clean artwork)), ((manga aesthetics)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with (({effect})), ((manga shading)), "
                f"((dramatic contrast)), ((emotional intensity)), "
                f"((panel composition)), ((artistic finish))"
            )
        
        return components

    def _handle_village_theme(self, **kwargs) -> Dict[str, str]:
        """Village theme handler with enhanced cultural elements."""
        components = {}
        
        # Select region and cultural elements
        region = random.choice(["asian", "european", "middle_eastern"])
        cultural_style = random.choice(self.cultural_styles[region])
        cultural_atmosphere = random.choice(self.cultural_atmospheres[region])
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((breathtaking village scene)) of {custom_subject}, "
                f"((in {cultural_style} style)), ((masterful composition)), "
                f"((cultural authenticity))"
            )
        else:
            village_type = random.choice(self.village_types)
            architecture = random.choice(self.village_architecture)
            cultural = random.choice(self.village_cultural_elements)
            view = random.choice(self.village_views)
            components["subject"] = (
                f"((breathtaking {view})) of a ((traditional {village_type})) "
                f"with ((authentic {architecture})) and ((detailed {cultural})), "
                f"((in {cultural_style} style)), ((masterful composition)), "
                f"((cultural authenticity))"
            )
        
        if kwargs.get("include_environment") == "yes":
            season = random.choice(list(self.seasonal_elements.keys()))
            seasonal_element = random.choice(self.seasonal_elements[season])
            components["environment"] = (
                f"featuring ((beautiful {seasonal_element})), "
                f"((with {cultural_atmosphere})), ((natural beauty)), "
                f"((cultural heritage)), ((traditional lifestyle))"
            )
        
        if kwargs.get("include_style") == "yes":
            photo_style = random.choice(self.photography_styles)
            mood = random.choice(self.photography_moods)  # Using photography_moods
            components["style"] = (
                f"((professional {photo_style})), ((perfect exposure)), "
                f"((cultural authenticity)), ((architectural details)), "
                f"((capturing {mood} mood)), ((rich colors)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            dramatic_light = random.choice(self.lighting_setups["dramatic"])
            components["effects"] = (
                f"with ((natural lighting)), ((atmospheric depth)), "
                f"((perfect composition)), ((rich textures)), "
                f"((cultural details)), ((environmental harmony)), "
                f"((enhanced by {dramatic_light} lighting))"
            )
        
        return components

    def _handle_vintage_anthro_theme(self, **kwargs) -> Dict[str, str]:
        """Vintage anthropomorphic theme handler."""
        components = {}
        
        # Generate base anthropomorphic character
        animal = random.choice(self.animals)
        profession = random.choice(self.vintage_anthro_professions)
        clothing = random.choice(self.vintage_anthro_clothing)
        activity = random.choice(self.vintage_anthro_activities)
        prop = random.choice(self.vintage_anthro_props)
        setting = random.choice(self.vintage_anthro_settings)
        
        components["subject"] = (
            f"hyper-realistic anthropomorphic {animal} with detailed fur texture "
            f"and human-like expressions, as a {profession}"
        )
        
        if kwargs.get("include_action") == "yes":
            components["action"] = (
                f"{activity}, wearing ((highly detailed {clothing})), "
                f"holding {prop}"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a {setting}, vintage Victorian era atmosphere, "
                f"volumetric lighting"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"professional vintage photography, ultra-realistic textures, "
                f"detailed fabric and fur rendering, studio lighting setup, "
                f"sharp focus, 8k resolution, photorealistic details"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with cinematic color grading, subtle film grain, "
                f"perfect exposure, volumetric lighting, detailed shadows, "
                f"and period-accurate details"
            )
        
        return components

    def _handle_realistic_theme(self, **kwargs) -> Dict[str, str]:
        """Realistic photography theme handler with enhanced photography attributes."""
        components = {}
        
        # Select base elements with more photography-specific attributes
        photo_style = random.choice(self.photography_styles)
        technique = random.choice(self.photography_techniques)
        mood = random.choice(self.photography_moods)
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((professional {photo_style})) of {custom_subject}, "
                f"((using {technique})), ((capturing {mood} mood)), "
                f"((perfect composition))"
            )
        else:
            if random.random() < 0.7:  # 70% chance for human subject
                profession = random.choice(self.professions)
                clothing = random.choice(self.clothing["realistic"])
                components["subject"] = (
                    f"((professional {photo_style})) of {profession} wearing {clothing}, "
                    f"((using {technique})), ((in {mood} mood)), "
                    f"((perfect composition))"
                )
            else:  # 30% chance for nature/animal
                animal = random.choice(self.animals)
                behavior = random.choice(self.behaviors)
                components["subject"] = (
                    f"((professional {photo_style})) of {animal} {behavior}, "
                    f"((using {technique})), ((capturing {mood} mood)), "
                    f"((perfect composition))"
                )
        
        if kwargs.get("include_environment") == "yes":
            lighting = random.choice(self.lighting_setups["natural"])
            dramatic_light = random.choice(self.lighting_setups["dramatic"])
            components["environment"] = (
                f"with ((natural {lighting} lighting)), "
                f"((enhanced by {dramatic_light})), "
                f"((perfect exposure)), ((atmospheric depth))"
            )
        
        if kwargs.get("include_style") == "yes":
            workflow = random.choice(self.digital_art_workflows)  # Using digital_art_workflows
            components["style"] = (
                f"((professional photography)), ((ultra sharp focus)), "
                f"((perfect exposure)), ((high detail)), ((color accurate)), "
                f"((masterful composition)), ((using {workflow})), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            digital_effect = random.choice(self.digital_art_effects)
            components["effects"] = (
                f"with ((natural lighting)), ((atmospheric depth)), "
                f"((perfect composition)), ((rich textures)), "
                f"((environmental harmony)), ((photographic realism)), "
                f"((subtle {digital_effect}))"
            )
        
        return components

    def _handle_christmas_theme(self, **kwargs) -> Dict[str, str]:
        """Christmas theme handler."""
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((festive Christmas scene)) of {custom_subject}, "
                f"((holiday spirit)), ((magical atmosphere)), "
                f"((Christmas wonder)), ((festive charm))"
            )
        else:
            character = random.choice(self.christmas_elements["characters"])
            activity = random.choice(self.christmas_elements["activities"])
            decoration = random.choice(self.christmas_elements["decorations"])
            components["subject"] = (
                f"((festive Christmas scene)) of ((cheerful {character})), "
                f"((engaged in {activity})), ((surrounded by {decoration})), "
                f"((holiday spirit)), ((magical atmosphere))"
            )
        
        if kwargs.get("include_action") == "yes":
            activity = random.choice(self.christmas_elements["activities"])  # Get a new activity for variation
            components["action"] = (
                f"((joyfully {activity})), ((festive movement)), "
                f"((holiday cheer)), ((Christmas spirit))"
            )
        
        if kwargs.get("include_environment") == "yes":
            setting = random.choice(self.christmas_elements["settings"])
            weather = random.choice(self.christmas_elements["weather"])
            season = "winter"
            seasonal_element = random.choice(self.seasonal_elements[season])
            components["environment"] = (
                f"in a ((magical {setting})) during {weather}, "
                f"featuring ((beautiful {seasonal_element})), "
                f"((festive atmosphere)), ((Christmas magic)), "
                f"((holiday warmth))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.christmas_styles)
            mood = random.choice(self.christmas_moods)
            components["style"] = (
                f"((holiday {style})), ((festive style)), "
                f"((Christmas colors)), ((warm lighting)), "
                f"({mood} atmosphere)), ((seasonal charm)), "
                f"((perfect composition)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            magical_effect = random.choice(self.christmas_elements["magical_effects"])  # Changed from "effects" to "magical_effects"
            components["effects"] = (
                f"with ((magical {magical_effect})), ((twinkling lights)), "
                f"((soft snowfall)), ((warm glow)), ((festive sparkle)), "
                f"((holiday magic)), ((Christmas wonder))"
            )
        
        return components

    def _handle_selfie_theme(self, **kwargs) -> Dict[str, str]:
        """Selfie theme handler with location-appropriate styling."""
        components = {}
        
        # Define location-based clothing styles
        location_outfits = {
            "beach": ["swimsuit", "beach cover-up", "summer dress", "board shorts", "resort wear"],
            "gym": ["workout outfit", "athletic wear", "sports bra and leggings", "gym shorts and tank top"],
            "cafe": ["casual chic outfit", "trendy streetwear", "fashionable ensemble", "smart casual attire"],
            "restaurant": ["elegant dress", "formal suit", "cocktail attire", "upscale outfit"],
            "hiking trail": ["hiking gear", "outdoor activewear", "trail outfit", "adventure wear"],
            "tourist spot": ["comfortable tourist outfit", "casual travel wear", "sightseeing attire"],
            "shopping mall": ["trendy casual wear", "shopping outfit", "fashion-forward ensemble"],
            "party": ["party dress", "club wear", "evening attire", "festive outfit"],
            "office": ["business attire", "professional suit", "corporate wear", "business casual"],
            "park": ["casual outdoor wear", "picnic outfit", "relaxed ensemble"]
        }
        
        # Select location and appropriate outfit
        location = random.choice(list(location_outfits.keys()))
        outfit = random.choice(location_outfits[location])
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        if custom_subject:
            components["subject"] = (
                f"((professional selfie photograph)) of {custom_subject}, "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        else:
            components["subject"] = (
                f"((professional selfie photograph)) of ((attractive person)), "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(["golden hour", "sunset", "bright daylight", "blue hour", "evening"])
            components["environment"] = (
                f"at a ((beautiful {location})) during {time}, "
                f"((perfect lighting)), ((instagram-worthy background)), "
                f"((social media aesthetic)), ((lifestyle photography))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((social media photography)), ((smartphone aesthetic)), "
                f"((perfect exposure)), ((authentic lifestyle)), "
                f"((trendy composition)), ((influencer style)), "
                f"((natural looking)), ((candid moment)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((natural bokeh)), ((soft skin glow)), "
                f"((perfect lighting)), ((subtle vignette)), "
                f"((instagram filter)), ((social media finish)), "
                f"((lifestyle colors)), ((authentic atmosphere))"
            )
        
        return components