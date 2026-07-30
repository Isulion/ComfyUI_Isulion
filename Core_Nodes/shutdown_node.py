import os
import subprocess

print("\033[93m⚠️  SECURITY WARNING: The '💤 IsulionShutdown' node is loaded.\033[0m")
print("\033[93m   This node can shut down your entire system when executed.\033[0m")
print("\033[93m   Only use in trusted workflows. To disable, remove shutdown_node.py.\033[0m")

class ShutdownNode:
    """
    A node that will shutdown the computer.
    WARNING: This node executes a system shutdown command.
    Only use in trusted workflows.
    """
    
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": ("*",),
                "delay": ("INT", {
                    "default": 30,
                    "min": 0,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "shutdown_computer"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def shutdown_computer(self, input, delay):
        try:
            if os.name == 'nt':  # Windows
                os.system(f'shutdown /s /f /t {delay}')
            else:  # Linux/Unix
                minutes = max(1, round(delay / 60))  # Convert seconds to minutes, minimum 1 minute
                os.system(f'shutdown -h +{minutes}')
            print(f"Shutdown command initiated. Computer will shutdown in {delay} seconds.")
        except Exception as e:
            print(f"Error initiating shutdown: {str(e)}")
        
        return ()

NODE_CLASS_MAPPINGS = {
    "💤 IsulionShutdown": ShutdownNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "💤 IsulionShutdown": "💤 Isulion Shutdown"
}
