from ..base_selector import SimpleSelectorNode


class Isulion_TimeOfDayGenerator(SimpleSelectorNode):
    POOL = [
        'Dawn', 'Sunrise', 'Early Morning', 'Morning', 'Late Morning', 'Noon',
        'Early Afternoon', 'Afternoon', 'Late Afternoon', 'Golden Hour',
        'Sunset', 'Dusk', 'Twilight', 'Evening', 'Night', 'Midnight',
        'Blue Hour', 'First Light', 'Magic Hour', 'Civil Twilight',
        'Astronomical Twilight', 'Nautical Twilight', 'Witching Hour',
        'Pre-dawn', 'Post-sunset'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "time": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("time", "seed",)
    FUNCTION = "generate_time"
    CATEGORY = "Art/Styles"

    def generate_time(self, randomize: str, seed: int, time: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            time = rng.choice(self._pool_for())

        return (f"{time}", seed)
