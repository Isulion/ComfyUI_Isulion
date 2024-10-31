from .isulion_prompt_generator import IsulionPromptGenerator
from .isulion_OllamaGenerate import OllamaGenerate
from .isulion_animal_generator import IsulionAnimalRandom
from .isulion_cute_animal_generator import IsulionCuteAnimalRandom

NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "OllamaGenerate": OllamaGenerate,
    "AnimalGenerator": IsulionAnimalRandom,
    "CuteAnimalGenerator": IsulionCuteAnimalRandom
}

# Optional: Provide a custom display name for the node
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator",
    "OllamaGenerate": "Isulion Ollama Generate",
    "AnimalGenerator": "Isulion Animal Selector",
    "AnimalGenerator": "Isulion Cute Animal Selector"
    
}
