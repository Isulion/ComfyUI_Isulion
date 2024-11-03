from ollama import Client
import json

class OllamaGenerate:
    """Node for generating text using Ollama models"""
    
    def __init__(self):
        self.client = None
        self.current_host = None
        self.available_models = []
        self._update_model_list()
    
    def _update_model_list(self):
        """Fetch available models from Ollama server"""
        try:
            self.client = Client(host="http://127.0.0.1:11434")
            self.current_host = "http://127.0.0.1:11434"
            models = self.client.list()
            self.available_models = [model['name'] for model in models['models']]
        except Exception as e:
            print(f"Failed to fetch models: {str(e)}")
            self.available_models = []
    
    @classmethod
    def INPUT_TYPES(cls):
        try:
            # Create temporary instance to get models
            temp = cls()
            models = temp.available_models
            if not models:
                raise ValueError("No models available - Please check if Ollama server is running")
        except Exception as e:
            print(f"Error getting models: {str(e)}")
            models = []
            
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "What is Art?"
                }),
                "url": ("STRING", {
                    "multiline": False,
                    "default": "http://127.0.0.1:11434"
                }),
                "model": (models, {
                    "default": models[0] if models else ""
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "ollama_generate"
    CATEGORY = "Ollama"

    def ollama_generate(self, prompt, url, model):
        """Generate text using Ollama model
        
        Args:
            prompt (str): Input prompt for generation
            url (str): Ollama API endpoint URL
            model (str): Name of the model to use
            
        Returns:
            tuple: Generated response text
        """
        try:
            # Initialize client if needed
            if not self.client or self.current_host != url:
                self.client = Client(host=url)
                self.current_host = url
                self._update_model_list()

            # Validate inputs
            if not prompt.strip():
                raise ValueError("Prompt cannot be empty")
                
            if not url.startswith(("http://", "https://")):
                raise ValueError("Invalid URL format")

            # Generate response
            response = self.client.generate(
                model=model,
                prompt=prompt,
                keep_alive="0m"  # Keep alive disabled
            )

            # Extract and validate response
            if not response or 'response' not in response:
                raise RuntimeError("Invalid response from Ollama")
                
            return (response['response'],)

        except Exception as e:
            error_msg = f"Ollama generation failed: {str(e)}"
            print(error_msg)
            return (error_msg,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "OllamaGenerate": OllamaGenerate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaGenerate": "Isulion Ollama Generate 🤖",
}
