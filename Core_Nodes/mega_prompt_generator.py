import random

class IsulionMegaPromptGenerator:
    # Reuse all the existing lists/dictionaries from other nodes
    animals = ['Dog','Cat','Horse','Cow','Chicken','Pig','Sheep','Goat','Lion','Tiger','Elephant','Bear','Wolf','Fox','Deer','Rabbit','Kangaroo','Giraffe','Zebra','Monkey','Chimpanzee','Gorilla','Orangutan','Panda','Koala','Hippopotamus','Rhinoceros','Crocodile','Alligator','Eagle','Hawk','Falcon','Owl','Penguin','Dolphin','Whale','Shark','Octopus','Squid','Jellyfish','Crab','Lobster','Clownfish','Sea Turtle','Frog','Toad','Snake','Lizard','Gecko','Tortoise','Camel','Donkey','Bat','Rat','Mouse','Squirrel','Chipmunk','Porcupine','Hedgehog','Skunk','Raccoon','Otter','Seal','Walrus','Polar Bear','Grizzly Bear','Cheetah','Leopard','Jaguar','Antelope','Buffalo','Bison','Moose','Reindeer','Mole','Platypus','Echidna','Parrot','Peacock','Swan','Duck','Goose','Turkey','Flamingo','Pelican','Seagull','Sparrow','Pigeon','Crow','Magpie','Woodpecker','Hummingbird','Butterfly','Bee','Ant','Spider','Scorpion','Worm','Snail','Slug']  # from Animal node
    cute_animals = ['Red Panda','Koala','Fennec Fox','Pygmy Marmoset','Quokka','Sea Otter','Harp Seal Pup','Panda Cub','Penguin Chick','Hedgehog','Axolotl','Sloth','Rabbit','Kitten','Puppy','Meerkat','Sugar Glider','Chinchilla','Slow Loris','Hamster','Red Fox Kit','Lamb','Piglet','Duckling','Pygmy Hippo','Baby Giraffe','Baby Alpaca','Otter Pup','Corgi Puppy','Golden Retriever Puppy','Seal Pup','Snow Leopard Cub','Tiger Cub','Lion Cub','Baby Gorilla','Baby Orangutan','Pygmy Goat','Fawn (Baby Deer)','Ferret','Platypus','Kangaroo Joey','Wallaby','Dik-Dik','Serval Kitten','Caracal Kitten','Clouded Leopard Cub','Red Squirrel','Chipmunk','Prairie Dog','Arctic Fox','Polar Bear Cub','Bottlenose Dolphin Calf','Beluga Whale Calf','Manatee Calf','Baby Skunk','Raccoon Kit','Baby Opossum','Baby Echidna (Puggle)','Baby Tapir','GiantPanda Cub','Baby Hippo','Baby Rhino','Baby Zebra','Baby Elephant Seal','Baby Wombat','Baby Emu','Baby Kiwi Bird','Baby Flamingo','Cygnet (Baby Swan)','Baby Tortoise','Baby Alligator','Baby Crocodile','Baby Chameleon','Baby Iguana','Baby Frog','Baby Toad','Baby Gecko','Ring-tailed Lemur','Sifaka Lemur','Mouse Lemur','Bush Baby','PygmyPossum','Baby Mole','Baby Bat','Leveret (Baby Hare)','Baby Mole Rat','Baby Porcupine','Baby Badger','Pygmy Rabbit','Baby Seal','Baby Puffin','Owlet (Baby Owl)','Hoglet(Baby Hedgehog)','Baby Armadillo','Baby Pangolin','Baby Okapi','Baby Cheetah','Baby Ocelot','Baby Lynx','Baby Tasmanian Devil']  # from Cute Animal node
    behaviors = ["sleeping", "running", "hunting", "playing", "eating", "drinking", "grooming", "swimming", "flying", "climbing", "jumping", "stalking", "resting", "fighting", "mating", "nursing", "exploring", "hiding", "gathering"]  # from Animal Behavior node
    professions = ["chef", "wizard", "warrior", "merchant", "blacksmith", "healer", "ranger", "bard", "alchemist", "scholar", "knight", "assassin", "monk", "necromancer", "paladin", "druid", "hunter", "mage", "thief", "priest"]  # from Profession node
    races = ["elf", "dwarf", "orc", "halfling", "human", "gnome", "troll", "goblin", "fairy", "centaur", "mermaid", "dragon-kin", "tiefling", "angel", "demon", "giant", "vampire", "werewolf", "nymph", "satyr"]  # from Fantasy Race node
    clothing = {
        "fantasy": ["ornate robes", "leather armor", "chainmail", "plate armor", "mage robes", "ranger cloak", "druid vestments", "royal garments", "battle armor", "mystic robes", "elven silk", "dwarven steel armor", "assassin's garb", "priest's vestments", "tribal attire"],
        "realistic": ["business suit", "casual wear", "jeans and t-shirt", "dress", "uniform", "sportswear", "formal attire", "streetwear", "hoodie", "leather jacket", "blazer", "sweater", "coat", "shorts", "skirt"],
        "sci_fi": ["space suit", "cybernetic armor", "nanotech suit", "power armor", "environmental suit", "combat exoskeleton", "stealth suit", "hazmat suit", "neural interface suit", "quantum armor", "plasma-resistant gear", "gravity suit", "bio-enhanced armor", "energy shield suit", "phase shift armor"]
    }
    actions = ["running", "jumping", "fighting", "casting spell", "flying", "swimming", "climbing", "sneaking", "dancing", "meditating", "charging", "defending", "attacking", "healing", "crafting", "exploring", "investigating", "performing ritual", "transforming", "commanding"]
    compositions = ["close-up shot", "wide angle", "birds eye view", "low angle", "portrait", "landscape", "panoramic", "macro shot", "aerial view", "profile view", "dutch angle", "over the shoulder", "establishing shot", "tracking shot", "symmetrical composition", "rule of thirds", "centered composition", "dynamic angle", "dramatic perspective", "silhouette"]
    habitats = ["forest", "desert", "mountains", "ocean", "jungle", "tundra", "savanna", "wetlands", "cave", "valley", "canyon", "beach", "volcanic region", "coral reef", "grassland", "rainforest", "arctic", "oasis", "cliff", "underground"]
    weather = ["sunny", "rainy", "stormy", "snowy", "cloudy", "foggy", "windy", "thunderstorm", "hail", "sleet", "hurricane", "tornado", "clear sky", "overcast", "misty", "drizzle", "blizzard", "sandstorm", "heat wave", "lightning storm"]
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
        "gamora", "groot", "rocket raccoon", "drax", "nebula", "venom",
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

    anime_characters = [
        "schoolgirl", "ninja", "samurai", "mecha pilot", "magical girl", 
        "shrine maiden", "demon slayer", "alchemist", "spirit", "yokai",
        "shinobi", "ronin", "sensei", "student", "idol", "witch", "summoner",
        "warrior", "priestess", "hero", "villain", "anti-hero", "guardian",
        "assassin", "swordmaster", "dragon rider", "beast tamer"
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
        "living room", "kitchen", "bedroom", "bathroom", "dining room",
        "home office", "library", "conservatory", "entrance hall", "loft",
        "studio apartment", "penthouse", "master suite", "walk-in closet",
        "game room", "home theater", "sunroom", "reading nook", "wine cellar",
        "gym", "spa bathroom", "meditation room", "craft room", "music room",
        "greenhouse", "mudroom", "pantry", "laundry room", "powder room",
        "breakfast nook", "man cave", "she shed", "nursery", "playroom",
        "guest room", "attic", "basement", "garage", "pool house", "solarium",
        "observatory", "billiard room", "drawing room", "great room", "foyer",
        "gallery", "study", "butler's pantry", "dressing room"
    ]

    interior_elements = [
        "furniture", "lighting", "textiles", "artwork", "plants",
        "decorative objects", "rugs", "window treatments", "architectural details",
        "storage solutions", "seating", "tables", "mirrors", "wallpaper",
        "throw pillows", "curtains", "blinds", "shelving", "cabinets",
        "countertops", "flooring", "ceiling fixtures", "wall sconces",
        "pendant lights", "chandeliers", "track lighting", "bookcases",
        "armchairs", "sofas", "ottomans", "coffee tables", "side tables",
        "dining tables", "beds", "dressers", "nightstands", "vanities",
        "console tables", "bar carts", "room dividers", "sculptures",
        "paintings", "photographs", "tapestries", "vases", "candleholders",
        "clocks", "fireplaces", "fountains", "area rugs", "carpets",
        "hardwood floors", "tile work", "crown molding", "wainscoting",
        "built-ins", "exposed beams", "archways", "columns", "french doors",
        "skylights", "bay windows", "stained glass", "indoor fountains"
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
        "fashion blogger", "curvy fitness model", "curvy travel influencer", "lifestyle blogger",
        "food critic", "curvy beauty guru", "tech reviewer", "deep cleavage wellness coach",
        "busty yoga instructor", "digital nomad", "busty streetwear model", "makeup artist",
        "busty personal trainer", "luxury lifestyle", "sustainable living blogger",
        "adventure photographer", "home decor expert", "fashion model"
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

    # Update theme prefixes with more design-focused language
    theme_prefixes = {
        "anime": "minimalist anime artwork with clean lines of",
        "realistic": "professional studio photograph with precise lighting, ultra-sharp focus, minimalist composition of",
        "sci_fi": "sleek and refined futuristic design, premium finish, elegant technological details of",
        "fantasy": "elegant fantasy artwork with refined details of",
        "cute chimera": "clean and polished digital art with smooth gradients of",
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
        "strange_animal": "premium studio photograph with architectural precision of",
        "futuristic_city": "ultra-modern architectural visualization with premium materials of",
        "pixar": "highly detailed Pixar-style 3D render with clean geometry and appealing design of",
        "binet": "minimalist surreal fine art photograph with pristine studio lighting of",
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
        "Pixar-style 3D render", "Pixar animation", "Pixar character design",
        "Pixar-like CGI", "Pixar digital art", "Pixar concept art"
    ]

    pixar_characteristics = [
        "expressive eyes", "squash and stretch animation", "exaggerated features",
        "clean geometry", "soft lighting", "subsurface scattering",
        "playful design", "appealing shapes", "rounded forms", "polished surfaces",
        "vibrant colors", "subtle textures", "dynamic poses", "emotional expression",
        "charming details", "whimsical elements"
    ]

    pixar_materials = [
        "glossy plastic", "soft rubber", "brushed metal", "plush fabric",
        "smooth ceramic", "polished wood", "shiny chrome", "matte finish",
        "translucent material", "reflective surface", "velvet texture",
        "metallic sheen", "pearlescent coating"
    ]

    # Add Binet-specific elements
    binet_styles = [
        "minimalist surreal photograph", "elegant surreal composition",
        "dreamlike studio photograph", "conceptual fine art photograph",
        "surreal fashion photograph", "artistic portrait photograph"
    ]

    binet_elements = [
        "floating objects", "levitating elements", "suspended in air",
        "defying gravity", "geometric composition", "clean lines",
        "perfect symmetry", "elegant minimalism", "surreal arrangement",
        "dreamlike composition", "ethereal atmosphere", "pristine white background"
    ]

    binet_subjects = [
        "elegant woman", "fashion model", "ballet dancer", "contemporary dancer",
        "graceful figure", "minimalist portrait", "artistic nude",
        "sculptural pose", "contorted figure", "geometric form"
    ]

    binet_poses = [
        "sculptural pose", "geometric stance", "floating in space",
        "suspended in air", "defying gravity", "elegant contortion",
        "minimalist gesture", "surreal position", "balanced composition",
        "artistic arrangement"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "theme": ([
                    "Essential Realistic",
                    "Futuristic Sci-Fi",
                    "Studio Cinema",
                    "Enchanted Fantasy",
                    "Fusion Cute Animals",
                    "Animation Cartoon",
                    "Anime",
                    "Architectural",
                    "Abstract",
                    "Culinary",
                    "Spaces Interior",
                    "Dimension 3D",
                    "Ethereal Halloween",
                    "Lifestyle Instagram",
                    "Chimera Strange Animals",
                    "Metropolis Futuristic City",
                    "Pixar Animation",
                    "Binet Surreal",
                    "Dynamic Random"
                ], {"default": "Essential"}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
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
                include_subject="yes", include_action="yes", 
                include_environment="yes", include_style="yes",
                include_effects="yes", enhancement_level="moderate",
                enhancement_focus="detail"):
        
        # Create a mapping between new and old theme names
        theme_mapping = {
            "Essential Realistic": "realistic",
            "Futuristic Sci-Fi": "sci_fi",
            "Studio Cinema": "cinema",
            "Enchanted Fantasy": "fantasy",
            "Fusion Cute Animals": "cute chimera",
            "Animation Cartoon": "cartoon",
            "Anime": "anime",
            "Architectural": "architecture",
            "Abstract": "abstract",
            "Culinary": "food",
            "Spaces Interior": "interior",
            "Dimension 3D": "3D",
            "Ethereal Halloween": "halloween",
            "Lifestyle Instagram": "instagram",
            "Chimera Strange Animals": "strange_animal",
            "Metropolis Futuristic City": "futuristic_city",
            "Pixar Animation": "pixar",
            "Binet Surreal": "binet",
            "Dynamic Random": "random"
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
            if internal_theme == "futuristic_city":
                # Select main architectural element
                architecture = random.choice(self.futuristic_city_elements["architecture"])
                # Select infrastructure
                infrastructure = random.choice(self.futuristic_city_elements["infrastructure"])
                # Select atmosphere
                atmosphere = random.choice(self.futuristic_city_elements["atmosphere"])
                # Select time
                time = random.choice(self.futuristic_city_elements["time"])
                
                subject_text = f"cinematic wide shot of a {atmosphere} futuristic megacity with {architecture} and {infrastructure}, during {time}, ultra detailed cityscape, shallow depth of field, sharp focus, 8k"

            elif internal_theme == "strange_animal":
                # Define animal families to avoid similar combinations
                animal_families = {
                    'felines': ['cat', 'lion', 'tiger', 'leopard', 'cheetah', 'jaguar', 'lynx', 'ocelot', 'caracal', 'cougar', 'panther', 'serval', 'bobcat', 'snow leopard', 'clouded leopard'],
                    'canines': ['dog', 'wolf', 'fox', 'coyote', 'dingo', 'jackal', 'fennec fox', 'arctic fox', 'red wolf', 'african wild dog', 'maned wolf'],
                    'bears': ['bear', 'panda', 'grizzly bear', 'polar bear', 'black bear', 'sun bear', 'spectacled bear', 'sloth bear', 'brown bear', 'asiatic black bear'],
                    'primates': ['monkey', 'gorilla', 'chimpanzee', 'orangutan', 'baboon', 'gibbon', 'lemur', 'mandrill', 'capuchin', 'marmoset', 'tamarin', 'macaque', 'bonobo', 'siamang'],
                    'rodents': ['rat', 'mouse', 'squirrel', 'chipmunk', 'hamster', 'beaver', 'capybara', 'gerbil', 'guinea pig', 'porcupine', 'chinchilla', 'marmot', 'prairie dog', 'dormouse'],
                    'birds': ['eagle', 'hawk', 'owl', 'penguin', 'parrot', 'peacock', 'swan', 'duck', 'goose', 'falcon', 'hummingbird', 'toucan', 'macaw', 'flamingo', 'crane', 'pelican', 'albatross', 'raven', 'crow', 'cardinal'],
                    'reptiles': ['crocodile', 'alligator', 'snake', 'lizard', 'gecko', 'tortoise', 'iguana', 'chameleon', 'komodo dragon', 'python', 'cobra', 'viper', 'turtle', 'monitor lizard', 'bearded dragon', 'anaconda'],
                    'marine': ['dolphin', 'whale', 'shark', 'octopus', 'squid', 'jellyfish', 'crab', 'lobster', 'seal', 'sea lion', 'walrus', 'orca', 'narwhal', 'manatee', 'sea turtle', 'seahorse', 'ray', 'starfish', 'eel', 'anglerfish'],
                    'marsupials': ['kangaroo', 'koala', 'wallaby', 'tasmanian devil', 'wombat', 'quokka', 'opossum', 'numbat', 'bandicoot', 'sugar glider'],
                    'insects': ['butterfly', 'beetle', 'ant', 'bee', 'wasp', 'dragonfly', 'mantis', 'grasshopper', 'cricket', 'ladybug', 'moth', 'cicada', 'firefly', 'scarab'],
                    'ungulates': ['horse', 'deer', 'elephant', 'giraffe', 'zebra', 'rhinoceros', 'hippopotamus', 'moose', 'elk', 'antelope', 'gazelle', 'bison', 'buffalo', 'camel', 'llama', 'alpaca'],
                }

                def get_animal_family(animal):
                    animal_lower = animal.lower()
                    for family, members in animal_families.items():
                        if any(member in animal_lower for member in members):
                            return family
                    return None

                # Get a cute head animal and remove baby-related words
                max_attempts = 20
                while max_attempts > 0:
                    head = random.choice(self.cute_animals)
                    head = head.lower().replace('baby ', '').replace('cub', '').replace('puppy', '').replace('kitten', '').replace('kit', '')
                    head = head.title()
                    
                    body = random.choice(self.animals)
                    
                    # Check if they're from different families
                    head_family = get_animal_family(head)
                    body_family = get_animal_family(body)
                    
                    if head_family != body_family or head_family is None or body_family is None:
                        break
                        
                    max_attempts -= 1
                
                subject_text = f"a complex raw photograph of an intricated chimerical fantastical creature with ((the body of a {body})) and ((the head of a {head})), bokeh background, cinematic lighting, shallow depth of field, 35mm wide angle lens, sharp focus, cinematic film still, dynamic angle, Photography, 8k, masterfully detailed"

            elif internal_theme == "fantasy":
                # New specific handling for fantasy theme
                if random.random() < 0.3:  # 30% chance for magical creature
                    race = random.choice(self.races)
                    profession = random.choice(self.professions)
                    clothing = random.choice(self.clothing["fantasy"])
                    subject_text = f"{race} {profession} wearing {clothing}"
                else:  # 70% chance for character
                    profession = random.choice(self.professions)
                    race = random.choice(self.races)
                    artifact = random.choice(self.artifacts["weapon"])
                    clothing = random.choice(self.clothing["fantasy"])
                    subject_text = f"{race} {profession} wielding {artifact}, wearing {clothing}"
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
                character = random.choice(self.cartoon_characters)
                action = random.choice(self.actions)
                subject_text = f"{character} {action}"
            elif internal_theme == "cute chimera":
                # Modified chimera creation to mix normal and cute animals
                if random.random() < 0.5:
                    # Mix cute head with normal body
                    head = random.choice(self.cute_animals)
                    body = random.choice(self.animals)
                    subject_text = f"cute hybrid creature with {head} head and {body} body"
                else:
                    # Mix normal head with cute body
                    head = random.choice(self.animals)
                    body = random.choice(self.cute_animals)
                    subject_text = f"cute hybrid creature with {head} head and {body} body"
                
                behavior = random.choice(self.behaviors)
                subject_text += f", {behavior}"
            elif internal_theme == "cinema":
                # Add proper cinema character handling
                character = random.choice(self.cinema_characters)
                action = random.choice(self.actions)
                subject_text = f"{character} {action}"
            elif internal_theme == "anime":
                character = random.choice(self.anime_characters)
                action = random.choice(self.actions)
                subject_text = f"{character} {action}"
            elif internal_theme == "architecture":
                style = random.choice(self.architecture_styles)
                element = random.choice(self.architecture_elements)
                subject_text = f"{style} {element}"
            elif internal_theme == "sci_fi":
                if random.random() < 0.6:  # 60% chance for character
                    tech = random.choice(self.technology["augments"])
                    clothing = random.choice(self.clothing["sci_fi"])
                    subject_text = f"futuristic character with {tech} wearing {clothing}"
                else:  # 40% chance for spacecraft/tech
                    ship = random.choice(self.spacecraft["military"])
                    tech = random.choice(self.technology["weapons"])
                    subject_text = f"advanced {ship} equipped with {tech}"
            elif internal_theme == "food":
                food = random.choice(self.food_types)
                style = random.choice(self.food_styles)
                subject_text = f"{style} {food}"
            elif internal_theme == "interior":
                style = random.choice(self.interior_styles)
                space = random.choice(self.interior_spaces)
                element = random.choice(self.interior_elements)
                subject_text = f"{style} {space} with {element}"
            elif internal_theme == "3D":
                style = random.choice(self.threed_styles)
                if random.random() < 0.5:
                    subject = random.choice(self.architecture_elements)
                else:
                    options = (self.technology["gadgets"] + 
                             [f"{race} character" for race in self.races])
                    subject = random.choice(options)
                subject_text = f"{style} {subject}"
            elif internal_theme == "halloween":
                creature = random.choice(self.halloween_elements["creatures"])
                prop = random.choice(self.halloween_elements["props"])
                subject_text = f"{creature} with {prop}"
            elif internal_theme == "instagram":
                influencer = random.choice(self.influencer_types)
                activity = random.choice(self.influencer_activities)
                subject_text = f"beautiful {influencer} {activity}"
            elif internal_theme == "realistic":  # Changed from else to explicit theme
                if random.random() < 0.7:  # 70% chance for human subject
                    profession = random.choice(self.professions)
                    clothing = random.choice(self.clothing["realistic"])
                    pose = random.choice([
                        "portrait", "candid shot", "environmental portrait",
                        "profile shot", "three-quarter view", "full body shot"
                    ])
                    lighting = random.choice([
                        "natural lighting", "studio lighting", "golden hour lighting",
                        "dramatic lighting", "soft lighting", "window lighting"
                    ])
                    subject_text = f"professional {pose} photograph of {profession} wearing {clothing}, {lighting}, shallow depth of field, sharp focus, 8k"
                else:  # 30% chance for nature/animal
                    subject = random.choice([
                        f"wildlife photograph of {random.choice(self.animals)} {random.choice(self.behaviors)}",
                        f"landscape photograph of {random.choice(self.habitats)}",
                        f"macro photograph of {random.choice(['flowers', 'insects', 'water droplets', 'leaves', 'crystals'])}",
                        f"architectural photograph of {random.choice(self.architecture_elements)}"
                    ])
                    subject_text = f"professional {subject}, high detail, sharp focus, 8k"
            elif internal_theme == "pixar":
                # Generate Pixar-style subject
                style = random.choice(self.pixar_styles)
                character_trait = random.choice(self.pixar_characteristics)
                material = random.choice(self.pixar_materials)
                
                if random.random() < 0.5:  # 50% chance for character
                    character = random.choice(self.cartoon_characters)
                    subject_text = f"{style} of {character} with {character_trait}, made of {material}, ultra detailed 3D model, octane render, soft lighting, subsurface scattering, 8k"
                else:  # 50% chance for object/scene
                    object_or_scene = random.choice([
                        "toy", "lamp", "robot", "vehicle", "household object",
                        "kitchen appliance", "desk item", "garden tool",
                        "musical instrument", "sports equipment"
                    ])
                    subject_text = f"{style} of a charming {object_or_scene} with {character_trait}, made of {material}, ultra detailed 3D model, octane render, soft lighting, subsurface scattering, 8k"
            elif internal_theme == "binet":
                style = random.choice(self.binet_styles)
                element = random.choice(self.binet_elements)
                subject = random.choice(self.binet_subjects)
                pose = random.choice(self.binet_poses)
                
                subject_text = f"{style} of {subject} in {pose}, {element}, pure white background, ultra clean composition, perfect studio lighting, minimalist elegance, ultra sharp focus, medium format photography, pristine quality, 8k"
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
                components.append(effects_text)
            else:  # realistic or mixed
                if random.choice([True, False]):
                    effect = random.choice(self.magical_effects["nature"])
                    effects_text = f"with {effect}"
                else:
                    art = random.choice(self.artifacts["jewelry"])
                    effects_text = f"with {art}"
            components.append(effects_text)

        # Adjust detail level based on complexity
        if complexity == "simple":
            components = components[:3]
        elif complexity == "complex":
            if internal_theme == "fantasy":
                extra_effect = random.choice(self.magical_effects["ice"])
                effects_text += f", additional {extra_effect}"
                components.append(f"additional {extra_effect}")
            elif internal_theme == "sci_fi":
                extra_tech = random.choice(self.technology["gadgets"])
                effects_text += f", additional {extra_tech}"
                components.append(f"additional {extra_tech}")

        prompt = ", ".join(components)

        # Add enhancement
        if enhancement_level in self.enhancements[enhancement_focus]:
            enhancement = random.choice(self.enhancements[enhancement_focus][enhancement_level])
            prompt = f"{prompt}, {enhancement}"
            effects_text = f"{effects_text}, {enhancement}"

        return (prompt, subject_text, action_text, environment_text, style_text, effects_text, seed)