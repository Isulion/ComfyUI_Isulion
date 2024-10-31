import subprocess
import logging

class OllamaModelSelector:
    @classmethod
    def INPUT_TYPES(s):
        try:
            # Run ollama list command
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse the output, skipping the header line
                lines = result.stdout.strip().split('\n')[1:]
                models = []
                
                for line in lines:
                    if line.strip():  # Skip empty lines
                        # First column before whitespace is the model name
                        model_name = line.split()[0]
                        # Remove ':latest' suffix if present
                        model_name = model_name.replace(':latest', '')
                        models.append(model_name)
                
                # Sort models alphabetically for better UX
                models.sort()
                
                if not models:  # If no models found after parsing
                    models = ["No models installed - Use 'ollama pull' to install models"]
            else:
                models = ["Error running ollama list command"]
                logging.warning(f"Failed to get models from ollama list: {result.stderr}")
        except FileNotFoundError:
            models = ["Ollama not found - Is it installed?"]
            logging.error("Ollama command not found. Please ensure Ollama is installed and in PATH")
        except Exception as e:
            models = ["Error getting model list"]
            logging.error(f"Error getting Ollama models: {str(e)}")

        return {
            "required": {
                "model_name": (models, {
                    "default": models[2] if models else "No models found",
                    "tooltip": "Select an Ollama model to use"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)  # Simple string return type
    RETURN_NAMES = ("MODEL",)
    FUNCTION = "get_model"
    
    CATEGORY = "Isulion/Ollama"
    DESCRIPTION = "Select an Ollama model from installed models"

    def get_model(self, model_name):
        # Return just the model name string
        return (model_name,)  # Return as tuple with single string value

NODE_CLASS_MAPPINGS = {
    "OllamaModelSelector": OllamaModelSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaModelSelector": "Ollama Model Selector"
} 