from ..base_selector import SimpleSelectorNode


class Isulion_HabitatGenerator(SimpleSelectorNode):
    POOL = [
        'Jungle', 'Rainforest', 'Savanna', 'Desert', 'Arctic Tundra', 'Ocean', 'Coral Reef',
        'Mountain Range', 'Alpine Forest', 'Grassland', 'Wetland', 'Mangrove Swamp',
        'Deciduous Forest', 'Coniferous Forest', 'Rocky Shore', 'Sandy Beach', 'Cave System',
        'River Valley', 'Lake Shore', 'Bamboo Forest', 'Salt Marsh', 'Kelp Forest',
        'Volcanic Region', 'Coastal Cliff', 'Prairie', 'Steppe', 'Taiga', 'Deep Ocean',
        'Shallow Reef', 'Underground Cave', 'Hot Spring', 'Oasis', 'Canyon', 'Delta',
        'Estuary', 'Fjord', 'Glacier', 'Ice Sheet', 'Island', 'Peninsula'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "habitat": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("habitat", "seed",)
    FUNCTION = "generate_habitat"
    CATEGORY = "Art/Styles"

    def generate_habitat(self, randomize: str, seed: int, habitat: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            habitat = rng.choice(self._pool_for())

        return (f"{habitat}", seed)
