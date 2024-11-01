import random
from ...utils.common import handle_seed

class IsulionMegaPromptGenerator:
    # Reuse all the existing lists/dictionaries from other nodes
    animals = ['Dog','Cat','Horse','Cow','Chicken','Pig','Sheep','Goat','Lion','Tiger','Elephant','Bear','Wolf','Fox','Deer','Rabbit','Kangaroo','Giraffe','Zebra','Monkey','Chimpanzee','Gorilla','Orangutan','Panda','Koala','Hippopotamus','Rhinoceros','Crocodile','Alligator','Eagle','Hawk','Falcon','Owl','Penguin','Dolphin','Whale','Shark','Octopus','Squid','Jellyfish','Crab','Lobster','Clownfish','Sea Turtle','Frog','Toad','Snake','Lizard','Gecko','Tortoise','Camel','Donkey','Bat','Rat','Mouse','Squirrel','Chipmunk','Porcupine','Hedgehog','Skunk','Raccoon','Otter','Seal','Walrus','Polar Bear','Grizzly Bear','Cheetah','Leopard','Jaguar','Antelope','Buffalo','Bison','Moose','Reindeer','Mole','Platypus','Echidna','Parrot','Peacock','Swan','Duck','Goose','Turkey','Flamingo','Pelican','Seagull','Sparrow','Pigeon','Crow','Magpie','Woodpecker','Hummingbird','Butterfly','Bee','Ant','Spider','Scorpion','Worm','Snail','Slug']  # from Animal node
    cute_animals = ["kitten", "puppy", "baby fox", "baby panda", "baby penguin", "baby seal", "baby rabbit", "baby deer", "baby elephant", "baby giraffe", "baby koala", "baby monkey", "baby owl", "baby hedgehog", "baby hamster", "baby duckling", "baby chick", "baby tiger", "baby lion", "baby polar bear"]  # from Cute Animal node
    behaviors = ["sleeping", "running", "hunting", "playing", "eating", "drinking", "grooming", "nesting", "swimming", "flying", "climbing", "jumping", "stalking", "resting", "fighting", "mating", "nursing", "exploring", "hiding", "gathering"]  # from Animal Behavior node
    professions = ["chef", "wizard", "warrior", "merchant", "blacksmith", "healer", "ranger", "bard", "alchemist", "scholar", "knight", "assassin", "monk", "necromancer", "paladin", "druid", "hunter", "mage", "thief", "priest"]  # from Profession node
    races = ["elf", "dwarf", "orc", "halfling", "human", "gnome", "troll", "goblin", "fairy", "centaur", "mermaid", "dragon-kin", "tiefling", "angel", "demon", "giant", "vampire", "werewolf", "nymph", "satyr"]  # from Fantasy Race node
    clothing = {
        "fantasy": ["ornate robes", "leather armor", "chainmail", "plate armor", "mage robes", "ranger cloak", "druid vestments", "royal garments", "battle armor", "mystic robes", "elven silk", "dwarven steel armor", "assassin's garb", "priest's vestments", "tribal attire"],
        "modern": ["business suit", "casual wear", "jeans and t-shirt", "dress", "uniform", "sportswear", "formal attire", "streetwear", "hoodie", "leather jacket", "blazer", "sweater", "coat", "shorts", "skirt"],
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

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "theme": (["fantasy", "sci_fi", "modern", "mixed"], {"default": "fantasy"}),
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
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("prompt", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, theme, complexity, randomize, seed=0, 
                include_subject="yes", include_action="yes", 
                include_environment="yes", include_style="yes",
                include_effects="yes"):
        if randomize == "enable":
            seed = handle_seed(seed)
        
        components = []

        # Subject generation
        if include_subject == "yes":
            if theme == "fantasy":
                race = random.choice(self.races)
                profession = random.choice(self.professions)
                clothing = random.choice(self.clothing["fantasy"])
                components.append(f"{race} {profession} wearing {clothing}")
            elif theme == "sci_fi":
                tech = random.choice(self.technology["augments"])
                clothing = random.choice(self.clothing["sci_fi"])
                components.append(f"futuristic character with {tech} wearing {clothing}")
            else:  # modern or mixed
                if random.choice([True, False]):
                    animal = random.choice(self.cute_animals if random.random() < 0.3 else self.animals)
                    behavior = random.choice(self.behaviors)
                    components.append(f"{animal} {behavior}")
                else:
                    profession = random.choice(self.professions)
                    clothing = random.choice(self.clothing["modern"])
                    components.append(f"{profession} wearing {clothing}")

        # Action and composition
        if include_action == "yes":
            action = random.choice(self.actions)
            composition = random.choice(self.compositions)
            components.append(f"{action}, {composition}")

        # Environment
        if include_environment == "yes":
            if theme == "fantasy":
                location = random.choice(self.mythical_locations)
                weather_cond = random.choice(self.weather)
                time = random.choice(self.times)
                components.append(f"in a {location} during {weather_cond} {time}")
            elif theme == "sci_fi":
                atmos = random.choice(self.alien_world_elements["atmospheres"])
                terrain = random.choice(self.alien_world_elements["terrains"])
                feature = random.choice(self.alien_world_elements["features"])
                components.append(f"on an alien world with {atmos} atmosphere, {terrain}, and {feature}")
            else:
                habitat = random.choice(self.habitats)
                weather_cond = random.choice(self.weather)
                time = random.choice(self.times)
                components.append(f"in a {habitat} during {weather_cond} {time}")

        # Style and mood
        if include_style == "yes":
            art_style = random.choice(self.art_styles)
            emotion = random.choice(self.emotions)
            components.append(f"{art_style} with {emotion} mood")

        # Special effects
        if include_effects == "yes":
            if theme == "fantasy":
                effect = random.choice(self.magical_effects["fire"])  # Randomly choose effect type
                artifact = random.choice(self.artifacts["weapon"])  # Randomly choose artifact type
                components.append(f"with {effect} and {artifact}")
            elif theme == "sci_fi":
                tech = random.choice(self.technology["weapons"])  # Randomly choose tech type
                ship = random.choice(self.spacecraft["military"])  # Randomly choose ship type
                components.append(f"with {tech} and {ship} in background")

        # Adjust detail level based on complexity
        if complexity == "simple":
            components = components[:3]
        elif complexity == "complex":
            # Add extra details based on theme
            if theme == "fantasy":
                extra_effect = random.choice(self.magical_effects["ice"])
                components.append(f"additional {extra_effect}")
            elif theme == "sci_fi":
                extra_tech = random.choice(self.technology["gadgets"])
                components.append(f"additional {extra_tech}")

        prompt = ", ".join(components)
        return (prompt, seed) 