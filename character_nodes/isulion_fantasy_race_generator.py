import random

class IsulionFantasyRaceGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, seed=0):
        random.seed(seed)
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
        return (random.choice(races),) 