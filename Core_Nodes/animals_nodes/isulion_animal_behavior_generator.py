import random

class Isulion_AnimalBehaviorGenerator:
    behaviors = [
        'Hunting', 'Sleeping', 'Playing', 'Flying', 'Swimming', 'Running',
        'Walking', 'Eating', 'Drinking', 'Grooming', 'Nesting', 'Perching',
        'Climbing', 'Jumping', 'Diving', 'Stalking', 'Resting', 'Foraging',
        'Grazing', 'Prowling', 'Pouncing', 'Soaring', 'Gliding', 'Hovering',
        'Fishing', 'Basking', 'Burrowing', 'Hibernating', 'Migrating',
        'Mating', 'Nurturing', 'Teaching', 'Fighting', 'Defending',
        'Exploring', 'Hiding', 'Camouflaging', 'Gathering', 'Building',
        'Communicating'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "behavior": (cls.behaviors,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("behavior", "seed",)
    FUNCTION = "generate_behavior"
    CATEGORY = "Art/Styles"

    def generate_behavior(self, randomize: str, seed: int, behavior: str) -> tuple:
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            behavior = random.choice(self.behaviors)

        return (f"{behavior}", seed)
