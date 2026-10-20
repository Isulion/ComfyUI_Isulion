from ..base_selector import SimpleSelectorNode


class IsulionMythicalLocationGenerator(SimpleSelectorNode):
    POOL = [
        "crystal cave", "floating islands", "ancient temple", "enchanted forest",
        "dragon's lair", "wizard's tower", "fairy grove", "rainbow bridge",
        "underwater palace", "cloud castle", "phoenix nest", "mystic library",
        "forgotten ruins", "elemental sanctuary", "starlit grove", "demon realm",
        "celestial observatory", "ethereal gardens", "astral plane", "shadow realm",
        "elven citadel", "dwarven halls", "dragon's peak", "mermaid lagoon",
        "phoenix sanctuary", "unicorn glade", "goblin market", "witch's cottage",
        "giant's stronghold", "fae court", "crystal spires", "void gates",
        "ancient battleground", "sacred grove", "cursed castle", "magic academy"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "location": (s.POOL,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("location", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, randomize, location, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            location = rng.choice(self._pool_for())

        return (location, seed)
