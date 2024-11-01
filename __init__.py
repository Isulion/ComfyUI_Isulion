import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

try:
    from core.prompt_generator import IsulionPromptGenerator
    from core.ollama_generator import OllamaGenerate

    # Animal nodes
    from nodes.animal.animal_selector import IsulionAnimalSelector
    from nodes.animal.cute_animal_selector import IsulionCuteAnimalSelector
    from nodes.animal.animal_behavior_generator import IsulionAnimalBehaviorGenerator

    # Character nodes
    from nodes.character.profession_generator import IsulionProfessionGenerator
    from nodes.character.fantasy_race_generator import IsulionFantasyRaceGenerator
    from nodes.character.clothing_generator import IsulionClothingGenerator

    # Environment nodes
    from nodes.environment.habitat_generator import IsulionHabitatGenerator
    from nodes.environment.weather_generator import IsulionWeatherGenerator
    from nodes.environment.time_of_day_generator import IsulionTimeOfDayGenerator

    # Scene nodes
    from nodes.scene.action_generator import IsulionActionGenerator
    from nodes.scene.scene_composition import IsulionSceneComposition

    # Style nodes
    from nodes.style.art_style_generator import IsulionArtStyleGenerator
    from nodes.style.emotion_generator import IsulionEmotionGenerator

    # Fantasy nodes
    from nodes.fantasy.magical_effect_generator import IsulionMagicalEffectGenerator
    from nodes.fantasy.mythical_location_generator import IsulionMythicalLocationGenerator
    from nodes.fantasy.artifact_generator import IsulionArtifactGenerator

    # Sci-fi nodes
    from nodes.scifi.tech_generator import IsulionTechGenerator
    from nodes.scifi.alien_world_generator import IsulionAlienWorldGenerator
    from nodes.scifi.spacecraft_generator import IsulionSpacecraftGenerator

    # Enhancement nodes
    from nodes.enhancement.style_mixer import IsulionStyleMixer
    from nodes.enhancement.prompt_enhancer import IsulionPromptEnhancer
    from nodes.enhancement.negative_prompt_generator import IsulionNegativePromptGenerator

except ImportError as e:
    print(f"Error importing Isulion nodes: {str(e)}")

# Node mappings
NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "IsulionOllamaGenerate": OllamaGenerate,
    # ... rest of the mappings ...
}

# Display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator ✨",
    "IsulionOllamaGenerate": "Isulion Ollama Generate 🤖",
    # ... rest of the mappings ...
}
