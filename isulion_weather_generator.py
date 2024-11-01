import random
from nodes import NODE_CLASS_MAPPINGS

class Isulion_WeatherGenerator:
    weather_conditions = [
        'Sunny', 'Cloudy', 'Partly Cloudy', 'Overcast', 'Rainy', 'Heavy Rain',
        'Thunderstorm', 'Lightning Storm', 'Snowy', 'Blizzard', 'Foggy', 'Misty',
        'Clear Sky', 'Stormy', 'Windy', 'Breezy', 'Hazy', 'Dusty', 'Sandstorm',
        'Drizzle', 'Sleet', 'Hail', 'Rainbow', 'Double Rainbow', 'Aurora Borealis',
        'Heat Wave', 'Humid', 'Dry', 'Frost', 'Ice Storm', 'Tornado', 'Hurricane',
        'Tropical Storm', 'Monsoon', 'Clear Night', 'Starry Night'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "weather": (cls.weather_conditions,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("weather", "seed",)
    FUNCTION = "generate_weather"
    CATEGORY = "Art/Styles"

    def generate_weather(self, randomize, seed, weather):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            weather = random.choice(self.weather_conditions)

        return (f"{weather}", seed)

# Remove NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS from here