import random

class IsulionFantasyRaceGenerator:
    races = [
        "elf", "dwarf", "orc", "halfling", "gnome", "fairy",
        "dragon-born", "tiefling", "angel", "demon", "merfolk",
        "centaur", "satyr", "nymph", "giant", "goblin",
        "vampire", "werewolf", "phoenix", "unicorn", "griffin",
        "minotaur", "harpy", "mermaid", "siren", "dryad",
        "elemental", "golem", "chimera", "sphinx", "pegasus",
        "troll", "ogre", "pixie", "sprite", "banshee",
        "wraith", "ghost", "lich", "djinn", "ifrit",
        "sylph", "undine", "kitsune", "tanuki", "yokai",
        "wendigo", "skinwalker", "changeling", "doppelganger", "shapeshifter"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "race": (s.races,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("race", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, randomize, race, seed=0):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            race = random.choice(self.races)
        
        return (race, seed) 