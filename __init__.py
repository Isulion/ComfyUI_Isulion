from .nodes.core.prompt_generator import IsulionPromptGenerator
from .nodes.core.ollama_generate import OllamaGenerate
from .nodes.animals.animal_selector import Isulion_AnimalRandom
from .nodes.animals.cute_animal_selector import IsulionCuteAnimalRandom
from .nodes.animals.animal_behavior import Isulion_AnimalBehaviorGenerator
from .nodes.characters.profession import IsulionProfessionGenerator
from .nodes.characters.fantasy_race import IsulionFantasyRaceGenerator
from .nodes.characters.clothing import IsulionClothingGenerator
from .nodes.environment.habitat import Isulion_HabitatGenerator
from .nodes.environment.weather import Isulion_WeatherGenerator
from .nodes.environment.time_of_day import Isulion_TimeOfDayGenerator
from .nodes.scene.action import IsulionActionGenerator
from .nodes.scene.composition import IsulionSceneComposition
from .nodes.style.art_style import Isulion_ArtStyleGenerator
from .nodes.style.emotion import Isulion_EmotionGenerator
from .nodes.fantasy.magical_effect import IsulionMagicalEffectGenerator
from .nodes.fantasy.mythical_location import IsulionMythicalLocationGenerator
from .nodes.fantasy.artifact import IsulionArtifactGenerator
from .nodes.scifi.tech import IsulionTechGenerator
from .nodes.scifi.alien_world import IsulionAlienWorldGenerator
from .nodes.scifi.spacecraft import IsulionSpacecraftGenerator
from .nodes.enhancement.style_mixer import IsulionStyleMixer
from .nodes.enhancement.prompt_enhancer import IsulionPromptEnhancer
from .nodes.enhancement.negative_prompt import IsulionNegativePromptGenerator

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
    "IsulionAnimalBehaviorGenerator": Isulion_AnimalBehaviorGenerator,
    "IsulionProfessionGenerator": IsulionProfessionGenerator,
    "IsulionFantasyRaceGenerator": IsulionFantasyRaceGenerator,
    "IsulionClothingGenerator": IsulionClothingGenerator,
    "IsulionActionGenerator": IsulionActionGenerator,
    "IsulionSceneComposition": IsulionSceneComposition,
    "IsulionMagicalEffectGenerator": IsulionMagicalEffectGenerator,
    "IsulionMythicalLocationGenerator": IsulionMythicalLocationGenerator,
    "IsulionArtifactGenerator": IsulionArtifactGenerator,
    "IsulionTechGenerator": IsulionTechGenerator,
    "IsulionAlienWorldGenerator": IsulionAlienWorldGenerator,
    "IsulionSpacecraftGenerator": IsulionSpacecraftGenerator,
    "IsulionStyleMixer": IsulionStyleMixer,
    "IsulionPromptEnhancer": IsulionPromptEnhancer,
    "IsulionNegativePromptGenerator": IsulionNegativePromptGenerator,
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
    "IsulionAnimalBehaviorGenerator": "Isulion Animal Behavior Generator 🦊",
    "IsulionProfessionGenerator": "Isulion Character Profession 👨‍🍳",
    "IsulionFantasyRaceGenerator": "Isulion Fantasy Race Generator 🧝‍♂️",
    "IsulionClothingGenerator": "Isulion Clothing Style Generator 👔",
    "IsulionActionGenerator": "Isulion Action Generator ⚔️",
    "IsulionSceneComposition": "Isulion Scene Composition 🎬",
    "IsulionMagicalEffectGenerator": "Isulion Magical Effect Generator ✨",
    "IsulionMythicalLocationGenerator": "Isulion Mythical Location Generator 🏰",
    "IsulionArtifactGenerator": "Isulion Artifact Generator 📿",
    "IsulionTechGenerator": "Isulion Tech Generator 🤖",
    "IsulionAlienWorldGenerator": "Isulion Alien World Generator 🪐",
    "IsulionSpacecraftGenerator": "Isulion Spacecraft Designer 🚀",
    "IsulionStyleMixer": "Isulion Style Mixer 🎨",
    "IsulionPromptEnhancer": "Isulion Prompt Enhancer 📝",
    "IsulionNegativePromptGenerator": "Isulion Negative Prompt Generator ⛔",
}
