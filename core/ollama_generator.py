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
    CATEGORY = "Isulion/Core"

    def ollama_generate(self, prompt, url, model):
        client = Client(host=url)
        response = client.generate(
            model=model,
            prompt=prompt,
            keep_alive="0m"
        )
        return (response['response'],) 