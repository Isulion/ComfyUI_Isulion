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
            "📱 Selfie": "selfie", 
            "💥 Futuristic Battlefield": "futuristic_battlefield",  
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
                    "💥 Futuristic Battlefield", 
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
                    "📱 Selfie", 
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
                "custom_location": ("STRING", {"default": "", "multiline": True}),  # Added this line
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
                custom_subject: str = "", custom_location: str = "",  # Added custom_location parameter
                include_environment: str = "yes", 
                include_style: str = "yes", 
                include_effects: str = "yes") -> Tuple[str, str, str, str, str, int]:
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
            custom_location=custom_location.strip(),  # Make sure custom_location is passed
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
        components = {}
        
        # Use custom subject if provided
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
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
            if custom_location:
                components["environment"] = f"in {custom_location}"
            else:
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((detailed {custom_location})) with ((perfect lighting)), "
                    f"((dramatic atmosphere)), ((stunning background detail)), "
                    f"((masterful scene composition))"
                )
            else:
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
        
        # Determine logo style approach with adjusted weights
        # Reduce weight of character style (which includes animals) from 0.15 to 0.05
        style_approach = random.choices(
            ["classic", "3D", "character", "artistic"],
            weights=[0.6, 0.2, 0.05, 0.15]  # Classic logos are most common, character logos (which may include animals) are rarer
        )[0]
        
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
            # Reduced list of mascot options, focusing more on abstract/cute characters rather than specific animals
            mascot_options = [
                "cute mascot", "friendly character", "abstract character",
                "geometric character", "playful mascot", "simple character",
                "minimalist mascot", "modern character", "unique mascot"
            ]
            character = random.choice(mascot_options)
            decorative = random.choice(self.logo_decorative_elements)
            
            components["subject"] = (
                f"((professional {character} logo)) with the text \"{logo_text}\", "
                f"((cute character design)), ((playful typography)), "
                f"((charming illustration)), ((logo style))"
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        style = random.choice(self.caricature_styles)
        features = random.choice(self.caricature_features)
        expression = random.choice(self.caricature_expressions)
        elements = random.choice(self.caricature_elements)
        
        components["subject"] = (
            f"((highly exaggerated cartoon caricature)) of {custom_subject if custom_subject else 'Donald Trump'}), "
            f"with ((extremely {features})), "
            f"((showing a {expression})), "
            f"((cartoon-style exaggeration)), "
            f"((comic book distortion)), "
            f"((animated caricature style))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((detailed {custom_location})), "
                    f"((caricature composition)), ((artistic atmosphere)), "
                    f"((contextual details))"
                )
            else:
                elements = random.choice(self.caricature_elements)
                setting = random.choice(self.caricature_settings)
                weather = random.choice(self.weather)
                time = random.choice(self.times)
                components["environment"] = (
                    f"in a ((detailed {setting})) during {weather} {time}, "
                    f"with ((meaningful {elements})), ((caricature composition)), "
                    f"((artistic atmosphere)), ((contextual details))"
                )

        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((caricature art style)), ((exaggerated features)), "
                f"((cartoon aesthetics)), ((dynamic composition)), "
                f"((professional quality)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((cartoon effects)), ((exaggerated proportions)), "
                f"((dynamic lines)), ((artistic finish)), "
                f"((professional rendering)), ((caricature style))"
            )

        return components  # Added return statement

    def _handle_futuristic_city_theme(self, **kwargs) -> Dict[str, str]:
        """Futuristic city theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        composition = random.choice(self.compositions)
        atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((futuristic {custom_location})), "
                    f"((advanced technology)), ((cyberpunk elements)), "
                    f"((futuristic urban landscape))"
                )
            else:
                time = random.choice(self.futuristic_city_elements["time"])
                components["environment"] = (
                    f"during {time}, ((with {atmosphere} atmosphere)), "
                    f"((advanced technology)), ((cyberpunk elements)), "
                    f"((futuristic urban landscape))"
                )

        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((futuristic aesthetic)), ((sci-fi atmosphere)), "
                f"((advanced technology)), ((cyberpunk style)), "
                f"((ultra modern design)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((neon lighting)), ((holographic displays)), "
                f"((volumetric fog)), ((light rays)), ((energy effects)), "
                f"((reflective surfaces)), ((atmospheric perspective))"
            )

        return components  # Added missing return

    def _handle_halloween_theme(self, **kwargs) -> Dict[str, str]:
        """Halloween theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        creature = random.choice(self.halloween_elements["creatures"])
        prop = random.choice(self.halloween_elements["props"])
        effect = random.choice(self.halloween_effects)
        
        components["subject"] = (
            f"((spooky {custom_subject if custom_subject else creature})) with ((haunted {prop})), "
            f"((eerie atmosphere)), ((halloween theme)), "
            f"((with {effect}))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in a ((haunted {custom_location})), "
                    f"((gothic atmosphere)), ((supernatural ambiance))"
                )
            else:
                setting = random.choice(self.halloween_elements["settings"])
                time = random.choice(self.halloween_times)
                weather = random.choice(self.halloween_weather)
                components["environment"] = (
                    f"in a ((haunted {setting})) during {weather} {time}, "
                    f"((gothic atmosphere)), ((supernatural ambiance))"
                )

        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((halloween aesthetic)), ((spooky atmosphere)), "
                f"((gothic style)), ((eerie mood)), "
                f"((haunting quality)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((ghostly mist)), ((eerie glow)), "
                f"((dark shadows)), ((moonlight rays)), "
                f"((supernatural effects)), ((ominous atmosphere))"
            )

        return components  # Added missing return

    def _handle_instagram_theme(self, **kwargs) -> Dict[str, str]:
        """Instagram theme handler with enhanced lighting effects."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        influencer = random.choice(self.influencer_types)
        activity = random.choice(self.influencer_activities)
        lighting_effect = random.choice(self.instagram_lighting_effects)
        
        components["subject"] = (
            f"professional lifestyle photograph of {custom_subject if custom_subject else influencer} {activity}, "
            f"((with {lighting_effect})), "
            f"((instagram aesthetic)), ((social media style)))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"at ((beautiful {custom_location})), "
                    f"((lifestyle setting)), ((perfect ambiance)), "
                    f"((instagram worthy location)), ((premium environment)), "
                    f"((social media backdrop)), ((influencer location)))"
                )
            else:
                time = random.choice(self.instagram_times)
                location = random.choice(self.influencer_locations)
                components["environment"] = (
                    f"at {location} during {time}, "
                    f"((lifestyle setting)), ((perfect ambiance)), "
                    f"((instagram worthy location)), ((premium environment)), "
                    f"((social media backdrop)), ((influencer location)))"
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        if random.random() < 0.7:  # 70% chance for action scene
            action = random.choice(self.marvel_action_scenes)
            components["subject"] = (
                f"((classic Marvel comic book art)) of {custom_subject if custom_subject else random.choice(self.marvel_characters)} {action}, "
                f"((vintage comic book illustration)), ((comic book art))"
            )
        else:  # 30% chance for character portrait
            pose = random.choice(self.marvel_poses)
            components["subject"] = (
                f"((classic Marvel comic book art)) of {custom_subject if custom_subject else random.choice(self.marvel_characters)} in {pose}, "
                f"((vintage comic book illustration)), ((comic book art))"
            )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((epic {custom_location})), with classic comic book background, "
                    f"dramatic comic perspective"
                )
            else:
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        # Select common elements
        furniture = random.choice(self.peaky_blinders_furniture)
        prop = random.choice(self.peaky_blinders_props)
        atmosphere = random.choice(self.peaky_blinders_atmospheres)
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((1920s {custom_location})) with {furniture}, "
                    f"surrounded by {prop}, {atmosphere}"
                )
            else:
                setting = random.choice(self.peaky_blinders_settings)
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
        
        # Select base elements
        style = random.choice(self.pixar_styles)
        character_trait = random.choice(self.pixar_characteristics)
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()

        if custom_subject:
            components["subject"] = (
                f"{style} of {custom_subject}, "
                f"with {character_trait}, "
                f"((ultra detailed 3D model)), ((Pixar animation style)), "
                f"((charming character design)), ((appealing features))"
            )
        else:
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
            if custom_location:
                components["environment"] = (
                    f"in ((charming {custom_location})), ((magical atmosphere)), "
                    f"((colorful setting)), ((playful scene)), "
                    f"((perfect lighting)), ((detailed background))"
                )
            else:
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((devastated {custom_location})) with ((post-apocalyptic atmosphere)), "
                    f"((wasteland environment)), ((signs of destruction))"
                )
            else:
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        character = random.choice(self.school_manga_characters)
        uniform = random.choice(self.school_manga_uniforms)
        accessory = random.choice(self.school_manga_accessories)
        linework = random.choice(self.school_manga_linework)
        shading = random.choice(self.school_manga_shading)
        
        components["subject"] = (
            f"((professional black and white manga illustration)) of {custom_subject if custom_subject else f'a {character}'}, "
            f"wearing ((technically detailed {uniform})), with ((masterfully rendered {accessory})), "
            f"((perfect manga linework)), ((professional ink technique)), "
            f"((high contrast black and white rendering)), ((clean technical execution))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((detailed manga {custom_location})) with ((precise architectural linework)), "
                    f"((perfect perspective control)), ((clean background separation)), "
                    f"((professional environmental detail)), ((masterful spatial depth)), "
                    f"((sharp background contrast))"
                )
            else:
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
        """Steampunk theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        metal_color = random.choice(self.steampunk_color_palettes["metals"])
        wood_color = random.choice(self.steampunk_color_palettes["woods"])
        accent_color = random.choice(self.steampunk_color_palettes["accents"])
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((steampunk {custom_location})), "
                    f"((Victorian industrial era)), ((steampunk atmosphere)), "
                    f"((mechanical complexity)), ((featuring {metal_color} and {accent_color} tones))"
                )
            else:
                environment = random.choice(self.steampunk_elements["environments"])
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
        """Underwater theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        depth_color = random.choice(self.underwater_color_schemes["depths"])
        shallow_color = random.choice(self.underwater_color_schemes["shallows"])
        biolum_color = random.choice(self.underwater_color_schemes["bioluminescence"])
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((underwater {custom_location})) with ((mesmerizing {biolum_color} lighting)), "
                    f"((crystal clear {shallow_color} visibility)), ((schools of exotic fish)), "
                    f"((mysterious aquatic atmosphere)), ((underwater currents))"
                )
            else:
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
                f"((magazine quality)), ((editorial style)), "
                f"((perfect exposure)), ((fashion lighting)), 8k resolution"
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
        """Village theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        village_type = random.choice(self.village_types)
        architecture = random.choice(self.village_architecture)
        cultural = random.choice(self.village_cultural_elements)
        view = random.choice(self.village_views)
        
        components["subject"] = (
            f"((breathtaking {view})) of {custom_subject if custom_subject else f'a ((traditional {village_type}))'} "
            f"with ((authentic {architecture})) and ((detailed {cultural})), "
            f"((masterful composition)), ((cultural authenticity))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((traditional {custom_location})), "
                    f"((cultural heritage)), ((natural beauty)), "
                    f"((traditional lifestyle)), ((authentic atmosphere))"
                )
            else:
                season = random.choice(list(self.seasonal_elements.keys()))
                seasonal_element = random.choice(self.seasonal_elements[season])
                components["environment"] = (
                    f"featuring ((beautiful {seasonal_element})), "
                    f"((cultural heritage)), ((natural beauty)), "
                    f"((traditional lifestyle))"
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
        """Realistic photography theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        photo_style = random.choice(self.photography_styles)
        technique = random.choice(self.photography_techniques)
        mood = random.choice(self.photography_moods)
        
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
            if custom_location:
                components["environment"] = (
                    f"in ((detailed {custom_location})), "
                    f"((perfect exposure)), ((atmospheric depth))"
                )
            else:
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
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        character = random.choice(self.christmas_elements["characters"])
        activity = random.choice(self.christmas_elements["activities"])
        decoration = random.choice(self.christmas_elements["decorations"])
        
        components["subject"] = (
            f"((festive Christmas scene)) of {custom_subject if custom_subject else f'((cheerful {character}))'}, "
            f"((engaged in {activity})), ((surrounded by {decoration})), "
            f"((holiday spirit)), ((magical atmosphere))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((magical {custom_location})) with ((festive atmosphere)), "
                    f"((Christmas magic)), ((holiday warmth))"
                )
            else:
                setting = random.choice(self.christmas_elements["settings"])
                weather = random.choice(self.christmas_elements["weather"])
                components["environment"] = (
                    f"in a ((magical {setting})) during {weather}, "
                    f"((festive atmosphere)), ((Christmas magic)), "
                    f"((holiday warmth))"
                )

        if kwargs.get("include_action") == "yes":
            activity = random.choice(self.christmas_elements["activities"])  # Get a new activity for variation
            components["action"] = (
                f"((joyfully {activity})), ((festive movement)), "
                f"((holiday cheer)), ((Christmas spirit))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.christmas_styles)
            mood = random.choice(self.christmas_moods)
            components["style"] = (
                f"((holiday {style})), ((festive style)), "
                f"((Christmas colors)), ((warm lighting)), ({mood} atmosphere)), "
                f"((seasonal charm)), ((perfect composition)), 8k resolution"
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
        
        # Get custom location and subject
        custom_location = kwargs.get("custom_location", "").strip()
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Determine location and outfit
        if custom_location:
            # Use the custom location directly if provided
            location = custom_location
            # Try to find matching outfits or use generic outfit options
            matching_locations = [loc for loc in location_outfits.keys() 
                                    if loc.lower() in custom_location.lower()]
            if matching_locations:
                outfit = random.choice(location_outfits[matching_locations[0]])
            else:
                # Use casual outfit if no specific location match
                outfit = "stylish casual wear"
        else:
            location = random.choice(list(location_outfits.keys()))
            outfit = random.choice(location_outfits[location])
        
        # Build subject component
        if custom_subject:
            components["subject"] = (
                f"((professional selfie photograph)) of {custom_subject} at a ((beautiful {location})), "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        else:
            components["subject"] = (
                f"((professional selfie photograph)) of ((attractive person)) at a ((beautiful {location})), "
                f"((wearing {outfit})), ((perfect selfie angle)), "
                f"((flattering pose)), ((authentic expression)), "
                f"((high-quality smartphone photography))"
            )
        
        if kwargs.get("include_environment") == "yes":
            time = random.choice(["golden hour", "sunset", "bright daylight", "blue hour", "evening"])
            components["environment"] = (
                f"during {time}, ((perfect lighting)), "
                f"((instagram-worthy {location} background)), "
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

    def _handle_interior_theme(self, **kwargs) -> Dict[str, str]:
        """Interior theme handler with enhanced lighting."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        style = random.choice(self.interior_styles)
        space = random.choice(self.interior_spaces)
        element = random.choice(self.interior_elements)
        
        components["subject"] = (
            f"professional interior design photograph of {custom_subject if custom_subject else f'a ((luxury {style} {space}))'} "
            f"with ((premium {element})), ((masterful composition))"
        )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((luxury {custom_location})) with ((perfect lighting)), "
                    f"((luxury interior design)), ((perfect exposure)), "
                    f"((architectural visualization)), ((premium quality))"
                )
            else:
                time = random.choice(self.interior_times)
                lighting = random.choice(self.interior_lighting)
                components["environment"] = (
                    f"during {time} with ((perfect {lighting})), "
                    f"((luxury interior design)), ((perfect exposure)), "
                    f"((architectural visualization)), ((premium quality))"
                )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((luxury {style} {space} aesthetic)), ((premium {element} aesthetic)), "
                f"((professional interior design)), ((perfect lighting)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((luxury lighting)), ((high-end finishes)), "
                f"((customized design)), ((exclusive materials)), "
                f"((high-quality craftsmanship)), ((interior design harmony))"
            )
        
        return components

    def _handle_cute_chimera_theme(self, **kwargs) -> Dict[str, str]:
        """Cute Chimera theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base elements
        base_animal = random.choice(self.cute_animals)  # Changed from cute_animals to self.cute_animals
        action = random.choice(self.cute_chimera_actions)
        habitat = random.choice(self.cute_chimera_habitats) 
        weather = random.choice(self.cute_chimera_weather)
        emotion = random.choice(self.cute_chimera_emotions)
        art_style = random.choice(self.cute_chimera_art_styles)
        
        if custom_subject:
            components["subject"] = (
                f"((adorable chimera creature)) of {custom_subject}, "
                f"((showing {emotion} expression)), ((ultra cute design)), "
                f"((kawaii style)), ((fluffy texture)), ((charming features))"
            )
        else:
            components["subject"] = (
                f"((adorable chimera creature)) based on {base_animal}, "
                f"((showing {emotion} expression)), {action}, "
                f"((ultra cute design)), ((kawaii style)), "
                f"((fluffy texture)), ((charming features))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in a ((magical {habitat})) during {weather}, "
                f"((enchanted atmosphere)), ((dreamy setting)), "
                f"((whimsical environment)), ((fairy tale mood))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"(({art_style})), ((soft lighting)), "
                f"((pastel colors)), ((gentle shading)), "
                f"((adorable aesthetic)), ((sweet atmosphere)), "
                f"((magical mood)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((sparkly effects)), ((magical glow)), "
                f"((soft bokeh)), ((dreamy atmosphere)), "
                f"((gentle light rays)), ((fairy dust)), "
                f"((enchanted particles)), ((kawaii elements))"
            )
        
        return components

    def _handle_cartoon_theme(self, **kwargs) -> Dict[str, str]:
        """Animation Cartoon theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        # Select base elements
        character = random.choice(self.cartoon_characters)
        style = random.choice(self.cartoon_styles)
        expression = random.choice(self.cartoon_expressions)
        effect = random.choice(self.cartoon_effects)
        
        if custom_subject:
            components["subject"] = (
                f"((professional cartoon animation)) of {custom_subject}, "
                f"((with {expression})), ((animated character design)), "
                f"((cartoon style)), ((dynamic pose)), ((expressive features))"
            )
        else:
            components["subject"] = (
                f"((professional cartoon animation)) of {character}, "
                f"((with {expression})), ((animated character design)), "
                f"((cartoon style)), ((dynamic pose)), ((expressive features))"
            )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((animated {custom_location})), "
                    f"((cartoon world)), ((vibrant colors)), "
                    f"((dynamic background)), ((animated scenery))"
                )
            else:
                environment = random.choice(self.cartoon_environments)
                components["environment"] = (
                    f"in ((animated {environment})), "
                    f"((cartoon world)), ((vibrant colors)), "
                    f"((dynamic background)), ((animated scenery))"
                )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"(({style})), ((professional animation)), "
                f"((cartoon rendering)), ((vibrant palette)), "
                f"((dynamic composition)), ((animated style)), "
                f"((expressive design)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with (({effect})), ((cartoon physics)), "
                f"((animated motion)), ((dynamic lighting)), "
                f"((cartoon shading)), ((animated effects)), "
                f"((expressive animation))"
            )
        
        return components

    def _handle_architecture_theme(self, **kwargs) -> Dict[str, str]:
        """Architecture theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        # Select base elements
        style = random.choice(self.architecture_styles)
        element = random.choice(self.architecture_elements)
        
        if custom_subject:
            components["subject"] = (
                f"((architectural masterpiece)) of {custom_subject}, "
                f"((in {style} style)), ((architectural photography)), "
                f"((professional composition)), ((structural elegance))"
            )
        else:
            components["subject"] = (
                f"((architectural masterpiece)) of ((magnificent {element})), "
                f"((in {style} style)), ((architectural photography)), "
                f"((professional composition)), ((structural elegance))"
            )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((dramatic {custom_location})), "
                    f"((perfect lighting)), ((architectural context)), "
                    f"((professional environment)), ((structural harmony))"
                )
            else:
                lighting = random.choice(self.lighting_setups["dramatic"])
                components["environment"] = (
                    f"with ((dramatic {lighting})), ((architectural atmosphere)), "
                    f"((perfect perspective)), ((structural context)), "
                    f"((professional environment))"
                )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((architectural photography)), ((professional composition)), "
                f"((structural detail)), ((perfect lighting)), "
                f"((dramatic perspective)), ((technical precision)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((dramatic lighting)), ((perfect shadows)), "
                f"((architectural atmosphere)), ((structural emphasis)), "
                f"((professional post-processing)), ((technical excellence))"
            )
        
        return components

    def _handle_strange_animal_theme(self, **kwargs) -> Dict[str, str]:
        """Chimera Animals theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base animals
        animal_family = random.choice(list(self.animal_families.keys()))
        base_animal = random.choice(self.animal_families[animal_family])
        second_animal = random.choice(self.animals)  # Different animal for hybrid
        
        if custom_subject:
            components["subject"] = (
                f"((mythical chimera creature)) of {custom_subject}, "
                f"((hybrid anatomy)), ((fantastic beast)), "
                f"((magical creature)), ((mythological hybrid))"
            )
        else:
            components["subject"] = (
                f"((mythical chimera creature)) combining {base_animal} and {second_animal}, "
                f"((hybrid anatomy)), ((fantastic beast)), "
                f"((magical creature)), ((mythological hybrid))"
            )
        
        if kwargs.get("include_environment") == "yes":
            habitat = random.choice(self.mythical_locations)
            weather = random.choice(self.weather)
            components["environment"] = (
                f"in ((mystical {habitat})) during {weather}, "
                f"((magical atmosphere)), ((mythical realm)), "
                f"((fantastic setting))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.art_styles)
            components["style"] = (
                f"((fantasy art style)), ((mythical aesthetic)), "
                f"((creature design)), ((hybrid anatomy)), "
                f"((magical atmosphere)), ((professional quality)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.magical_effects["nature"])
            components["effects"] = (
                f"with ((magical {effect})), ((mystical aura)), "
                f"((fantastic atmosphere)), ((mythical elements)), "
                f"((hybrid features)), ((creature details))"
            )
        
        return components

    def _handle_food_theme(self, **kwargs) -> Dict[str, str]:
        """Food/Culinary theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base elements
        food_type = random.choice(self.food_types)
        style = random.choice(self.food_styles)
        setting = random.choice(self.food_settings)
        
        if custom_subject:
            components["subject"] = (
                f"((professional food photography)) of {custom_subject}, "
                f"((culinary art)), ((gourmet presentation)), "
                f"((food styling)), ((appetizing composition))"
            )
        else:
            components["subject"] = (
                f"((professional food photography)) of ((delicious {food_type})), "
                f"((culinary art)), ((gourmet presentation)), "
                f"((food styling)), ((appetizing composition))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"on ((beautiful {setting})), ((professional food styling)), "
                f"((culinary setting)), ((gourmet atmosphere)), "
                f"((restaurant quality))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"(({style})), ((professional food photography)), "
                f"((culinary excellence)), ((perfect lighting)), "
                f"((gourmet quality)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with ((perfect depth of field)), ((soft lighting)), "
                f"((appetizing colors)), ((food texture details)), "
                f"((professional styling)), ((culinary aesthetics))"
            )
        
        return components

    def _handle_3d_theme(self, **kwargs) -> Dict[str, str]:
        """3D theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base elements
        style = random.choice(self.threed_styles)
        material = random.choice(self.threed_materials)
        effect = random.choice(self.threed_effects)
        
        if custom_subject:
            components["subject"] = (
                f"((professional 3D render)) of {custom_subject}, "
                f"((in {style})), ((with {material} materials)), "
                f"((3D modeling)), ((perfect geometry))"
            )
        else:
            components["subject"] = (
                f"((professional 3D render)) in {style}, "
                f"((with {material} materials)), ((3D modeling)), "
                f"((perfect geometry)), ((detailed textures))"
            )
        
        if kwargs.get("include_environment") == "yes":
            environment = random.choice(self.threed_environments)
            components["environment"] = (
                f"in ((professional {environment})), "
                f"((perfect lighting setup)), ((3D space)), "
                f"((detailed environment)), ((studio quality))"
            )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"((professional 3D rendering)), ((perfect materials)), "
                f"((high-end finish)), ((technical excellence)), "
                f"((3D mastery)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with (({effect})), ((perfect reflections)), "
                f"((professional rendering)), ((3D effects)), "
                f"((technical precision)), ((render quality))"
            )
        
        return components

    def _handle_fantasy_theme(self, **kwargs) -> Dict[str, str]:
        """Fantasy theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        
        # Select base elements
        race = random.choice(self.races)
        profession = random.choice(self.professions)
        artifact = random.choice(self.artifacts["weapon"])
        location = random.choice(self.mythical_locations)
        
        if custom_subject:
            components["subject"] = (
                f"((fantasy artwork)) of {custom_subject}, "
                f"((magical character)), ((fantasy design)), "
                f"((mythical being)), ((enchanted presence))"
            )
        else:
            components["subject"] = (
                f"((fantasy artwork)) of ((magical {race} {profession})), "
                f"((wielding {artifact})), ((fantasy character)), "
                f"((mythical being)), ((enchanted presence))"
            )
        
        if kwargs.get("include_environment") == "yes":
            components["environment"] = (
                f"in ((magical {location})), ((fantasy realm)), "
                f"((mystical atmosphere)), ((enchanted setting)), "
                f"((mythical world))"
            )
        
        if kwargs.get("include_style") == "yes":
            style = random.choice(self.art_styles)
            components["style"] = (
                f"((fantasy art style)), ((magical aesthetic)), "
                f"((mythical quality)), ((enchanted atmosphere)), "
                f"((professional artwork)), 8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.magical_effects["arcane"])
            components["effects"] = (
                f"with ((magical {effect})), ((mystical aura)), "
                f"((fantasy elements)), ((enchanted effects)), "
                f"((mythical atmosphere))"
            )
        
        return components

    def _handle_cinema_theme(self, **kwargs) -> Dict[str, str]:
        """Cinema theme handler."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        # Select base elements
        location = random.choice(self.cinema_locations)
        prop = random.choice(self.cinema_props)
        atmosphere = random.choice(self.cinema_atmospheres)
        style = random.choice(self.cinema_styles)
        effect = random.choice(self.cinema_effects)
        action = random.choice(self.cinema_specific_actions)
        
        if custom_subject:
            components["subject"] = (
                f"((professional movie scene)) of {custom_subject}, "
                f"((with {prop})), ((cinematic quality)), "
                f"((movie production)), ((professional filming)), "
                f"{action}"
            )
        else:
            character = random.choice(self.cinema_characters)  # Using predefined cinema characters
            components["subject"] = (
                f"((professional movie scene)) of {character}, "
                f"((with {prop})), ((cinematic quality)), "
                f"((movie production)), ((professional filming)), "
                f"{action}"
            )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((cinematic {custom_location})), "
                    f"((with {atmosphere})), ((professional set design)), "
                    f"((movie set quality)), ((production value))"
                )
            else:
                components["environment"] = (
                    f"in ((professional {location})), "
                    f"((with {atmosphere})), ((professional set design)), "
                    f"((movie set quality)), ((production value))"
                )
        
        if kwargs.get("include_style") == "yes":
            components["style"] = (
                f"(({style})), ((professional cinematography)), "
                f"((movie production quality)), ((cinematic framing)), "
                f"((theatrical presentation)), ((film production)), "
                f"8k resolution"
            )
        
        if kwargs.get("include_effects") == "yes":
            components["effects"] = (
                f"with (({effect})), ((professional post-processing)), "
                f"((cinematic color grading)), ((movie effects)), "
                f"((production quality)), ((theatrical finish))"
            )
        
        return components

    def _handle_futuristic_battlefield_theme(self, **kwargs) -> Dict[str, str]:
        """Futuristic battlefield theme handler focused on weapons and military technology."""
        components = {}
        
        # Get custom inputs
        custom_subject = kwargs.get("custom_subject", "").strip()
        custom_location = kwargs.get("custom_location", "").strip()
        
        # Select base elements
        element = random.choice(self.battlefield_elements)
        atmosphere = random.choice(self.battlefield_atmospheres)
        
        if custom_subject:
            components["subject"] = (
                f"((advanced military hardware)) of {custom_subject}, "
                f"((weapons system)), ((military technology)), "
                f"((combat equipment)), ((future warfare)), "
                f"((tactical systems)), ((battlefield technology))"
            )
        else:
            components["subject"] = (
                f"((advanced military hardware)) featuring ((advanced {element})), "
                f"((weapons platform)), ((military innovation)), "
                f"((combat technology)), ((future warfare)), "
                f"((tactical systems)), ((battlefield advancement))"
            )
        
        if kwargs.get("include_environment") == "yes":
            if custom_location:
                components["environment"] = (
                    f"on ((war-torn {custom_location})), "
                    f"((with {atmosphere})), ((active combat zone)), "
                    f"((open battlefield)), ((future war scenario)), "
                    f"((outdoor combat area))"
                )
            else:
                setting = random.choice(self.battlefield_environments)
                components["environment"] = (
                    f"on ((massive {setting})), ((with {atmosphere})), "
                    f"((active battlefield)), ((combat terrain)), "
                    f"((war zone)), ((open combat field))"
                )

        if kwargs.get("include_style") == "yes":
            style = random.choice(self.battlefield_styles)
            components["style"] = (
                f"(({style})), ((military technology)), "
                f"((tactical visualization)), ((weapons design)), "
                f"((technical precision)), ((combat systems)), "
                f"((military hardware)), 8k resolution"
            )

        if kwargs.get("include_effects") == "yes":
            effect = random.choice(self.battlefield_effects)
            components["effects"] = (
                f"with ((dramatic {effect})), ((weapons discharge)), "
                f"((combat atmosphere)), ((battlefield lighting)), "
                f"((tactical effects)), ((system readouts)), "
                f"((weapons visuals)), ((war zone ambiance))"
            )
        
        return components