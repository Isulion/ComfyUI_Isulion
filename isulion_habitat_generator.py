import random
from nodes import NODE_CLASS_MAPPINGS

class Isulion_HabitatGenerator:
    habitats = [
        'Jungle', 'Rainforest', 'Savanna', 'Desert', 'Arctic Tundra', 'Ocean', 'Coral Reef',
        'Mountain Range', 'Alpine Forest', 'Grassland', 'Wetland', 'Mangrove Swamp',
        'Deciduous Forest', 'Coniferous Forest', 'Rocky Shore', 'Sandy Beach', 'Cave System',
        'River Valley', 'Lake Shore', 'Bamboo Forest', 'Salt Marsh', 'Kelp Forest',
        'Volcanic Region', 'Coastal Cliff', 'Prairie', 'Steppe', 'Taiga', 'Deep Ocean',
        'Shallow Reef', 'Underground Cave', 'Hot Spring', 'Oasis', 'Canyon', 'Delta',
        'Estuary', 'Fjord', 'Glacier', 'Ice Sheet', 'Island', 'Peninsula'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "habitat": (cls.habitats,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("habitat", "seed",)
    FUNCTION = "generate_habitat"
    CATEGORY = "Art/Styles"

    def generate_habitat(self, randomize, seed, habitat):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            habitat = random.choice(self.habitats)

        return (f"{habitat}", seed)

# Remove NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS from here