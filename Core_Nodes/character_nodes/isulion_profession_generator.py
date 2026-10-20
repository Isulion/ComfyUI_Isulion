from ..base_selector import SimpleSelectorNode


class IsulionProfessionGenerator(SimpleSelectorNode):
    POOL = [
        "chef", "wizard", "warrior", "merchant", "scholar", "artist",
        "blacksmith", "alchemist", "hunter", "healer", "guard", "noble",
        "farmer", "sailor", "explorer", "musician", "dancer", "priest",
        "actor", "tour guide", "florist", "cake decorator", "zookeeper",
        "ski instructor", "software developer", "nurse practitioner", "doctor",
        "physician", "information security analyst", "truck driver", "teacher",
        "firefighter", "police officer", "lawyer", "engineer", "pilot",
        "astronaut", "archaeologist", "detective", "librarian", "architect"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "profession": (s.POOL,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("profession", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, randomize, profession, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            profession = rng.choice(self._pool_for())

        return (profession, seed)
