class CustomTextNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello, World!", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "display_text"

    def display_text(self, text):
        return (text,)

NODE_CLASS_MAPPINGS = {
    "CustomTextNode": CustomTextNode
}