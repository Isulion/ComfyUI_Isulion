"""
Isulion ComfyUI Custom Nodes
A collection of powerful prompt generation nodes for ComfyUI
"""

__version__ = "2.0.0"
__author__ = "Isulion"
__description__ = "Advanced prompt generation nodes for ComfyUI with multiple themes and styles"

# Import all node classes
from .Core_Nodes.isulion_prompt_generator import IsulionPromptGenerator
from .mega_prompt_V3 import MegaPromptV3
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
from .character_nodes.isulion_epoch_generator import IsulionEpochGenerator
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
from .Core_Nodes.video_prompt_generator import NODE_CLASS_MAPPINGS as VIDEO_PROMPT_NODES
from .mega_prompt_all_themes import IsulionMultiplePromptGenerator
from .isucollage_node import IsuCollageNode
from .load_images_node import IsulionLoadImagesNode
from .shutdown_node import NODE_CLASS_MAPPINGS as SHUTDOWN_NODES

# Node mappings
NODE_CLASS_MAPPINGS = {
    **VIDEO_PROMPT_NODES,
    **SHUTDOWN_NODES,
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "IsulionAnimalRandom": Isulion_AnimalRandom,
    "IsulionCuteAnimalRandom": IsulionCuteAnimalRandom,
    "IsulionAnimalBehaviorGenerator": Isulion_AnimalBehaviorGenerator,
    "IsulionHabitatGenerator": Isulion_HabitatGenerator,
    "IsulionWeatherGenerator": Isulion_WeatherGenerator,
    "IsulionTimeOfDayGenerator": Isulion_TimeOfDayGenerator,
    "IsulionArtStyleGenerator": Isulion_ArtStyleGenerator,
    "IsulionActionGenerator": IsulionActionGenerator,
    "IsulionSceneComposition": IsulionSceneComposition,
    "IsulionProfessionGenerator": IsulionProfessionGenerator,
    "IsulionFantasyRaceGenerator": IsulionFantasyRaceGenerator,
    "IsulionClothingGenerator": IsulionClothingGenerator,
    "IsulionMagicalEffectGenerator": IsulionMagicalEffectGenerator,
    "IsulionMythicalLocationGenerator": IsulionMythicalLocationGenerator,
    "IsulionArtifactGenerator": IsulionArtifactGenerator,
    "IsulionTechGenerator": IsulionTechGenerator,
    "IsulionAlienWorldGenerator": IsulionAlienWorldGenerator,
    "IsulionSpacecraftGenerator": IsulionSpacecraftGenerator,
    "IsulionEmotionGenerator": Isulion_EmotionGenerator,
    "IsulionStyleMixer": IsulionStyleMixer,
    "IsulionPromptEnhancer": IsulionPromptEnhancer,
    "IsulionNegativePromptGenerator": IsulionNegativePromptGenerator,
    "IsulionMegaPromptGenerator": IsulionMegaPromptGenerator,
    "MegaPromptV3": MegaPromptV3,
    "IsulionMultiplePromptGenerator": IsulionMultiplePromptGenerator,
    "IsuCollage_Node": IsuCollageNode,
    "IsulionLoadImagesNode": IsulionLoadImagesNode,
    "IsulionEpochGenerator": IsulionEpochGenerator
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "🎨 Isulion Prompt Generator",
    "MegaPromptV3": "🚀 Isulion Mega Prompt V3",
    "IsulionMultiplePromptGenerator": "🔄 Isulion Multiple Prompt Generator",
    "IsulionAnimalRandom": "🦁 Isulion Animal Selector",
    "IsulionCuteAnimalRandom": "🐰 Isulion Cute Animal Selector",
    "IsulionAnimalBehaviorGenerator": "🦊 Isulion Animal Behavior Generator",
    "IsulionHabitatGenerator": "🌳 Isulion Habitat Generator",
    "IsulionWeatherGenerator": "🌤️ Isulion Weather Generator",
    "IsulionTimeOfDayGenerator": "🌅 Isulion Time of Day Generator",
    "IsulionArtStyleGenerator": "🖼️ Isulion Art Style Generator",
    "IsulionActionGenerator": "⚡ Isulion Action Generator",
    "IsulionSceneComposition": "🎬 Isulion Scene Composition",
    "IsulionProfessionGenerator": "👨‍💼 Isulion Profession Generator",
    "IsulionFantasyRaceGenerator": "🧝‍♂️ Isulion Fantasy Race Generator",
    "IsulionClothingGenerator": "👔 Isulion Clothing Generator",
    "IsulionMagicalEffectGenerator": "✨ Isulion Magical Effect Generator",
    "IsulionMythicalLocationGenerator": "🏰 Isulion Mythical Location Generator",
    "IsulionArtifactGenerator": "⚔️ Isulion Artifact Generator",
    "IsulionTechGenerator": "🤖 Isulion Tech Generator",
    "IsulionAlienWorldGenerator": "👽 Isulion Alien World Generator",
    "IsulionSpacecraftGenerator": "🛸 Isulion Spacecraft Generator",
    "IsulionEmotionGenerator": "😊 Isulion Emotion Generator",
    "IsulionStyleMixer": "🎨 Isulion Style Mixer",
    "IsulionPromptEnhancer": "💫 Isulion Prompt Enhancer",
    "IsulionNegativePromptGenerator": "⛔ Isulion Negative Prompt Generator",
    "IsulionMegaPromptGenerator": "🌟 Isulion Mega Prompt Generator",
    "IsuCollage_Node": "🖼️ Isulion Image Collage",
    "IsulionLoadImagesNode": "📁 Isulion Load Images from Directory",
    "IsulionEpochGenerator": "⏳ Isulion Epoch Generator"
}

__version__ = "2.0.0"