from .isulion_prompt_generator import IsulionPromptGenerator
from .isulion_OllamaGenerate import OllamaGenerate
from .ixulion_ollamaModelSelect import OllamaModelSelector

NODE_CLASS_MAPPINGS = {
    "IsulionPromptGenerator": IsulionPromptGenerator,
    "OllamaGenerate": OllamaGenerate,
    "OllamaModelSelector": OllamaModelSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator",
    "OllamaGenerate": "Ollama Generate",
    "OllamaModelSelector": "Ixulion Ollama Model Selector"
}
