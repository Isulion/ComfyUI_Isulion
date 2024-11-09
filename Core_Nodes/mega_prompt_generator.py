import random

class IsulionMegaPromptGenerator:
    # Reuse all the existing lists/dictionaries from other nodes
    animals = ['Dog','Cat','Horse','Cow','Chicken','Pig','Sheep','Goat','Lion','Tiger','Elephant','Bear','Wolf','Fox','Deer','Rabbit','Kangaroo','Giraffe','Zebra','Monkey','Chimpanzee','Gorilla','Orangutan','Panda','Koala','Hippopotamus','Rhinoceros','Crocodile','Alligator','Eagle','Hawk','Falcon','Owl','Penguin','Dolphin','Shark','Octopus','Squid','Jellyfish','Crab','Lobster','Clownfish','Sea Turtle','Frog','Toad','Snake','Lizard','Gecko','Tortoise','Camel','Donkey','Bat','Rat','Mouse','Squirrel','Chipmunk','Porcupine','Hedgehog','Skunk','Raccoon','Otter','Seal','Walrus','Polar Bear','Grizzly Bear','Cheetah','Leopard','Jaguar','Antelope','Buffalo','Bison','Moose','Reindeer','Mole','Platypus','Echidna','Parrot','Peacock','Swan','Duck','Goose','Turkey','Flamingo','Pelican','Seagull','Sparrow','Pigeon','Crow','Magpie','Woodpecker','Hummingbird','Butterfly','Bee','Ant','Spider','Scorpion','Worm','Snail']  # from Animal node
    cute_animals = ['Red Panda','Koala','Fennec Fox','Pygmy Marmoset','Quokka','Sea Otter','Harp Seal Pup','Panda Cub','Penguin Chick','Hedgehog','Axolotl','Sloth','Rabbit','Kitten','Puppy','Meerkat','Sugar Glider','Chinchilla','Slow Loris','Hamster','Red Fox Kit','Lamb','Piglet','Duckling','Pygmy Hippo','Baby Giraffe','Baby Alpaca','Otter Pup','Corgi Puppy','Golden Retriever Puppy','Seal Pup','Snow Leopard Cub','Tiger Cub','Lion Cub','Baby Gorilla','Baby Orangutan','Pygmy Goat','Fawn (Baby Deer)','Ferret','Platypus','Kangaroo Joey','Wallaby','Serval Kitten','Caracal Kitten','Clouded Leopard Cub','Red Squirrel','Chipmunk','Prairie Dog','Arctic Fox','Polar Bear Cub','Baby Skunk','Raccoon Kit','Baby Opossum','Baby Echidna (Puggle)','Baby Tapir','GiantPanda Cub','Baby Hippo','Baby Rhino','Baby Zebra','Baby Elephant Seal','Baby Wombat','Baby Emu','Baby Kiwi Bird','Baby Flamingo','Cygnet (Baby Swan)','Baby Tortoise','Baby Alligator','Baby Crocodile','Baby Chameleon','Baby Iguana','Baby Frog','Baby Toad','Baby Gecko','Ring-tailed Lemur','Sifaka Lemur','Mouse Lemur','Bush Baby','PygmyPossum','Baby Mole','Baby Bat','Leveret (Baby Hare)','Baby Mole Rat','Baby Porcupine','Baby Badger','Pygmy Rabbit','Baby Seal','Baby Puffin','Owlet (Baby Owl)','Hoglet(Baby Hedgehog)','Baby Armadillo','Baby Pangolin','Baby Okapi','Baby Cheetah','Baby Ocelot','Baby Lynx','Baby Tasmanian Devil']  # from Cute Animal node
    behaviors = ["sleeping", "running", "hunting", "playing", "eating", "drinking", "grooming", "swimming", "flying", "climbing", "jumping", "stalking", "resting", "fighting", "mating", "nursing", "exploring", "hiding", "gathering"]  # from Animal Behavior node
    professions = ["chef", "wizard", "warrior", "merchant", "blacksmith", "healer", "ranger", "bard", "alchemist", "scholar", "knight", "assassin", "monk", "necromancer", "paladin", "druid", "hunter", "mage", "thief", "priest"]  # from Profession node
    races = ["elf", "dwarf", "orc", "halfling", "human", "gnome", "troll", "goblin", "fairy", "centaur", "mermaid", "dragon-kin", "tiefling", "angel", "demon", "giant", "vampire", "werewolf", "nymph", "satyr"]  # from Fantasy Race node
    clothing = {
        "fantasy": ["ornate robes", "leather armor", "chainmail", "plate armor", "mage robes", "ranger cloak", "druid vestments", "royal garments", "battle armor", "mystic robes", "elven silk", "dwarven steel armor", "assassin's garb", "priest's vestments", "tribal attire"],
        "realistic": ["business suit", "casual wear", "jeans and t-shirt", "dress", "uniform", "sportswear", "formal attire", "streetwear", "hoodie", "leather jacket", "blazer", "sweater", "coat", "shorts", "skirt"],
        "sci_fi": ["space suit", "cybernetic armor", "nanotech suit", "power armor", "environmental suit", "combat exoskeleton", "stealth suit", "hazmat suit", "neural interface suit", "quantum armor", "plasma-resistant gear", "gravity suit", "bio-enhanced armor", "energy shield suit", "phase shift armor"]
    }
    actions = ["running", "jumping", "fighting", "casting spell", "flying", "swimming", "climbing", "sneaking", "dancing", "meditating", "charging", "defending", "attacking", "healing", "crafting", "exploring", "investigating", "performing ritual", "commanding"]
    compositions = ["close-up shot", "wide angle", "birds eye view", "low angle", "portrait", "landscape", "panoramic", "macro shot", "aerial view", "profile view", "dutch angle", "over the shoulder", "establishing shot", "tracking shot", "symmetrical composition", "rule of thirds", "centered composition", "dynamic angle", "dramatic perspective", "silhouette"]
    habitats = ["forest", "desert", "mountains", "ocean", "jungle", "tundra", "savanna", "wetlands", "cave", "valley", "canyon", "beach", "volcanic region", "coral reef", "grassland", "rainforest", "arctic", "oasis", "cliff", "underground"]
    weather = ["sunny", "rainy", "stormy", "snowy", "cloudy", "foggy", "windy", "thunderstorm", "hail", "sleet", "hurricane", "tornado", "clear sky", "overcast", "misty", "drizzle", "blizzard", "sandstorm", "heat wave"]
    times = ["dawn", "sunrise", "morning", "noon", "afternoon", "dusk", "sunset", "twilight", "night", "midnight", "golden hour", "blue hour", "early morning", "late evening", "first light", "witching hour", "dead of night", "break of day", "high noon", "starlit night"]
    art_styles = ["oil painting", "digital art", "watercolor", "pencil sketch", "ink drawing", "acrylic", "pastel", "charcoal", "concept art", "illustration", "photorealistic", "impressionist", "abstract", "minimalist", "surrealist", "anime", "comic book", "fantasy art", "sci-fi art", "traditional"]
    emotions = ["happy", "sad", "angry", "peaceful", "excited", "fearful", "determined", "confused", "serene", "anxious", "confident", "melancholic", "joyful", "fierce", "calm", "passionate", "mysterious", "playful", "serious", "contemplative"]
    magical_effects = {
        "fire": ["blazing aura", "flame burst", "inferno swirl", "phoenix flames", "fire storm", "burning halo", "ember glow", "magma burst", "flame vortex", "heat wave"],
        "ice": ["frost crystals", "blizzard swirl", "ice spikes", "frozen aura", "snow storm", "crystal frost", "glacial burst", "arctic wind", "ice shield", "frozen mist"],
        "lightning": ["thunder strike", "electric arc", "storm bolt", "lightning chain", "static field", "plasma burst", "spark shower", "voltage surge", "thunder cloud", "electric storm"],
        "nature": ["vine growth", "flower bloom", "leaf storm", "root surge", "pollen cloud", "forest spirits", "natural healing", "earth tremor", "growth burst", "nature's blessing"],
        "arcane": ["mystic runes", "energy spiral", "magical circles", "arcane symbols", "power flux", "spell matrix", "ethereal glow", "mana burst", "wisdom aura", "mystic barrier"]
    }
    mythical_locations = ["crystal cave", "floating islands", "ancient temple", "enchanted forest", "dragon's lair", "wizard's tower", "fairy grove", "rainbow bridge", "underwater palace", "cloud castle", "phoenix nest", "mystic library", "forgotten ruins", "elemental sanctuary", "starlit grove", "demon realm", "celestial observatory", "ethereal gardens", "astral plane", "shadow realm"]
    artifacts = {
        "weapon": ["legendary sword", "mystic staff", "enchanted bow", "divine spear", "cursed blade", "holy mace", "ancient axe", "magical dagger", "sacred hammer", "ethereal blade"],
        "jewelry": ["power amulet", "magic ring", "mystic crown", "enchanted bracelet", "soul gem", "crystal pendant", "rune necklace", "celestial tiara", "dragon scale ring", "phoenix feather brooch"],
        "armor": ["divine shield", "mystic gauntlets", "enchanted helm", "sacred breastplate", "magical cloak", "soul armor", "crystal greaves", "celestial shield", "dragon scale mail", "phoenix plate"]
    }
    technology = {
        "weapons": ["plasma rifle", "quantum blade", "laser cannon", "ion blaster", "gravity gun", "antimatter pistol", "fusion sword", "particle beam", "sonic disruptor", "nano blade"],
        "gadgets": ["holographic display", "neural interface", "quantum computer", "energy shield", "teleporter", "cloaking device", "bio scanner", "force field", "time manipulator", "ai companion"],
        "augments": ["cybernetic arm", "neural implant", "bionic eye", "exoskeleton", "nano enhancer", "memory chip", "strength augment", "speed booster", "healing module", "stealth system"]
    }
    alien_world_elements = {
        "atmospheres": ["toxic", "breathable", "dense", "thin", "corrosive", "radioactive", "crystalline", "gaseous", "plasma", "multi-layered"],
        "terrains": ["crystalline desert", "floating islands", "liquid metal seas", "bio-luminescent forest", "gravity wells", "plasma lakes", "quantum fields", "living crystal", "void chasms", "energy plains"],
        "colors": ["purple", "emerald", "crimson", "azure", "golden", "silver", "obsidian", "prismatic", "iridescent", "phosphorescent"],
        "features": ["multiple moons", "binary suns", "ring system", "space anomaly", "wormhole", "asteroid belt", "nebula view", "aurora", "plasma storms", "quantum rifts"]
    }
    spacecraft = {
        "military": ["battlecruiser", "stealth frigate", "carrier", "destroyer", "dreadnought", "gunship", "interceptor", "warship", "assault carrier", "combat shuttle"],
        "civilian": ["passenger liner", "cargo hauler", "mining vessel", "exploration ship", "colony ship", "research vessel", "transport", "space yacht", "rescue ship", "diplomatic vessel"],
    }  # from Spacecraft node
    cinema_characters = [
        "spiderman", "batman", "hulk", "wonder woman", "superman", "iron man",
        "captain america", "thor", "black widow", "deadpool", "wolverine",
        "optimus prime", "megatron", "buzz lightyear", "woody", "shrek",
        "donkey", "puss in boots", "harley quinn", "joker", "catwoman", 
        "black panther", "doctor strange", "scarlet witch", "vision",
        "ant-man", "wasp", "thanos", "loki", "captain marvel", "star-lord",
        "gamora", "groot", "rocket raccoon", "drax", "nebula",  # Removed duplicate "venom"
        "miles morales", "ghost rider", "blade", "punisher", "daredevil",
        "jessica jones", "luke cage", "iron fist", "green goblin", "doctor octopus",
        "venom", "carnage", "mysterio", "sandman", "vulture", "electro",
        "terminator", "robocop", "predator", "alien", "indiana jones",
        "james bond", "ethan hunt", "john wick", "neo", "trinity", "morpheus",
        "luke skywalker", "darth vader", "yoda", "princess leia", "han solo",
        "chewbacca", "obi-wan kenobi", "rey", "kylo ren", "mandalorian",
        "gandalf", "frodo", "aragorn", "legolas", "gimli", "gollum", "saruman",
        "harry potter", "hermione granger", "ron weasley", "dumbledore", "voldemort",
        "jack sparrow", "davy jones", "king kong", "godzilla", "jurassic park raptor",
        "t-rex", "marty mcfly", "doc brown", "ghostbusters", "xenomorph"
    ]
    
    cartoon_characters = [
        "mickey mouse", "donald duck", "goofy", "bugs bunny", "spongebob",
        "homer simpson", "mario", "luigi", "sonic", "pikachu", "sailor moon",
        "goku", "naruto", "ash ketchum", "doraemon", "hello kitty", "popeye",
        "fred flintstone", "scooby doo", "shaggy", "tom and jerry", "pink panther",
        "garfield", "ninja turtles", "winnie the pooh", "tigger", "elsa"
    ]

    anime_styles = [
        "anime key visual", "manga panel", "anime illustration", "light novel cover",
        "anime character sheet", "manga page", "anime promotional art",
        "anime ending card", "manga splash page", "anime concept art"
    ]

    anime_characters = [
        # Character archetypes
        "tsundere", "kuudere", "yandere", "dandere", "deredere",
        "genki girl", "ojou-sama", "bishonen", "bishojo", "moe character",
        
        # Common roles
        "magical girl", "isekai protagonist", "student council president",
        "transfer student", "childhood friend", "shrine maiden", "ninja",
        "samurai warrior", "demon slayer", "monster hunter", "idol singer",
        "genius detective", "esper", "mecha pilot", "alchemist",
        
        # Fantasy/Special roles
        "summoned hero", "dragon knight", "spirit medium", "magic academy student",
        "demon lord", "celestial maiden", "guardian spirit", "beast tamer",
        "sword saint", "dark magician", "holy priestess", "mystic healer",
        
        # Modern roles
        "high school student", "club president", "sports ace", "genius programmer",
        "aspiring chef", "art prodigy", "music composer", "fashion designer"
    ]

    anime_expressions = [
        "determined expression", "gentle smile", "confident smirk", "cute pout",
        "tearful eyes", "fierce gaze", "cheerful grin", "elegant composure",
        "shocked face", "blushing cheeks", "serene look", "intense stare"
    ]

    anime_emotions = [
        "burning determination", "overflowing joy", "quiet resolve",
        "hidden sadness", "righteous anger", "pure innocence",
        "unwavering courage", "deep melancholy", "boundless enthusiasm",
        "serene tranquility", "fierce passion", "gentle kindness"
    ]

    anime_actions = [
        "charging into battle", "casting magic spell", "striking a pose",
        "running with toast in mouth", "training montage", "dramatic transformation",
        "emotional confession", "epic sword clash", "magical girl transformation",
        "dramatic entrance", "power-up sequence", "slice-of-life moment"
    ]

    anime_environments = [
        "cherry blossom avenue", "rooftop at sunset", "traditional japanese garden",
        "modern tokyo street", "magical academy", "summer festival",
        "ancient temple grounds", "futuristic city", "peaceful countryside",
        "mysterious forest", "beach during summer", "snowy mountain shrine"
    ]

    anime_effects = [
        "speed lines", "floating cherry blossoms", "magical particles",
        "glowing aura", "dramatic wind effect", "sparkling stars",
        "flowing energy", "lens flare", "emotional flowers", "power symbols",
        "dramatic shadows", "dynamic impact frames"
    ]

    anime_compositions = [
        "dynamic camera angle", "dramatic foreshortening", "dutch angle shot",
        "extreme close-up", "panoramic wide shot", "hero shot",
        "split-panel layout", "motion blur focus", "fisheye perspective"
    ]

    architecture_styles = [
        "gothic", "modern", "art deco", "baroque", "minimalist", "brutalist",
        "victorian", "classical", "renaissance", "contemporary", "futuristic",
        "industrial", "organic", "high-tech", "postmodern", "deconstructivist",
        "traditional japanese", "islamic", "greek revival", "romanesque",
        "neoclassical", "tudor", "colonial", "art nouveau", "beaux-arts",
        "rococo", "bauhaus", "mid-century modern", "neo-gothic", "byzantine",
        "modernist", "prairie style", "international style", "spanish colonial",
        "craftsman", "mediterranean", "georgian", "edwardian", "neo-futuristic",
        "sustainable", "parametric", "vernacular", "pueblo revival"
    ]

    architecture_elements = [
        "cathedral", "skyscraper", "temple", "palace", "castle", "mansion",
        "bridge", "tower", "museum", "library", "opera house", "station",
        "observatory", "pavilion", "monument", "arch", "dome", "spire",
        "courtyard", "garden", "amphitheater", "aqueduct", "basilica",
        "belvedere", "citadel", "colonnade", "conservatory", "fortress",
        "gatehouse", "greenhouse", "lighthouse", "mausoleum", "minaret",
        "monastery", "obelisk", "pagoda", "pantheon", "pyramid", "rotunda",
        "sanctuary", "terrace", "vault", "ziggurat", "acropolis", "arcade",
        "atrium", "balustrade", "buttress", "cloister", "portico"
    ]

    abstract_elements = [
        "geometric shapes", "flowing lines", "color fields", "patterns",
        "fractals", "curves", "spirals", "dots", "waves", "symmetry",
        "asymmetry", "gradients", "textures", "layers", "dimensions",
        "perspective", "depth", "movement", "rhythm", "space",
        "tessellations", "mosaics", "kaleidoscope", "interference",
        "diffraction", "refraction", "distortion", "reflection",
        "transparency", "opacity", "luminosity", "contrast", "harmony",
        "discord", "balance", "tension", "fluidity", "rigidity",
        "compression", "expansion", "intersection", "overlay", "repetition",
        "fragmentation", "convergence", "divergence", "radial patterns",
        "linear patterns", "organic patterns", "crystalline structures"
    ]

    abstract_styles = [
        "cubist", "expressionist", "constructivist", "suprematist",
        "de stijl", "abstract expressionist", "color field", "minimalist",
        "geometric abstraction", "lyrical abstraction", "op art", "kinetic art",
        "hard-edge painting", "organic abstraction", "biomorphic",
        "abstract surrealism", "abstract impressionism", "action painting",
        "tachisme", "art informel", "neo-plasticism", "orphism",
        "rayonism", "synchronism", "concrete art", "systems art",
        "process art", "color abstraction", "gestural abstraction",
        "post-painterly abstraction", "abstract illusionism", "neo-geo",
        "digital abstraction", "generative art", "glitch art",
        "abstract photography", "abstract sculpture", "light art",
        "sound art", "conceptual abstraction", "neo-expressionism"
    ]

    # Add these new class variables
    food_types = [
        "sushi", "pizza", "burger", "pasta", "steak", "salad", "soup", "dessert",
        "cake", "ice cream", "chocolate", "sandwich", "ramen", "curry", "seafood",
        "barbecue", "tacos", "pancakes", "waffles", "croissant", "bread", "pastry",
        "macarons", "cupcakes", "donuts", "fruit platter", "cheese board", "dim sum",
        "pho", "paella", "risotto", "lasagna", "sashimi", "tempura", "dumplings",
        "bibimbap", "pad thai", "butter chicken", "falafel", "shawarma", "kebab",
        "poke bowl", "ceviche", "enchiladas", "tamales", "empanadas", "spring rolls",
        "samosas", "biryani", "moussaka", "couscous", "gnocchi", "ravioli",
        "carbonara", "tiramisu", "creme brulee", "gelato", "baklava", "churros",
        "crepes", "eclairs", "mochi", "truffles", "souffles", "tarts", "pies",
        "cheesecake", "brownies", "cookies", "biscuits", "scones", "muffins"
    ]

    food_styles = [
        "gourmet", "homemade", "street food", "fine dining", "rustic", "modern",
        "traditional", "fusion", "minimalist", "artisanal", "molecular gastronomy",
        "comfort food", "haute cuisine", "bistro style", "farm-to-table", "buffet",
        "tapas", "family style", "al fresco", "prix fixe", "tasting menu",
        "casual dining", "food truck", "pop-up restaurant", "cafeteria",
        "brasserie", "trattoria", "izakaya", "gastropub", "deli", "patisserie",
        "steakhouse", "seafood restaurant", "sushi bar", "pizzeria", "cafe",
        "bakery", "food hall", "wine pairing", "seasonal menu", "organic",
        "vegan", "vegetarian", "raw food", "slow food", "fast casual"
    ]

    interior_styles = [
        "modern", "minimalist", "scandinavian", "industrial", "bohemian",
        "contemporary", "traditional", "art deco", "mid-century modern",
        "rustic", "coastal", "farmhouse", "eclectic", "japanese zen",
        "mediterranean", "victorian", "tropical", "french country", "gothic",
        "baroque", "renaissance", "neoclassical", "art nouveau", "shabby chic",
        "hollywood regency", "asian fusion", "moroccan", "southwestern",
        "colonial", "tudor", "georgian", "retro", "vintage", "steampunk",
        "urban modern", "transitional", "maximalist", "wabi-sabi", "bauhaus",
        "brutalist", "chinoiserie", "hamptons style", "lodge", "nautical",
        "provincial", "rococo", "gothic revival", "modernist", "postmodern"
    ]

    interior_spaces = [
        "minimalist living room", "modern kitchen", "luxury bathroom", "elegant dining room",
        "designer home office", "grand library", "glass conservatory", "marble entrance hall",
        "architectural loft", "high-end studio space", "penthouse interior", "walk-in closet",
        "gourmet kitchen", "spa bathroom", "meditation space", "reading nook",
        "wine cellar", "art gallery space", "greenhouse interior", "luxury pantry",
        "designer laundry room", "grand staircase", "solarium", "drawing room",
        "gallery space", "atrium", "conservatory", "great room", "foyer",
        "butler's pantry", "dressing room", "powder room", "music room", "library"
    ]

    interior_elements = [
        "designer furniture", "architectural lighting", "luxury textiles", "statement artwork",
        "decorative objects", "handwoven rugs", "custom window treatments", "architectural details",
        "built-in storage", "marble surfaces", "crystal chandeliers", "designer mirrors",
        "textured wallpaper", "accent pillows", "silk curtains", "motorized blinds",
        "floating shelves", "custom cabinetry", "stone countertops", "pendant lights",
        "parquet flooring", "coffered ceiling", "wall sconces", "track lighting",
        "designer bookcases", "marble fireplace", "brass fixtures", "glass partitions",
        "wood paneling", "stone accent wall", "designer tiles", "smart home features",
        "built-in aquarium", "indoor water feature", "designer radiators", "smart glass windows",
        "hidden storage", "mood lighting", "automated systems", "sound system"
    ]

    threed_styles = [
        "low poly", "realistic 3D", "isometric", "voxel art", "clay render",
        "wireframe", "procedural", "photorealistic 3D", "stylized 3D",
        "geometric 3D", "architectural visualization", "product visualization",
        "character modeling", "environment modeling", "hard surface modeling"
    ]

    # Add these new class variables
    halloween_elements = {
        "creatures": [
            "ghost", "skeleton", "zombie", "vampire", "werewolf", "witch",
            "black cat", "demon", "gargoyle", "grim reaper", "mummy",
            "haunted doll", "possessed puppet", "banshee", "goblin",
            "headless horseman", "phantom", "wraith", "imp", "living scarecrow",
            "ghoul", "poltergeist", "wendigo", "hellhound", "shadow creature",
            "faceless entity", "doppelganger", "changeling", "boogeyman", "revenant",
            "lich", "necromancer", "dark fairy", "night stalker", "possessed child",
            "corpse bride", "pumpkin head", "plague doctor", "shadow walker", "sin eater"
        ],
        "settings": [
            "haunted house", "graveyard", "dark forest", "abandoned church",
            "cursed castle", "foggy cemetery", "witch's cottage", "crypt",
            "dungeon", "misty moor", "haunted mansion", "dark alley",
            "abandoned asylum", "cursed village", "spooky carnival",
            "ancient tomb", "forbidden tower", "ghost town", "dark swamp",
            "haunted lighthouse", "cursed school", "abandoned hospital",
            "forgotten catacombs", "haunted theater", "cursed library",
            "abandoned mine", "witch's grove", "demon's lair", "shadow realm",
            "haunted circus", "forgotten monastery", "cursed ruins",
            "abandoned orphanage", "dark carnival", "witch's cave"
        ],
        "props": [
            "jack o'lantern", "cobwebs", "candelabra", "crystal ball",
            "spell book", "cauldron", "cursed mirror", "haunted painting",
            "old tombstone", "creepy doll", "raven", "full moon",
            "twisted trees", "carved pumpkin", "black roses", "skull",
            "ancient runes", "poison bottles", "tarot cards",
            "ouija board", "haunted music box", "bone wind chimes",
            "cursed jewelry", "witch's broom", "black candles", "dead flowers",
            "rusty chains", "broken mirrors", "ghostly photographs",
            "possessed teddy bear", "voodoo doll", "pentagram", "blood stains",
            "ancient artifacts", "cursed diary", "spirit board", "demon mask",
            "witch's herbs", "sacrificial altar", "evil eye amulet"
        ]
    }

    # Add new class variables
    influencer_types = [
        "deep cleavage fashion blogger", "curvy fitness model", "curvy travel influencer", "lifestyle blogger",
        "food critic", "curvy beauty guru", "tech reviewer", "deep cleavage wellness coach",
        "busty yoga instructor", "digital nomad", "busty streetwear model", "deep cleavage makeup artist",
        "busty personal trainer", "luxury lifestyle", "sustainable living blogger",
        "deep cleavage adventure photographer", "home decor expert", "busty fashion model"
    ]

    influencer_activities = [
        "posing", "taking selfie", "vlogging", "doing photoshoot",
        "showcasing product", "recording story", "doing unboxing",
        "creating content", "doing tutorial", "reviewing product",
        "sharing lifestyle tips", "doing workout", "traveling",
        "doing makeup tutorial", "sharing fashion tips"
    ]

    influencer_locations = [
        "luxury hotel", "infinity pool", "beach resort", "rooftop bar",
        "trendy cafe", "designer store", "yoga studio", "private jet",
        "exotic beach", "urban rooftop", "luxury apartment",
        "high-end restaurant", "fashion show", "art gallery",
        "boutique hotel", "sunset viewpoint", "luxury yacht"
    ]

    # Update theme prefixes with more cute-focused language for cute chimera
    theme_prefixes = {
        "anime": "minimalist anime artwork with clean lines of",
        "realistic": "professional studio photograph with precise lighting, ultra-sharp focus, minimalist composition of",
        "sci_fi": "sleek and refined futuristic design, premium finish, elegant technological details of",
        "fantasy": "elegant fantasy artwork with refined details of",
        "cute chimera": "adorable kawaii-style digital artwork with soft pastel colors and fluffy details of",  # Updated this line
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
        "strange_animal": "professional wildlife photograph with cinematic lighting of",  # Updated this line
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
    }

    # Add design-focused enhancement words
    enhancements = {
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

    # Add these new class variables after the existing ones
    futuristic_city_elements = {
        "architecture": [
            "towering skyscrapers", "floating buildings", "anti-gravity structures",
            "crystalline towers", "holographic billboards", "neon-lit facades", 
            "suspended walkways", "transparent domes", "energy spires",
            "vertical gardens", "quantum architecture", "plasma conduits",
            "bio-organic buildings", "cybernetic structures", "nano-tech constructs",
            "self-repairing structures", "modular megastructures", "force field protected buildings",
            "artificial intelligence hubs", "data processing centers", "environmental purification towers",
            "solar collection arrays", "hyperloop stations", "quantum computing facilities",
            "biomimetic architecture", "space elevators", "atmospheric scrubbers",
            "holographic projection centers", "energy distribution nodes", "climate control towers"
        ],
        "infrastructure": [
            "magnetic levitation trains", "flying vehicles", "teleportation hubs",
            "energy grid networks", "holographic streets", "sky bridges",
            "underground megastructures", "atmospheric processors", "fusion reactors",
            "weather control systems", "orbital elevators", "gravity tubes",
            "quantum transportation networks", "automated delivery systems", "drone highways",
            "suborbital transport loops", "matter recycling facilities", "energy harvesting grids",
            "vertical transportation pods", "antigravity public transit", "neural network hubs",
            "plasma energy conduits", "waste reclamation systems", "atmospheric filtration networks",
            "autonomous vehicle lanes", "molecular assembly plants", "smart city grids",
            "hydroponic farming towers", "quantum communication arrays", "artificial ecosystem regulators"
        ],
        "atmosphere": [
            "neon-lit", "cyberpunk", "clean tech", "eco-futuristic", "dystopian",
            "utopian", "high-tech", "bio-mechanical", "quantum powered",
            "holographic", "plasma-driven", "chrome and glass", "crystalline",
            "bioluminescent", "nano-enhanced", "augmented reality infused", "solar punk",
            "techno-organic", "hyper-connected", "artificially sustained",
            "energy saturated", "digitally overlaid", "synthetically optimized",
            "quantum stabilized", "electromagnetically charged", "fusion powered",
            "holographically augmented", "climate controlled", "pollution free",
            "technologically integrated", "AI monitored"
        ],
        "time": [
            "night", "sunset", "dawn", "dusk", "midnight", "golden hour",
            "blue hour", "neon twilight", "artificial day", "perpetual twilight",
            "quantum time", "temporal flux", "synthetic daylight", "eternal dusk",
            "programmed dawn", "digital midnight", "holographic sunset", "artificial aurora",
            "binary sunrise", "plasma noon", "crystal clear morning", "nebula night",
            "virtual daytime", "simulated evening", "matrix morning", "cyber sunset",
            "quantum nightfall", "synthetic starlight", "digital dawn", "techno twilight"
        ]
    }

    # Add Pixar-specific elements
    pixar_styles = [
        "Pixar-style 3D render", "Pixar animation style", "Pixar character design",
        "Pixar-like CGI artwork", "Pixar digital art", "Pixar concept art",
        "cute Pixar-inspired render", "adorable Pixar animation", "charming Pixar scene"
    ]

    pixar_characteristics = [
        "expressive big eyes", "cute round features", "adorable facial expression",
        "charming smile", "playful pose", "endearing personality",
        "bouncy animation style", "squash and stretch", "appealing character design",
        "soft rounded forms", "cheerful demeanor", "heartwarming expression",
        "lovable character", "whimsical design", "friendly appearance",
        "cute button nose", "chubby cheeks", "innocent look",
        "playful attitude", "gentle features", "warm personality"
    ]

    pixar_materials = [
        "soft shiny plastic", "smooth rubber", "polished metal",
        "plush fabric", "velvety texture", "glossy surface",
        "matte finish", "fuzzy material", "silky smooth surface",
        "pearlescent sheen", "sparkly details", "metallic accents",
        "translucent glow", "iridescent highlights", "subtle shimmer"
    ]

    pixar_environments = [
        "colorful toy room", "cozy kitchen", "magical bedroom",
        "charming small town", "whimsical playground", "enchanted garden",
        "friendly neighborhood", "cute cafe interior", "adorable toy store",
        "magical school", "cheerful park", "lovely backyard",
        "charming village", "delightful candy shop", "magical library"
    ]

    pixar_lighting = [
        "warm golden lighting", "soft ambient glow", "cheerful sunlight",
        "magical light rays", "cozy indoor lighting", "playful color bounce",
        "gentle rim light", "charming practical lights", "dreamy atmosphere",
        "sparkly highlights", "magical light beams", "gentle volumetric lighting"
    ]

    # Update Binet-specific elements
    binet_styles = [
        "dramatic black and white portrait", 
        "high contrast monochrome portrait",
        "elegant anthropomorphic portrait",
        "sophisticated character portrait",
        "aristocratic animal portrait",
        "regal black and white portrait",
        "distinguished monochrome portrait",
        "formal Victorian portrait",
        "noble creature portrait",
        "dramatic studio portrait"
    ]

    binet_elements = [
        "dramatic lighting", 
        "deep black shadows",
        "crisp white highlights",
        "intricate fur details",
        "photorealistic textures",
        "elegant pose",
        "dignified expression",
        "aristocratic bearing",
        "refined character",
        "extreme contrast",
        "professional studio lighting",
        "majestic presence",
        "sophisticated demeanor",
        "formal posture",
        "noble countenance"
    ]

    binet_color_accents = [
        "selective red accent", "subtle pastel pink highlight", 
        "gentle pastel blue detail", "soft pastel yellow accent",
        "muted pastel green element", "striking red element",
        "delicate pastel purple touch", "bold red accent",
        "no color accent", "no color accent", "no color accent"  # More weight for B&W
    ]

    binet_themes = [
        "dramatic noir", "vintage elegance", "classic portraiture",
        "period character", "aristocratic style", "vintage glamour",
        "historical character", "timeless elegance", "dramatic contrast"
    ]

    binet_accessories = [
        "formal black suit with silk lapels",
        "elegant Victorian waistcoat",
        "distinguished bow tie",
        "ornate cravat",
        "formal dress coat",
        "military dress uniform",
        "aristocratic attire",
        "fine tailored jacket",
        "formal evening wear",
        "sophisticated three-piece suit",
        "elegant pocket square",
        "formal white gloves",
        "ceremonial medals",
        "gold watch chain",
        "silk top hat"
    ]

    binet_backgrounds = [
        "dark dramatic backdrop", "high contrast studio backdrop",
        "deep shadow background", "moody dark setting",
        "noir style backdrop", "dramatic vignette", "classic dark studio",
        "shadowy painted backdrop", "low key studio setting"
    ]

    # Add Binet-specific whimsical activities
    binet_activities = [
        "smoking an ornate pipe", "smoking a fancy cigar", "driving a vintage car",
        "piloting an old biplane", "playing a violin", "playing a grand piano",
        "reading an ancient book", "painting on an easel", "drinking fine wine",
        "playing chess", "writing with a quill pen", "conducting an orchestra",
        "riding a penny-farthing bicycle", "sailing a wooden ship", "playing polo",
        "having afternoon tea", "playing croquet", "fencing with elegance", 
        "playing billiards", "wearing a monocle and top hat", "hunting with hounds",
        "attending an opera", "collecting butterflies", "studying star charts",
        "examining artifacts", "brewing exotic teas", "mixing alchemical potions",
        "cataloging rare books", "polishing a pocket watch", "arranging flowers",
        "writing poetry", "practicing calligraphy", "bird watching with binoculars",
        "sketching in a leather-bound journal", "playing a harpsichord",
        "examining specimens through a microscope", "sipping brandy by the fireplace",
        "playing lawn tennis", "hosting a sophisticated dinner party",
        "studying ancient maps", "collecting rare coins", "playing backgammon",
        "tasting aged whiskey", "maintaining a curiosity cabinet",
        "pressing flowers in books", "playing the cello", "practicing archery",
        "riding a horse sidesaddle", "attending a masquerade ball",
        "studying phrenology", "collecting mineral specimens", "playing bridge",
        "maintaining a greenhouse", "writing letters with sealing wax",
        "studying meteorology", "practicing taxidermy", "playing the harp",
        "collecting mechanical watches", "studying astronomy", "playing bocce",
        "maintaining a rose garden", "practicing palmistry", "playing whist",
        "collecting antique weapons", "studying entomology", "playing the organ",
        "maintaining a wine cellar", "practicing cartography", "playing shuffleboard",
        "collecting rare stamps", "studying ornithology", "playing the flute",
        "maintaining a library", "practicing numerology", "playing mahjong",
        "collecting music boxes", "studying geology", "playing the mandolin",
        "maintaining a menagerie", "practicing physiognomy", "playing dominoes",
        "collecting snuff boxes", "studying botany", "playing the dulcimer",
        "maintaining a cabinet of curiosities", "practicing mesmerism"
    ]

    # Add new class variables for Vintage Anthropomorphic theme
    vintage_anthro_professions = [
        "detective", "pastry chef", "science professor", "jazz musician", "café waiter",
        "librarian", "train conductor", "newspaper editor", "watchmaker", "tailor",
        "botanist", "antiquarian", "theater actor", "poet", "photographer",
        "cartographer", "archaeologist", "chess master", "violin maker", "astronomer",
        "apothecary", "bookbinder", "clockmaker", "cobbler", "confectioner",
        "curator", "diplomat", "etiquette teacher", "fortune teller", "governess",
        "hat maker", "inventor", "jeweler", "linguist", "naturalist",
        "opera singer", "perfumer", "philosopher", "portrait painter", "seamstress",
        "tea merchant", "toymaker", "typographer", "violin tuner", "zoologist"
    ]

    vintage_anthro_clothing = [
        "trench coat and fedora", "chef's hat and apron", "lab coat and glasses",
        "stylish suit and hat", "white shirt and black vest", "tweed jacket with elbow patches",
        "conductor's uniform", "bow tie and waistcoat", "leather apron and spectacles",
        "smoking jacket and ascot", "explorer's outfit", "opera cape and top hat",
        "morning coat and cravat", "tailcoat and white gloves", "frock coat and top hat",
        "velvet smoking robe", "military dress uniform", "academic gown and hood",
        "three-piece pinstripe suit", "silk dressing gown", "riding habit and boots",
        "artist's smock and beret", "formal evening wear", "safari outfit and pith helmet",
        "double-breasted peacoat", "monocle and pocket square", "high collar and cummerbund",
        "embroidered waistcoat", "silk cravat and ruffled shirt", "leather riding boots"
    ]

    vintage_anthro_settings = [
        "misty street corner", "Parisian bakery", "university classroom",
        "dimly lit jazz club", "mountain lodge café", "antique bookshop",
        "steam train station", "Victorian study", "clockmaker's workshop",
        "botanical garden greenhouse", "museum archive", "vintage photography studio",
        "grand opera house", "gentleman's club", "antiquarian bookshop",
        "natural history museum", "astronomical observatory", "private library",
        "curiosity shop", "perfumery", "botanical laboratory",
        "cartography office", "vintage wine cellar", "art gallery",
        "old world pharmacy", "scientific laboratory", "music conservatory",
        "historic theater", "luxury ocean liner", "grand hotel lobby",
        "ornate drawing room", "vintage apothecary",
        "crystal palace greenhouse", "mahogany-paneled study", "rare book archive",
        "steampunk workshop", "velvet-draped parlor", "vintage chess club",
        "antique map room", "gilded ballroom", "vintage printing press",
        "astronomical dome", "vintage radio station", "collectors' salon",
        "Victorian orangery", "vintage auction house", "botanical illustration studio",
        "vintage observatory", "crystal greenhouse", "antique music room",
        "vintage lecture hall", "mechanical workshop", "vintage botanical society",
        "old world library", "vintage science lab", "collectors' vault"
    ]

    vintage_anthro_props = [
        "magnifying glass", "tray of pastries", "scientific beaker",
        "musical instrument", "coffee service", "leather-bound books",
        "pocket watch", "fountain pen", "brass telescope",
        "vintage camera", "chess set", "botanical specimens",
        "crystal decanter", "gramophone", "typewriter",
        "globe", "sextant", "microscope",
        "barometer", "compass", "quill and inkwell",
        "opera glasses", "calling card case", "leather briefcase",
        "brass scales", "apothecary jars", "mechanical calculator",
        "ornate tea set", "antique maps", "specimen collection boxes",
        "brass microscope", "crystal ink bottles", "wax seal kit",
        "vintage spectacles", "brass candlesticks", "leather document case",
        "porcelain teacups", "brass measuring tools", "vintage medical instruments",
        "antique clock", "brass compass", "leather-bound journal",
        "crystal perfume bottles", "brass monocle", "vintage writing desk",
        "botanical illustrations", "brass laboratory equipment", "leather satchel",
        "vintage photographs", "brass kaleidoscope", "antique violin",
        "crystal wine glasses", "brass spyglass", "vintage walking stick",
        "mechanical pocket watch", "brass sundial", "leather map case",
        "vintage chemistry set", "brass magnifier", "antique books",
        "crystal paperweight", "brass sextant", "vintage telescope",
        "mechanical music box", "brass thermometer", "leather portfolio",
        "vintage botanical prints", "brass hydrometers", "antique fountain pens",
        "crystal prisms", "brass astrolabe", "vintage scientific instruments",
        "mechanical chronometer", "brass balance scales", "leather travel case",
        "vintage astronomical charts", "brass weather instruments", "antique desk set",
        "crystal magnifying glass", "brass drawing tools", "vintage specimen jars",
        "mechanical adding machine", "brass surveying equipment", "leather book binding",
        "vintage laboratory glassware", "antique ink wells"
    ]

    vintage_anthro_activities = [
        "smoking an ornate pipe", "smoking a fancy cigar", "driving a vintage car",
        "piloting an old biplane", "playing a violin", "playing a grand piano",
        "reading an ancient book", "painting on an easel", "drinking fine wine",
        "playing chess", "writing with a quill pen", "conducting an orchestra",
        "riding a penny-farthing bicycle", "sailing a wooden ship", "playing polo",
        "having afternoon tea", "playing croquet", "fencing with elegance",
        "examining specimens", "peering through a telescope", "mixing chemicals",
        "cataloging artifacts", "sketching botanical drawings", "developing photographs",
        "operating a printing press", "tuning a gramophone", "brewing exotic tea",
        "polishing brass instruments", "arranging flowers", "collecting butterflies",
        "studying star charts", "measuring with calipers", "binding leather books",
        "typing on a vintage typewriter", "developing daguerreotypes", "calibrating instruments",
        "conducting experiments", "recording observations", "classifying specimens",
        "archiving documents", "restoring antiques", "curating exhibitions",
        "navigating with sextant", "studying maps", "writing correspondence",
        "hosting dinner parties", "attending opera", "giving lectures",
        "hunting with hounds", "riding in horse-drawn carriages", "attending balls",
        "playing billiards", "practicing archery", "collecting antiquities",
        "studying ancient texts", "conducting séances", "brewing potions",
        "maintaining timepieces", "playing bridge", "attending scientific symposiums",
        "exploring ruins", "sketching architecture", "conducting archaeological digs",
        "studying meteorology", "practicing phrenology", "conducting botanical surveys",
        "organizing expeditions", "maintaining terrariums", "studying entomology",
        "practicing taxidermy", "conducting astronomical observations", "mixing perfumes",
        "maintaining aquariums", "studying geology", "conducting anthropological research",
        "practicing cartography", "studying ornithology", "conducting chemical analysis",
        "maintaining herbariums", "studying paleontology", "conducting marine research",
        "using a steampunk AI assistant", "operating a brass quantum computer",
        "adjusting a mechanical neural network", "calibrating a clockwork VR headset"
    ]

    # Add new Star Wars specific variables
    star_wars_characters = [
        # Existing characters
        "jedi knight", "sith lord", "bounty hunter", "rebel pilot", "imperial officer",
        "stormtrooper", "mandalorian warrior", "wookiee warrior", "twilek dancer",
        "republic senator", "smuggler", "droid", "clone trooper", "royal guard",
        "jedi master", "sith apprentice", "rebel commander", "imperial admiral",
        "moisture farmer", "pod racer", "jawa trader", "tusken raider", "hutt crime lord",
        "republic commando", "imperial inquisitor", "force user", "padawan learner",
        "republic guard", "imperial spy", "rebel spy", "cantina patron", "podracer pilot",
        
        # Adding iconic characters
        "Yoda", "Darth Vader", "Luke Skywalker", "Princess Leia", "Han Solo",
        "Obi-Wan Kenobi", "Emperor Palpatine", "Chewbacca", "R2-D2", "C-3PO",
        "Boba Fett", "Darth Maul", "Qui-Gon Jinn", "Mace Windu", "Count Dooku",
        "Padmé Amidala", "Anakin Skywalker", "General Grievous", "Jabba the Hutt",
        "Lando Calrissian", "Admiral Ackbar", "Din Djarin", "Grogu", "Ahsoka Tano",
        "Captain Rex", "Asajj Ventress", "Grand Admiral Thrawn", "Kylo Ren", "Rey",
        "Finn", "Poe Dameron", "BB-8", "General Hux", "Captain Phasma",
        "Supreme Leader Snoke", "Moff Gideon", "Cara Dune", "Kuiil", "IG-11",
        "Fennec Shand", "Cad Bane", "Grand Moff Tarkin", "Admiral Piett"
    ]

    star_wars_locations = [
        "tatooine desert", "coruscant cityscape", "death star interior", "rebel base",
        "imperial star destroyer", "mos eisley cantina", "jedi temple", "sith temple",
        "endor forest", "cloud city", "naboo palace", "geonosis arena", "kamino facility",
        "mustafar lava fields", "kashyyyk treetops", "yavin temple", "hoth ice caves",
        "jabba's palace", "imperial base", "senate chamber", "trade federation ship",
        "podrace track", "crystal cave", "sarlacc pit", "dune sea", "moisture farm",
        "imperial academy", "rebel hangar", "spice mines", "smuggler's den"
    ]

    star_wars_vehicles = [
        "x-wing fighter", "tie fighter", "millennium falcon", "star destroyer",
        "lambda shuttle", "speeder bike", "at-at walker", "at-st walker",
        "republic gunship", "jedi starfighter", "pod racer", "sand crawler",
        "imperial shuttle", "y-wing bomber", "slave one", "nebulon-b frigate",
        "imperial transport", "rebel transport", "tie interceptor", "b-wing fighter",
        "imperial landing craft", "republic cruiser", "trade federation battleship"
    ]

    star_wars_props = [
        "lightsaber", "blaster", "force pike", "thermal detonator", "holocron",
        "comlink", "energy shield", "meditation chamber", "carbonite chamber",
        "training remote", "imperial probe droid", "protocol droid", "astromech droid",
        "vibroblade", "energy bow", "force artifact", "jedi robes", "imperial uniform",
        "rebel flight suit", "stormtrooper armor", "mandalorian armor", "blast door",
        "control panel", "power generator", "tractor beam", "ion cannon"
    ]

    star_wars_effects = [
        "force lightning", "force push", "lightsaber glow", "blaster fire",
        "force shield", "force healing", "force vision", "hyperspace jump",
        "ion discharge", "laser blast", "force meditation",
        "force choke", "force projection", "saber clash", "force storm",
        "force illusion", "force barrier", "force explosion", "force wave"
    ]

    # Add Marvel-specific variables
    marvel_characters = [
        # Avengers
        "Iron Man", "Captain America", "Thor", "Hulk", "Black Widow", "Hawkeye",
        "Spider-Man", "Doctor Strange", "Black Panther", "Captain Marvel",
        "Scarlet Witch", "Vision", "Falcon", "Winter Soldier", "War Machine",
        "Ant-Man", "Wasp", "Star-Lord", "Gamora", "Drax", "Rocket Raccoon",
        "Groot", "Nebula", "Nick Fury", "Maria Hill",
        
        # Villains
        "Thanos", "Loki", "Ultron", "Red Skull", "Doctor Doom",
        "Green Goblin", "Doctor Octopus", "Venom", "Mysterio", "Killmonger",
        "Hela", "Ronan", "Vulture", "Taskmaster", "Kang the Conqueror",
        
        # X-Men
        "Wolverine", "Professor X", "Magneto", "Jean Grey", "Cyclops",
        "Storm", "Beast", "Rogue", "Gambit", "Deadpool", "Phoenix",
        
        # Supporting Characters
        "Pepper Potts", "Happy Hogan", "Jane Foster", "MJ Watson", "Ned Leeds",
        "Wong", "Shuri", "Okoye", "Agent Coulson", "Luis", "Valkyrie"
    ]

    marvel_locations = [
        "Avengers Tower", "Stark Industries", "Sanctum Sanctorum", "Wakanda",
        "Asgard", "SHIELD Helicarrier", "Xavier's School", "Quantum Realm",
        "New York City streets", "Knowhere", "Titan", "Vormir", "Kamar-Taj",
        "Dark Dimension", "Mirror Dimension", "Sokovia", "Triskelion",
        "Latveria", "Asteroid M", "Genosha", "Savage Land", "K'un-Lun",
        "Hell's Kitchen", "Oscorp Tower", "Daily Bugle", "Midtown High School"
    ]

    marvel_props = [
        "Iron Man suit", "Captain America's shield", "Mjolnir", "Infinity Gauntlet",
        "Eye of Agamotto", "Cloak of Levitation", "Vibranium suit", "Web shooters",
        "Quantum suit", "Arc reactor", "Pym particles", "Spider suit", "Falcon wings",
        "Winter Soldier arm", "War Machine armor", "Hawkeye's bow", "Black Widow's batons",
        "Star-Lord's mask", "Groot's branches", "Rocket's weapons", "Infinity Stones",
        "Ultron drones", "SHIELD badge", "Quinjet", "Helicarrier", "Milano spaceship"
    ]

    marvel_effects = [
        "repulsor blast", "magic portal", "quantum energy",
        "vibranium pulse", "web effect", "mystic arts", "infinity stone glow",
        "hulk smash impact", "nano-tech transformation", "spider-sense",
        "time stone effect", "reality warping", "power stone surge",
        "space stone portal", "mind stone beam", "soul stone aura",
        "quantum particles", "arc reactor glow", "magic runes",
        "cosmic energy", "gamma radiation", "mutant power effect"
    ]

    # Add these new class variables at the top of the class with other theme-specific lists
    steampunk_elements = {
        "machines": [
            "brass clockwork", "steam engine", "copper boiler", "mechanical gears",
            "pneumatic tubes", "bronze automaton", "steam-powered robot", "gear train",
            "pressure gauge", "brass telescope", "mechanical calculator", "steam turbine",
            "copper pipes", "brass valves", "mechanical wings", "steam-powered armor"
        ],
        "accessories": [
            "top hat", "brass goggles", "leather gloves", "pocket watch",
            "mechanical monocle", "brass compass", "leather tool belt", "gear brooch",
            "brass buttons", "leather boots", "mechanical arm", "steam pack"
        ],
        "environments": [
            "Victorian industrial district",
            "clockwork metropolis",
            "steam-powered city",
            "brass and copper cityscape",
            "mechanical tower complex",
            "industrial revolution London",
            "gear-driven urban center",
            "steam-powered factory district",
            "mechanical engineering district",
            "Victorian mechanical city",
            "steampunk transportation hub",
            "industrial age marketplace",
            "mechanical innovation quarter",
            "steam-powered residential district"
        ]
    }

    post_apocalyptic_elements = {
        "environments": [
            "ruined cityscape", "abandoned highway", "overgrown mall",
            "destroyed factory", "wasteland settlement", "radiation zone",
            "underground bunker", "scrapyard city", "desert outpost"
        ],
        "props": [
            "rusty vehicle", "broken machinery", "salvaged weapons",
            "makeshift shelter", "scavenged supplies", "survival gear",
            "radiation suit", "gas mask", "improvised tools"
        ],
        "atmosphere": [
            "toxic fog", "nuclear sunset", "acid rain", "dust storm",
            "radioactive haze", "perpetual twilight", "burning sky"
        ]
    }

    # Update the underwater_elements dictionary with more civilization-focused elements
    underwater_elements = {
        "structures": [
            "massive crystal dome city", "bioluminescent skyscraper towers", "ancient atlantean palace",
            "underwater metropolis", "submerged floating city", "coral-integrated architecture",
            "pressurized glass habitation domes", "kelp forest residential district", "pearl-encrusted temples",
            "hydrothermal vent power stations", "aqua-glass transit tunnels", "oceanic research facilities",
            "underwater market squares", "marine cultivation farms", "tidal energy generators",
            "submerged archaeological ruins", "deep sea mining operations", "bioluminescent street networks"
        ],
        "life_forms": [
            "merfolk citizens", "aquatic humanoid traders", "bioluminescent sea people",
            "evolved marine colonists", "deep sea civilization dwellers", "underwater society members",
            "aquatic hybrid inhabitants", "marine-adapted humans", "oceanic cultural groups",
            "sea-dwelling communities", "underwater tribal societies", "advanced aquatic species"
        ],
        "technology": [
            "water pressure shields", "marine filtration systems", "underwater transport pods",
            "aquatic communication networks", "bubble-tech living spaces", "coral-based computers",
            "tidal energy collectors", "pressure-resistant infrastructure", "underwater farming systems",
            "marine waste recyclers", "aqua-plasma lighting", "oceanic defense systems",
            "underwater transportation grid", "marine oxygen generators", "aquatic food production"
        ],
        "cultural_elements": [
            "underwater market bazaars", "marine cultural centers", "aquatic education hubs",
            "deep sea entertainment venues", "oceanic art galleries", "submerged sports arenas",
            "marine religious temples", "underwater musical pavilions", "aquatic gathering spaces",
            "deep sea gardens", "marine meditation sanctuaries", "underwater theatrical stages"
        ]
    }

    microscopic_elements = {
        "structures": [
            "cell membrane", "molecular chain", "protein complex",
            "DNA helix", "mitochondria", "cellular matrix",
            "crystal lattice", "atomic structure", "quantum pattern"
        ],
        "processes": [
            "cell division", "protein synthesis", "electron transfer",
            "molecular binding", "neural firing", "quantum tunneling",
            "crystallization", "cellular repair", "atomic interaction"
        ],
        "environments": [
            "cellular landscape", "molecular forest", "quantum realm",
            "crystalline matrix", "neural network", "protein maze",
            "atomic void", "cellular city", "quantum field"
        ]
    }

    bio_organic_elements = {
        "structures": [
            "living metal", "organic circuitry", "neural interface",
            "bio-mechanical heart", "synthetic tissue", "living machine",
            "organic processor", "bio-digital hybrid", "living architecture"
        ],
        "processes": [
            "bio-synthesis", "organic computing", "neural integration",
            "tissue-metal fusion", "bio-digital transfer", "organic power generation",
            "synthetic evolution", "bio-mechanical growth"
        ],
        "aesthetics": [
            "bioluminescent circuits", "pulsing veins", "living metal skin",
            "organic crystal growth", "flowing circuitry", "breathing machinery",
            "synthetic nervous system", "bio-mechanical symmetry"
        ]
    }

    # Add this animal families dictionary at the class level
    animal_families = {
        'felines': ['cat', 'lion', 'tiger', 'leopard', 'cheetah', 'jaguar', 'lynx', 'ocelot', 'caracal', 'cougar', 'panther', 'serval', 'bobcat', 'snow leopard', 'clouded leopard', 'margay', 'fishing cat', 'puma', 'sand cat', 'jaguarundi', 'asian golden cat', 'black-footed cat', 'pallas cat', 'rusty-spotted cat', 'oncilla'],
        'canines': ['dog', 'wolf', 'fox', 'coyote', 'dingo', 'jackal', 'fennec fox', 'arctic fox', 'red wolf', 'african wild dog', 'maned wolf', 'golden retriever', 'puppy', 'german shepherd', 'husky', 'labrador', 'border collie', 'beagle', 'rottweiler', 'doberman', 'great dane', 'bulldog', 'poodle', 'corgi', 'dalmatian', 'swift fox', 'kit fox', 'gray fox', 'bush dog', 'raccoon dog'],
        'bears': ['bear', 'panda', 'grizzly bear', 'polar bear', 'black bear', 'sun bear', 'spectacled bear', 'sloth bear', 'brown bear', 'asiatic black bear', 'kodiak bear', 'cave bear', 'giant panda', 'red panda', 'moon bear', 'syrian brown bear', 'tibetan blue bear', 'formosan black bear', 'himalayan brown bear', 'gobi bear'],
        'primates': ['monkey', 'gorilla', 'chimpanzee', 'orangutan', 'baboon', 'gibbon', 'lemur', 'mandrill', 'capuchin', 'marmoset', 'tamarin', 'macaque', 'bonobo', 'siamang', 'proboscis monkey', 'howler monkey', 'spider monkey', 'langur', 'colobus', 'tarsier', 'galago', 'loris', 'indri', 'sifaka', 'aye-aye', 'vervet monkey', 'woolly monkey', 'squirrel monkey', 'mangabey', 'guereza'],
        'rodents': ['rat', 'mouse', 'squirrel', 'chipmunk', 'hamster', 'beaver', 'capybara', 'gerbil', 'guinea pig', 'porcupine', 'chinchilla', 'marmot', 'prairie dog', 'dormouse', 'agouti', 'degu', 'jerboa', 'kangaroo rat', 'lemming', 'vole', 'woodchuck', 'groundhog', 'flying squirrel', 'nutria', 'viscacha', 'gopher', 'springhare', 'coypu', 'hutia', 'zokors'],
        'birds': ['eagle', 'hawk', 'owl', 'penguin', 'parrot', 'peacock', 'swan', 'duck', 'goose', 'falcon', 'hummingbird', 'toucan', 'macaw', 'flamingo', 'crane', 'pelican', 'albatross', 'raven', 'crow', 'cardinal', 'blue jay', 'woodpecker', 'kingfisher', 'ostrich', 'emu', 'kiwi', 'condor', 'vulture', 'seagull', 'puffin', 'stork', 'heron', 'ibis', 'sparrow', 'finch', 'canary', 'cockatoo', 'parakeet', 'lorikeet', 'quail'],
        'reptiles': ['crocodile', 'alligator', 'snake', 'lizard', 'gecko', 'tortoise', 'iguana', 'chameleon', 'komodo dragon', 'python', 'cobra', 'viper', 'turtle', 'monitor lizard', 'bearded dragon', 'anaconda', 'boa constrictor', 'rattlesnake', 'mamba', 'skink', 'gila monster', 'tuatara', 'caiman', 'basilisk', 'anole', 'tegu', 'agama', 'worm lizard', 'amphisbaena', 'horned lizard'],
        'marine': ['dolphin', 'shark', 'octopus', 'squid', 'jellyfish', 'crab', 'lobster', 'seal', 'sea lion', 'walrus', 'orca', 'narwhal', 'manatee', 'sea turtle', 'seahorse', 'ray', 'starfish', 'eel', 'anglerfish', 'clownfish', 'barracuda', 'moray eel', 'hammerhead shark', 'great white shark', 'manta ray', 'sea urchin', 'sea cucumber', 'sea anemone', 'coral', 'dugong', 'blue whale', 'sea dragon', 'lionfish', 'pufferfish', 'swordfish'],
        'marsupials': ['kangaroo', 'koala', 'wallaby', 'tasmanian devil', 'wombat', 'quokka', 'opossum', 'numbat', 'bandicoot', 'sugar glider', 'quoll', 'potoroo', 'bettong', 'bilby', 'pademelon', 'tree kangaroo', 'cuscus', 'antechinus', 'dunnart', 'phascogale', 'ringtail possum', 'brushtail possum', 'glider possum', 'rock wallaby', 'swamp wallaby'],
        'insects': ['butterfly', 'beetle', 'ant', 'bee', 'wasp', 'dragonfly', 'mantis', 'grasshopper', 'cricket', 'ladybug', 'moth', 'cicada', 'firefly', 'scarab', 'caterpillar', 'centipede', 'millipede', 'scorpion', 'spider', 'termite', 'cockroach', 'earwig', 'stick insect', 'leaf insect', 'walking stick', 'praying mantis', 'assassin bug', 'water strider', 'giant water bug', 'jewel beetle', 'stag beetle', 'rhinoceros beetle', 'hercules beetle', 'atlas beetle', 'dung beetle'],
        'ungulates': ['horse', 'deer', 'elephant', 'giraffe', 'zebra', 'rhinoceros', 'hippopotamus', 'moose', 'elk', 'antelope', 'gazelle', 'bison', 'buffalo', 'camel', 'llama', 'alpaca', 'wildebeest', 'impala', 'kudu', 'oryx', 'eland', 'gemsbok', 'nyala', 'okapi', 'tapir', 'wild boar', 'warthog', 'peccary', 'mountain goat', 'bighorn sheep', 'ibex', 'chamois', 'markhor', 'tahr', 'muskox'],
    }

    # Add new character-specific costume and theme lists for Binet
    binet_character_themes = [
        "superhero", "pirate captain", "military general", "noir detective",
        "steampunk explorer", "royal commander", "distinguished admiral",
        "mysterious vigilante", "elegant aristocrat", "scholarly professor",
        "master spy", "legendary warrior", "noble diplomat", "master assassin",
        "distinguished inventor"
    ]

    binet_costume_elements = [
        "armored tactical suit with insignia", 
        "weathered pirate coat with brass buttons",
        "high-tech combat armor with glowing details",
        "leather trench coat with metal accents",
        "military uniform with medals and badges",
        "steampunk outfit with brass gadgets",
        "combat suit with battle damage",
        "formal military dress with gold trim",
        "tactical gear with utility pouches",
        "ornate battle armor with royal emblems",
        "advanced combat suit with power cores",
        "distinguished uniform with rank insignias",
        "masked vigilante suit with cape",
        "battle-worn armor with war medals",
        "high-tech stealth suit with sensors"
    ]

    binet_props_and_weapons = [
        "vibranium shield with battle scars",
        "ornate cutlass and flintlock pistol",
        "high-tech energy weapons",
        "dual katanas with glowing runes",
        "ceremonial sword and pistol",
        "advanced combat rifle",
        "ancient mystical weapons",
        "tactical combat gear",
        "experimental energy shield",
        "legendary blade with inscriptions",
        "modified sniper rifle",
        "enchanted battle staff",
        "custom twin pistols",
        "advanced targeting system",
        "mystical combat artifacts"
    ]

    # Add new contemporary themes for Binet
    binet_contemporary_themes = [
        "street artist", "graffiti master", "sports champion", "football player",
        "basketball star", "rugby athlete", "urban artist", "street performer",
        "modern athlete", "team captain", "sports legend", "urban warrior",
        "street style icon", "modern rebel", "contemporary artist"
    ]

    # Add sports and urban style accessories
    binet_sports_gear = [
        "professional sports jersey with team number",
        "rugby uniform with national emblem",
        "football kit with captain's armband",
        "athletic performance wear",
        "sports team uniform with sponsor logos",
        "professional athlete gear",
        "team captain uniform",
        "championship medal and jersey",
        "sports competition outfit",
        "national team colors",
        "victory celebration gear",
        "professional league uniform",
        "team spirit wear",
        "championship winner outfit",
        "sports star signature gear"
    ]

    # Add urban and artistic elements
    binet_urban_elements = [
        "street art backdrop",
        "urban graffiti elements",
        "spray paint effects",
        "abstract paint splashes",
        "dynamic paint strokes",
        "artistic ink splatters",
        "contemporary art patterns",
        "modern street art style",
        "urban decay textures",
        "artistic chaos elements",
        "modern art composition",
        "street culture symbols",
        "urban typography",
        "modern artistic flair",
        "contemporary design elements"
    ]

    # Add celebration and victory elements
    binet_celebration_elements = [
        "victory confetti shower",
        "championship celebration",
        "triumphant moment",
        "winning atmosphere",
        "crowd celebration effects",
        "stadium victory lights",
        "championship trophy presentation",
        "victory roar moment",
        "triumphant stance",
        "celebration fireworks",
        "victory lap scene",
        "champion's spotlight",
        "winning team celebration",
        "sports arena triumph",
        "victory parade atmosphere"
    ]

    # Add color scheme options for Binet theme
    binet_color_schemes = [
        "vibrant red and black with glowing effects",
        "luxury gold and white with soft highlights",
        "racing yellow with dynamic motion blur",
        "elegant emerald green with butterfly accents",
        "royal blue with chrome details",
        "neon colors with urban glow",
        "pastel tones with ethereal lighting",
        "rich burgundy with golden accents",
        "racing team colors with metallic finish",
        "designer brand colors with premium finish",
        "medical white with professional blue accents",
        "sports team official colors",
        "luxury fashion brand palette",
        "racing livery colors",
        "urban street art colors"
    ]

    # Add new contemporary clothing options for Binet theme
    binet_clothing = {
        "luxury": [
            "designer white fur coat with Chanel brooch",
            "black silk turtleneck with gold chain",
            "cream cashmere sweater with designer logo",
            "tailored Italian suit with pocket square",
            "luxury leather jacket with gold buttons",
            "designer blazer with silk scarf",
            "high-end trench coat with belt",
            "premium wool coat with fur collar",
            "silk blouse with pearl buttons",
            "velvet smoking jacket with satin lapels"
        ],
        "sports": [
            "professional racing suit with team logos",
            "official team jersey with captain's armband",
            "premium athletic wear with sponsor patches",
            "high-tech sports uniform with number",
            "professional rugby kit with team crest",
            "custom racing gear with sponsors",
            "championship team uniform with medals",
            "elite sports attire with team colors",
            "professional athlete uniform with patches",
            "custom sports jersey with name and number"
        ],
        "professional": [
            "white medical coat with stethoscope",
            "pilot's uniform with golden wings",
            "chef's whites with professional badges",
            "business suit with silk tie",
            "military dress uniform with medals",
            "police uniform with badges",
            "firefighter gear with patches",
            "judge's robes with ceremonial collar",
            "professor's blazer with elbow patches",
            "architect's professional attire with tools"
        ]
    }

    # First, add these new style elements for Marvel comics
    marvel_comic_styles = [
        "classic Marvel comic book art style", "vintage comic book illustration",
        "Silver Age Marvel comics style", "retro comic book art",
        "Jack Kirby style comic art", "Steve Ditko art style",
        "John Romita Sr comic style", "classic comic book panel",
        "Bronze Age Marvel style", "Golden Age comic art"
    ]

    marvel_comic_effects = [
        "Ben-Day dots pattern", "halftone shading effect", "comic ink lines",
        "bold comic book colors", "dramatic comic shadows", "action lines",
        "comic book crosshatching", "vintage print texture", "comic book color halftones",
        "dramatic comic perspective", "bold outline style", "comic book speed lines"
    ]

    marvel_comic_compositions = [
        "dynamic comic book pose", "heroic comic book stance",
        "dramatic comic panel layout", "action-packed comic scene",
        "classic comic book cover composition", "epic comic splash page",
        "dramatic comic book angle", "vintage comic framing"
    ]

    # Add these new class variables after the vintage_anthro_elements

    peaky_blinders_animals = [
        "lion", "wolf", "tiger", "bear", "gorilla", "bull", "horse", "stag",
        "fox", "dog", "goat", "ram", "leopard", "panther", "eagle", "hawk",
        "owl", "raven", "boar", "elk", "moose", "badger", "otter", "lynx",
        "wildcat", "hound", "mastiff", "doberman", "german shepherd", "great dane"
    ]

    peaky_blinders_outfits = [
        "sharp three-piece tweed suit with newsboy cap",
        "tailored pinstripe suit with flat cap",
        "wool herringbone suit with leather gloves",
        "custom-fitted waistcoat and pocket watch",
        "dark wool overcoat with matching cap",
        "tailored suit with suspenders and cap",
        "formal dress suit with bow tie and cap",
        "vintage three-piece suit with gold chain",
        "bespoke suit with silk tie and cap",
        "leather-trimmed suit with matching hat",
        "double-breasted suit with pocket square",
        "formal evening wear with top hat",
        "hunting tweed with leather boots",
        "racing suit with driving gloves",
        "military-inspired suit with medals"
    ]

    peaky_blinders_accessories = [
        "holding a large cigar",
        "with a silver pocket watch",
        "carrying a wooden cane",
        "with a glass of whiskey",
        "holding a vintage pistol",
        "with a leather briefcase",
        "smoking a carved pipe",
        "with brass knuckles",
        "holding a crystal tumbler",
        "with a leather holster",
        "carrying a walking stick",
        "with a gold cigarette case",
        "holding a glass of red wine",
        "with an ornate flask",
        "carrying a leather document case"
    ]

    peaky_blinders_settings = [
        "dimly lit gentleman's club",
        "smoky Birmingham pub",
        "vintage car garage",
        "industrial factory office",
        "private betting parlor",
        "luxurious study room",
        "historic train station",
        "cobblestone street corner",
        "underground speakeasy",
        "private members club",
        "horse racing track",
        "vintage wine cellar",
        "old boxing gym",
        "historic auction house",
        "private gambling den"
    ]

    peaky_blinders_furniture = [
        "luxurious leather armchair",
        "vintage wooden desk",
        "antique poker table",
        "carved mahogany bar",
        "velvet chesterfield sofa",
        "brass-trimmed writing desk",
        "vintage billiards table",
        "leather wingback chair",
        "ornate wooden throne",
        "antique smoking chair",
        "carved oak table",
        "vintage betting counter",
        "leather office chair",
        "brass-studded armchair",
        "antique card table"
    ]

    peaky_blinders_props = [
        "vintage car from the early 1920s",
        "antique pocket watch collection",
        "crystal whiskey decanters",
        "vintage firearms display",
        "old racing newspapers",
        "betting slips and ledgers",
        "carved wooden boxes",
        "vintage radio set",
        "old telephone",
        "brass table lamps",
        "antique cash register",
        "vintage photographs",
        "old boxing gloves",
        "horse racing trophies",
        "vintage playing cards"
    ]

    peaky_blinders_atmospheres = [
        "smoky atmosphere with golden lighting",
        "dim gaslight with long shadows",
        "morning fog with streaks of sunlight",
        "warm lamplight with tobacco haze",
        "dramatic evening shadows",
        "moody industrial lighting",
        "soft vintage lighting",
        "dramatic window light",
        "atmospheric street lighting",
        "candlelit ambiance",
        "dusty sunbeams",
        "rainy evening atmosphere",
        "misty morning light",
        "dramatic spotlight effect",
        "industrial steam and smoke"
    ]

    # Add these new Christmas-specific class variables after other theme elements:

    christmas_elements = {
        "characters": [
            "Santa Claus", "Mrs Claus", "reindeer", "elf workshop helper", 
            "snowman", "gingerbread man", "toy soldier", "nutcracker",
            "polar bear", "arctic fox", "penguin", "christmas angel",
            "wise men", "shepherd", "frost giant", "ice queen",
            "christmas fairy", "jack frost", "krampus", "winter spirit"
        ],
        "settings": [
            "Santa's workshop", "magical toy factory", "christmas village",
            "winter wonderland", "enchanted forest", "gingerbread town",
            "north pole", "cozy fireplace", "decorated living room",
            "snowy town square", "christmas market", "ice palace",
            "reindeer stables", "elves' dormitory", "candy cane forest",
            "christmas tree farm", "frozen lake", "magical ice cave",
            "decorated town hall", "festive shopping street"
        ],
        "decorations": [
            "christmas tree", "twinkling lights", "festive garland",
            "hanging stockings", "candy canes", "christmas wreaths",
            "glass ornaments", "tinsel", "mistletoe", "holly berries",
            "poinsettias", "advent calendar", "christmas star",
            "festive ribbons", "snow globes", "icicle lights",
            "nutcracker collection", "gingerbread house", "christmas village display",
            "wrapped presents"
        ],
        "magical_effects": [
            "sparkling snow", "northern lights", "magical stardust",
            "twinkling fairy lights", "glowing ornaments", "christmas magic",
            "festive sparkles", "magical gift wrap", "enchanted snowfall",
            "glowing christmas star", "magical tinsel", "santa's magic",
            "reindeer flight trails", "frosty window patterns", "candy cane magic",
            "christmas bell chimes", "magical gift ribbon", "festive glitter"
        ],
        "activities": [
            "opening presents", "decorating tree", "building snowman",
            "baking cookies", "singing carols", "wrapping gifts",
            "sledding", "ice skating", "making snow angels",
            "drinking hot cocoa", "hanging stockings", "reading christmas stories",
            "writing to santa", "feeding reindeer", "making gingerbread houses",
            "christmas shopping", "caroling", "attending christmas feast"
        ],
        "weather": [
            "gentle snowfall", "swirling snowflakes", "winter storm",
            "magical blizzard", "christmas eve snow", "frost patterns",
            "icy wind", "crystal clear winter night", "misty winter morning",
            "perfect christmas snow", "sparkling frost", "winter wonderland snow"
        ],
        "foods": [
            "christmas cookies", "gingerbread", "candy canes",
            "hot cocoa", "christmas pudding", "roast turkey",
            "fruit cake", "christmas ham", "mince pies",
            "mulled wine", "eggnog", "christmas chocolates",
            "roasted chestnuts", "sugar plums", "yule log cake",
            "christmas dinner", "festive treats", "decorated cupcakes"
        ]
    }

    christmas_styles = [
        "cozy christmas illustration", "vintage christmas card",
        "magical christmas scene", "festive digital art",
        "traditional christmas painting", "whimsical christmas art",
        "classic christmas illustration", "modern christmas design",
        "nostalgic christmas artwork", "cheerful christmas cartoon",
        "elegant christmas rendering", "heartwarming christmas scene"
    ]

    christmas_moods = [
        "magical", "joyful", "festive", "cozy", "nostalgic",
        "whimsical", "heartwarming", "cheerful", "peaceful",
        "enchanting", "merry", "traditional", "jolly", "celebratory"
    ]

    @classmethod
    def INPUT_TYPES(s):
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
                custom_subject="", use_custom_subject="no",  # Add these parameters
                include_subject="yes", include_action="yes", 
                include_environment="yes", include_style="yes",
                include_effects="yes", enhancement_level="moderate",
                enhancement_focus="detail"):
        
        # Create a mapping between new and old theme names
        theme_mapping = {
            "🎨 Abstract": "abstract",
            "🎌 Anime": "anime",
            "📺 Animation Cartoon": "cartoon",
            "🏛️ Architectural": "architecture",
            "🖼️ Binet Surreal": "binet",
            "🧬 Bio-Organic Technology": "bio_organic", 
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
        }

        # Convert new theme name to old theme name for internal processing
        internal_theme = theme_mapping.get(theme, theme)

        if randomize == "enable":
            seed = random.randint(0, 0xffffffffffffffff) if seed == 0 else seed
            random.seed(seed)

        # For random theme, pick a random theme except "random" itself
        if internal_theme == "random":
            available_themes = [t for t in self.theme_prefixes.keys() if t != "random"]
            internal_theme = random.choice(available_themes)

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

        if internal_theme == "abstract":
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
                        )
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
                        "((professional studio lighting)), ((sharp focus)), "
                        "((photorealistic detail)), ((cinematic framing)), "
                        "8k resolution" + color_emphasis
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