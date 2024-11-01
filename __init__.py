import os
import sys
import importlib.util

# Add the current directory to the path
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

# Initialize empty mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    # Import core modules
    if importlib.util.find_spec("core.prompt_generator") is not None:
        from core.prompt_generator import IsulionPromptGenerator
        NODE_CLASS_MAPPINGS["IsulionPromptGenerator"] = IsulionPromptGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionPromptGenerator"] = "Isulion Prompt Generator ✨"

    if importlib.util.find_spec("core.ollama_generator") is not None:
        from core.ollama_generator import OllamaGenerate
        NODE_CLASS_MAPPINGS["IsulionOllamaGenerate"] = OllamaGenerate
        NODE_DISPLAY_NAME_MAPPINGS["IsulionOllamaGenerate"] = "Isulion Ollama Generate 🤖"

    # Import character nodes
    if importlib.util.find_spec("nodes.character.profession_generator") is not None:
        from nodes.character.profession_generator import IsulionProfessionGenerator
        NODE_CLASS_MAPPINGS["IsulionProfessionGenerator"] = IsulionProfessionGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionProfessionGenerator"] = "Isulion Character Profession 👨‍🍳"

    if importlib.util.find_spec("nodes.character.fantasy_race_generator") is not None:
        from nodes.character.fantasy_race_generator import IsulionFantasyRaceGenerator
        NODE_CLASS_MAPPINGS["IsulionFantasyRaceGenerator"] = IsulionFantasyRaceGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionFantasyRaceGenerator"] = "Isulion Fantasy Race Generator 🧝‍♂️"

    if importlib.util.find_spec("nodes.character.clothing_generator") is not None:
        from nodes.character.clothing_generator import IsulionClothingGenerator
        NODE_CLASS_MAPPINGS["IsulionClothingGenerator"] = IsulionClothingGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionClothingGenerator"] = "Isulion Clothing Style Generator 👔"

    # Import scene nodes
    if importlib.util.find_spec("nodes.scene.action_generator") is not None:
        from nodes.scene.action_generator import IsulionActionGenerator
        NODE_CLASS_MAPPINGS["IsulionActionGenerator"] = IsulionActionGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionActionGenerator"] = "Isulion Action Generator ⚔️"

    if importlib.util.find_spec("nodes.scene.scene_composition") is not None:
        from nodes.scene.scene_composition import IsulionSceneComposition
        NODE_CLASS_MAPPINGS["IsulionSceneComposition"] = IsulionSceneComposition
        NODE_DISPLAY_NAME_MAPPINGS["IsulionSceneComposition"] = "Isulion Scene Composition 🎬"

    # Import fantasy nodes
    if importlib.util.find_spec("nodes.fantasy.magical_effect_generator") is not None:
        from nodes.fantasy.magical_effect_generator import IsulionMagicalEffectGenerator
        NODE_CLASS_MAPPINGS["IsulionMagicalEffectGenerator"] = IsulionMagicalEffectGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionMagicalEffectGenerator"] = "Isulion Magical Effect Generator ✨"

    if importlib.util.find_spec("nodes.fantasy.mythical_location_generator") is not None:
        from nodes.fantasy.mythical_location_generator import IsulionMythicalLocationGenerator
        NODE_CLASS_MAPPINGS["IsulionMythicalLocationGenerator"] = IsulionMythicalLocationGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionMythicalLocationGenerator"] = "Isulion Mythical Location Generator 🏰"

    if importlib.util.find_spec("nodes.fantasy.artifact_generator") is not None:
        from nodes.fantasy.artifact_generator import IsulionArtifactGenerator
        NODE_CLASS_MAPPINGS["IsulionArtifactGenerator"] = IsulionArtifactGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionArtifactGenerator"] = "Isulion Artifact Generator 📿"

    # Import sci-fi nodes
    if importlib.util.find_spec("nodes.scifi.tech_generator") is not None:
        from nodes.scifi.tech_generator import IsulionTechGenerator
        NODE_CLASS_MAPPINGS["IsulionTechGenerator"] = IsulionTechGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionTechGenerator"] = "Isulion Tech Generator 🤖"

    if importlib.util.find_spec("nodes.scifi.alien_world_generator") is not None:
        from nodes.scifi.alien_world_generator import IsulionAlienWorldGenerator
        NODE_CLASS_MAPPINGS["IsulionAlienWorldGenerator"] = IsulionAlienWorldGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionAlienWorldGenerator"] = "Isulion Alien World Generator 🪐"

    if importlib.util.find_spec("nodes.scifi.spacecraft_generator") is not None:
        from nodes.scifi.spacecraft_generator import IsulionSpacecraftGenerator
        NODE_CLASS_MAPPINGS["IsulionSpacecraftGenerator"] = IsulionSpacecraftGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionSpacecraftGenerator"] = "Isulion Spacecraft Designer 🚀"

    # Import enhancement nodes
    if importlib.util.find_spec("nodes.enhancement.style_mixer") is not None:
        from nodes.enhancement.style_mixer import IsulionStyleMixer
        NODE_CLASS_MAPPINGS["IsulionStyleMixer"] = IsulionStyleMixer
        NODE_DISPLAY_NAME_MAPPINGS["IsulionStyleMixer"] = "Isulion Style Mixer 🎨"

    if importlib.util.find_spec("nodes.enhancement.prompt_enhancer") is not None:
        from nodes.enhancement.prompt_enhancer import IsulionPromptEnhancer
        NODE_CLASS_MAPPINGS["IsulionPromptEnhancer"] = IsulionPromptEnhancer
        NODE_DISPLAY_NAME_MAPPINGS["IsulionPromptEnhancer"] = "Isulion Prompt Enhancer 📝"

    if importlib.util.find_spec("nodes.enhancement.negative_prompt_generator") is not None:
        from nodes.enhancement.negative_prompt_generator import IsulionNegativePromptGenerator
        NODE_CLASS_MAPPINGS["IsulionNegativePromptGenerator"] = IsulionNegativePromptGenerator
        NODE_DISPLAY_NAME_MAPPINGS["IsulionNegativePromptGenerator"] = "Isulion Negative Prompt Generator ⛔"

except ImportError as e:
    print(f"Error importing Isulion nodes: {str(e)}")
except Exception as e:
    print(f"Error initializing Isulion nodes: {str(e)}")
