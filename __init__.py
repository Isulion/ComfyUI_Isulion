from .isulion_prompt_generator import IsulionPromptGenerator
from .isulion_OllamaGenerate import OllamaGenerate
from .isulion_animal_generator import Isulion_AnimalRandom
from .isulion_cute_animal_generator import IsulionCuteAnimalRandom
from .isulion_emotion_generator import Isulion_EmotionGenerator
from .isulion_habitat_generator import Isulion_HabitatGenerator
from .isulion_weather_generator import Isulion_WeatherGenerator
from .isulion_time_of_day_generator import Isulion_TimeOfDayGenerator
from .isulion_art_style_generator import Isulion_ArtStyleGenerator
from .isulion_animal_behavior_generator import Isulion_AnimalBehaviorGenerator

NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "IsulionOllamaGenerate": OllamaGenerate,
    "IsulionAnimalRandom": Isulion_AnimalRandom,
    "IsulionCuteAnimalRandom": IsulionCuteAnimalRandom,
    "IsulionEmotionGenerator": Isulion_EmotionGenerator,
    "IsulionHabitatGenerator": Isulion_HabitatGenerator,
    "IsulionWeatherGenerator": Isulion_WeatherGenerator,
    "IsulionTimeOfDayGenerator": Isulion_TimeOfDayGenerator,
    "IsulionArtStyleGenerator": Isulion_ArtStyleGenerator,
    "IsulionAnimalBehaviorGenerator": Isulion_AnimalBehaviorGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator ✨",
    "IsulionOllamaGenerate": "Isulion Ollama Generate 🤖",
    "IsulionAnimalRandom": "Isulion Animal Selector 🦁",
    "IsulionCuteAnimalRandom": "Isulion Cute Animal Selector 🐱",
    "IsulionEmotionGenerator": "Isulion Emotion Generator 😊",
    "IsulionHabitatGenerator": "Isulion Habitat Generator 🌲",
    "IsulionWeatherGenerator": "Isulion Weather Generator ⛅",
    "IsulionTimeOfDayGenerator": "Isulion Time of Day Generator 🌅",
    "IsulionArtStyleGenerator": "Isulion Art Style Generator 🎨",
    "IsulionAnimalBehaviorGenerator": "Isulion Animal Behavior Generator 🦊"
}
