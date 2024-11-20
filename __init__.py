from .Core_Nodes.isulion_prompt_generator import IsulionPromptGenerator
from .animals_nodes.isulion_animal_generator import Isulion_AnimalRandom
from .animals_nodes.isulion_cute_animal_generator import IsulionCuteAnimalRandom
from .animals_nodes.isulion_animal_behavior_generator import Isulion_AnimalBehaviorGenerator
from .scene_nodes.isulion_habitat_generator import Isulion_HabitatGenerator
from .scene_nodes.isulion_weather_generator import Isulion_WeatherGenerator
from .scene_nodes.isulion_time_of_day_generator import Isulion_TimeOfDayGenerator
from .scene_nodes.isulion_art_style_generator import Isulion_ArtStyleGenerator
from .scene_nodes.isulion_action_generator import IsulionActionGenerator
from .scene_nodes.isulion_scene_composition import IsulionSceneComposition
from .character_nodes.isulion_profession_generator import IsulionProfessionGenerator
from .character_nodes.isulion_fantasy_race_generator import IsulionFantasyRaceGenerator
from .character_nodes.isulion_clothing_generator import IsulionClothingGenerator
from .fantasy_nodes.isulion_magical_effect_generator import IsulionMagicalEffectGenerator
from .fantasy_nodes.isulion_mythical_location_generator import IsulionMythicalLocationGenerator
from .fantasy_nodes.isulion_artifact_generator import IsulionArtifactGenerator
from .scifi_nodes.isulion_tech_generator import IsulionTechGenerator
from .scifi_nodes.isulion_alien_world_generator import IsulionAlienWorldGenerator
from .scifi_nodes.isulion_spacecraft_generator import IsulionSpacecraftGenerator
from .enhancement_nodes.isulion_emotion_generator import Isulion_EmotionGenerator
from .enhancement_nodes.isulion_style_mixer import IsulionStyleMixer
from .enhancement_nodes.isulion_prompt_enhancer import IsulionPromptEnhancer
from .enhancement_nodes.isulion_negative_prompt_generator import IsulionNegativePromptGenerator
from .Core_Nodes.mega_prompt_generator import IsulionMegaPromptGenerator
from .Mega_Prompt_V2 import MegaPromptV2

NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
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
    "IsulionMegaPromptGenerator": IsulionMegaPromptGenerator,
    "MegaPromptV2": MegaPromptV2,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator ✨",
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
    "IsulionMegaPromptGenerator": "Isulion Mega Prompt Generator 🎯",
    "MegaPromptV2": "Isulion Mega Prompt Generator V2 🚀",
}
