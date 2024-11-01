from ollama import Client

class OllamaGenerate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
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
                "model": ((), {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "ollama_generate"
    CATEGORY = "Ollama"

    def ollama_generate(self, prompt, url, model):
        # Keep_alive is now hardcoded to 0 (not visible to user)
        keep_alive = 0

        client = Client(host=url)

        # Generate the response from the model
        response = client.generate(
            model=model,
            prompt=prompt,
            keep_alive=f"{keep_alive}m"  # keep_alive is always 0
        )

        return (response['response'],)

# Register the node with your node mapping system
NODE_CLASS_MAPPINGS = {
    "OllamaGenerate": OllamaGenerate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaGenerate": "Isulion Ollama Generate 🤖",
}
