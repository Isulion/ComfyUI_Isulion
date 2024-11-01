import random
from nodes import NODE_CLASS_MAPPINGS

class Isulion_TimeOfDayGenerator:
    times = [
        'Dawn', 'Sunrise', 'Early Morning', 'Morning', 'Late Morning', 'Noon',
        'Early Afternoon', 'Afternoon', 'Late Afternoon', 'Golden Hour',
        'Sunset', 'Dusk', 'Twilight', 'Evening', 'Night', 'Midnight',
        'Blue Hour', 'First Light', 'Magic Hour', 'Civil Twilight',
        'Astronomical Twilight', 'Nautical Twilight', 'Witching Hour',
        'Pre-dawn', 'Post-sunset'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "time": (cls.times,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("time", "seed",)
    FUNCTION = "generate_time"
    CATEGORY = "Art/Styles"

    def generate_time(self, randomize, seed, time):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            time = random.choice(self.times)

        return (f"{time}", seed)

# Remove NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS from here