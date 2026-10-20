from ..base_selector import SimpleSelectorNode


class Isulion_AnimalBehaviorGenerator(SimpleSelectorNode):
    POOL = [
        'Hunting', 'Sleeping', 'Playing', 'Flying', 'Swimming', 'Running',
        'Walking', 'Eating', 'Drinking', 'Grooming', 'Nesting', 'Perching',
        'Climbing', 'Jumping', 'Diving', 'Stalking', 'Resting', 'Foraging',
        'Grazing', 'Prowling', 'Pouncing', 'Soaring', 'Gliding', 'Hovering',
        'Fishing', 'Basking', 'Burrowing', 'Hibernating', 'Migrating',
        'Mating', 'Nurturing', 'Teaching', 'Fighting', 'Defending',
        'Exploring', 'Hiding', 'Camouflaging', 'Gathering', 'Building',
        'Communicating'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "behavior": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("behavior", "seed",)
    FUNCTION = "generate_behavior"
    CATEGORY = "Art/Styles"

    def generate_behavior(self, randomize: str, seed: int, behavior: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            behavior = rng.choice(self._pool_for())

        return (f"{behavior}", seed)
