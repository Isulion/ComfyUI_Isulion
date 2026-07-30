"""
Isulion ComfyUI Custom Nodes
A collection of powerful prompt generation nodes for ComfyUI
"""

__version__ = "5.1.5"
__author__ = "Isulion"
__description__ = "Advanced prompt generation nodes for ComfyUI with multiple themes and styles"

WEB_DIRECTORY = ".Core_Nodes/js"

# Import all node classes
from .Core_Nodes.mega_prompt_V3 import IsulionMegaPromptV3
from .Core_Nodes.mega_prompt_all_themes import IsulionMultiplePromptGenerator
from .Core_Nodes.isucollage_node import IsuCollageNode
from .Core_Nodes.load_images_node import IsulionLoadImagesNode
from .Core_Nodes.shutdown_node import NODE_CLASS_MAPPINGS as ShutdownNode
from .Core_Nodes.QrCode_Generator import NODE_CLASS_MAPPINGS as QRCodeNode
from .Core_Nodes.Overlay_node import NODE_CLASS_MAPPINGS as OverlayQRCodeNode
from .Core_Nodes.video_prompt_generator import NODE_CLASS_MAPPINGS as VIDEO_PROMPT_NODES
from .Core_Nodes.display_image_from_url import DisplayImageFromURL
from .Core_Nodes.CustomTextNode import CustomTextNode

# Import category-specific nodes
from .Core_Nodes.animals_nodes.isulion_animal_generator import Isulion_AnimalRandom
from .Core_Nodes.animals_nodes.isulion_cute_animal_generator import IsulionCuteAnimalRandom
from .Core_Nodes.animals_nodes.isulion_animal_behavior_generator import Isulion_AnimalBehaviorGenerator

from .Core_Nodes.scene_nodes.isulion_habitat_generator import Isulion_HabitatGenerator
from .Core_Nodes.scene_nodes.isulion_weather_generator import Isulion_WeatherGenerator
from .Core_Nodes.scene_nodes.isulion_time_of_day_generator import Isulion_TimeOfDayGenerator
from .Core_Nodes.scene_nodes.isulion_art_style_generator import Isulion_ArtStyleGenerator
from .Core_Nodes.scene_nodes.isulion_action_generator import IsulionActionGenerator
from .Core_Nodes.scene_nodes.isulion_scene_composition import IsulionSceneComposition

from .Core_Nodes.character_nodes.isulion_profession_generator import IsulionProfessionGenerator
from .Core_Nodes.character_nodes.isulion_fantasy_race_generator import IsulionFantasyRaceGenerator
from .Core_Nodes.character_nodes.isulion_clothing_generator import IsulionClothingGenerator
from .Core_Nodes.character_nodes.isulion_epoch_generator import IsulionEpochGenerator

from .Core_Nodes.fantasy_nodes.isulion_magical_effect_generator import IsulionMagicalEffectGenerator
from .Core_Nodes.fantasy_nodes.isulion_mythical_location_generator import IsulionMythicalLocationGenerator
from .Core_Nodes.fantasy_nodes.isulion_artifact_generator import IsulionArtifactGenerator

from .Core_Nodes.scifi_nodes.isulion_tech_generator import IsulionTechGenerator
from .Core_Nodes.scifi_nodes.isulion_alien_world_generator import IsulionAlienWorldGenerator
from .Core_Nodes.scifi_nodes.isulion_spacecraft_generator import IsulionSpacecraftGenerator

from .Core_Nodes.enhancement_nodes.isulion_emotion_generator import Isulion_EmotionGenerator
from .Core_Nodes.enhancement_nodes.isulion_style_mixer import IsulionStyleMixer
from .Core_Nodes.enhancement_nodes.isulion_prompt_enhancer import IsulionPromptEnhancer
from .Core_Nodes.enhancement_nodes.isulion_negative_prompt_generator import IsulionNegativePromptGenerator
from .Core_Nodes.civitai_nodes.civitai_API_node import IsulionCivitaiModelExplorer, IsulionCivitaiTrending, IsulionCivitaiImageDisplay

# Node mappings
NODE_CLASS_MAPPINGS = {
    **VIDEO_PROMPT_NODES,
    **ShutdownNode,
    **QRCodeNode,
    **OverlayQRCodeNode,
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
    "IsulionCivitaiModelExplorer": IsulionCivitaiModelExplorer,
    "IsulionCivitaiTrending": IsulionCivitaiTrending,
    "IsulionCivitaiImageDisplay": IsulionCivitaiImageDisplay,
    "IsulionMegaPromptV3": IsulionMegaPromptV3,
    "IsulionMultiplePromptGenerator": IsulionMultiplePromptGenerator,
    "IsuCollage_Node": IsuCollageNode,
    "IsulionLoadImagesNode": IsulionLoadImagesNode,
    "IsulionEpochGenerator": IsulionEpochGenerator,
    "DisplayImageFromURL": DisplayImageFromURL,
    "CustomTextNode": CustomTextNode,
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
    "IsulionCivitaiModelExplorer": "🔍 Isulion Civitai Model Explorer",
    "IsulionCivitaiTrending": "🔥 Isulion Civitai Trending",
    "IsulionCivitaiImageDisplay": "🖼️ Isulion Civitai Image Display",
    "IsuCollage_Node": "🖼️ Isulion Image Collage",
    "IsulionLoadImagesNode": "📁 Isulion Load Images from Directory",
    "IsulionEpochGenerator": "⏳ Isulion Epoch Generator",
    "DisplayImageFromURL": "🖼️ Isulion Display Image From URL",
    "CustomTextNode": "📝 Custom Text Node",
    "💤 IsulionShutdown": "💤 Isulion Shutdown",
    "🧩 IsulionQRCode": "🧩 Isulion QRCode Generator",
    "⧉ IsulionOverlay": "⧉ IsulionOverlay"
}

__version__ = "5.1.5"