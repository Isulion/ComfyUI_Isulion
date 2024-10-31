from ollama import Client
import logging

class OllamaGenerate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "What is Art?",
                    "tooltip": "Input text to send to Ollama"
                }),
                "system": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "System prompt to set the behavior and context for the model"
                }),
                "model_name": ("STRING", {
                    "default": "dolphin-llama3",
                    "tooltip": "Name of the Ollama model to use"
                }),
                "host_url": ("STRING", {
                    "default": " http://localhost:11434",
                    "tooltip": "Ollama server URL (e.g., http://localhost:11434)"
                }),
                "keep_alive": (["true", "false"], {
                    "default": "true",
                    "tooltip": "Keep model loaded in memory (true) or unload after each generation (false)"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Ollama"

    def generate(self, text, system, model_name, host_url, keep_alive):
        try:
            # Create client with provided host URL
            client = Client(host=host_url)
            
            # Convert keep_alive string to appropriate value
            keep_alive_value = "5m" if keep_alive == "true" else "0m"
            
            # Generate response using the specified model
            response = client.generate(
                model=model_name,
                prompt=text,
                system=system,  # Added system prompt
                keep_alive=keep_alive_value
            )
            
            return (response['response'],)
            
        except Exception as e:
            logging.error(f"Error generating response from Ollama: {str(e)}")
            return (f"Error: {str(e)}",)

NODE_CLASS_MAPPINGS = {
    "OllamaGenerate": OllamaGenerate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaGenerate": "Ollama Generate",
}
