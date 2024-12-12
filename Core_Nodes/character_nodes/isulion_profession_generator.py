import random

class IsulionProfessionGenerator:
    professions = [
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
                "profession": (s.professions,),
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
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            profession = random.choice(self.professions)
        
        return (profession, seed) 