from ..base_selector import SimpleSelectorNode


class IsulionArtifactGenerator(SimpleSelectorNode):
    POOLS = {
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
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "artifact": (s._pool_for(),),
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
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            artifact = rng.choice(self._pool_for(type))

        return (artifact, seed)
