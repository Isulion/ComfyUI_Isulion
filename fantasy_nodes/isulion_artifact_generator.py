import random

class IsulionArtifactGenerator:
    artifacts = {
        "weapon": [
            "legendary sword", "mystic staff", "enchanted bow", "divine spear",
            "dragon slayer blade", "phoenix feather wand", "thunder hammer",
            "frost axe", "soul reaver", "starforged blade", "crystal dagger",
            "void staff", "light bringer", "shadow blade"
        ],
        "jewelry": [
            "power amulet", "magic ring", "crystal crown", "soul gem",
            "dragon heart pendant", "phoenix eye necklace", "moonstone ring",
            "sunfire crown", "starlight tiara", "void crystal", "eternity band",
            "wisdom pendant", "fate's circlet", "dream catcher"
        ],
        "tool": [
            "seeing glass", "teleport stone", "wisdom scroll", "healing chalice",
            "truth mirror", "fate dice", "levitation boots", "cloak of shadows",
            "bag of holding", "time turner", "memory crystal", "dreamcatcher",
            "compass of desires", "book of secrets"
        ],
        "relic": [
            "ancient tablet", "dragon scale", "phoenix feather", "unicorn horn",
            "mermaid's tear", "giant's tooth", "fairy dust", "demon's heart",
            "angel's feather", "dragon's eye", "witch's grimoire", "wizard's orb",
            "elemental crystal", "void shard"
        ]
    }

    @classmethod
    def INPUT_TYPES(s):
        all_artifacts = [item for sublist in s.artifacts.values() for item in sublist]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "artifact": (all_artifacts,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "type": (["any", "weapon", "jewelry", "tool", "relic"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("artifact", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, randomize, artifact, seed=0, type="any"):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            if type != "any" and type in self.artifacts:
                artifact = random.choice(self.artifacts[type])
            else:
                all_artifacts = [item for sublist in self.artifacts.values() for item in sublist]
                artifact = random.choice(all_artifacts)
        
        return (artifact, seed) 