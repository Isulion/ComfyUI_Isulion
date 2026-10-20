from ..base_selector import SimpleSelectorNode


class IsulionFantasyRaceGenerator(SimpleSelectorNode):
    POOL = [
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
                "race": (s.POOL,),
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
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            race = rng.choice(self._pool_for())

        return (race, seed)
