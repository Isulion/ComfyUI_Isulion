from ..base_selector import SimpleSelectorNode


class IsulionEpochGenerator(SimpleSelectorNode):
    POOL = [
        "Ancient Egypt", "Ancient Greece", "Roman Empire", "Middle Ages",
        "Renaissance", "Industrial Revolution", "Victorian Era", "Roaring Twenties",
        "Modern Era", "Digital Age", "Bronze Age", "Iron Age", "Stone Age",
        "Byzantine Empire", "Ming Dynasty", "Edo Period", "Colonial Period",
        "Belle Époque", "Art Deco Period", "Space Age", "Information Age",
        "Medieval Japan", "Viking Age", "Golden Age of Piracy", "Wild West",
        "Prehistoric Times", "Age of Enlightenment", "Age of Exploration",
        "Classical Antiquity", "Dark Ages", "Age of Discovery",
        "Baroque Period", "Gothic Era", "Romantic Period", "Jazz Age",
        "Post-Modern Era", "Cyberpunk Future", "Steampunk Era"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "epoch": (s.POOL,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("epoch", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, randomize, epoch, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            epoch = rng.choice(self._pool_for())

        return (epoch, seed)
