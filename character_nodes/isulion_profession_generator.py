import random

class IsulionProfessionGenerator:
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
        professions = [
            "chef", "wizard", "warrior", "merchant", "scholar", "artist",
            "blacksmith", "alchemist", "hunter", "healer", "guard", "noble",
            "farmer", "sailor", "explorer", "musician", "dancer", "priest",
            "actor", "tour guide", "florist", "cake decorator", "zookeeper",
            "ski instructor", "software developer", "nurse practitioner", "doctor",
            "physician", "information security analyst", "truck driver", "teacher",
            "firefighter", "police officer", "lawyer"
        ]
        return (random.choice(professions),) 