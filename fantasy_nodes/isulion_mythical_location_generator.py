import random

class IsulionMythicalLocationGenerator:
    locations = [
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
                "location": (s.locations,),
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
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            location = random.choice(self.locations)
        
        return (location, seed) 