from .isulion_prompt_generator import IsulionPromptGenerator
from .isulion_OllamaGenerate import OllamaGenerate

NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "OllamaGenerate": OllamaGenerate
}

# Optional: Provide a custom display name for the node
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator",
    "OllamaGenerate": "Isulion Ollama Generate"
}
