from ..base_selector import SimpleSelectorNode


class Isulion_WeatherGenerator(SimpleSelectorNode):
    POOL = [
        'Sunny', 'Cloudy', 'Partly Cloudy', 'Overcast', 'Rainy', 'Heavy Rain',
        'Thunderstorm', 'Lightning Storm', 'Snowy', 'Blizzard', 'Foggy', 'Misty',
        'Clear Sky', 'Stormy', 'Windy', 'Breezy', 'Hazy', 'Dusty', 'Sandstorm',
        'Drizzle', 'Sleet', 'Hail', 'Rainbow', 'Double Rainbow', 'Aurora Borealis',
        'Heat Wave', 'Humid', 'Dry', 'Frost', 'Ice Storm', 'Tornado', 'Hurricane',
        'Tropical Storm', 'Monsoon', 'Clear Night', 'Starry Night'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "weather": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("weather", "seed",)
    FUNCTION = "generate_weather"
    CATEGORY = "Art/Styles"

    def generate_weather(self, randomize: str, seed: int, weather: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            weather = rng.choice(self._pool_for())

        return (f"{weather}", seed)
