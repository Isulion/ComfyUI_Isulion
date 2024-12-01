import os
import subprocess

class ShutdownNode:
    """
    A node that will shutdown the computer.
    """
    
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": ("STRING", {"default": ""})  
            },
            "hidden": {"input": "STRING"}  
        }

    RETURN_TYPES = ()
    FUNCTION = "shutdown_computer"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def shutdown_computer(self, input=None):  
        try:
            if os.name == 'nt':  # Windows
                # Force shutdown with a 30-second delay
                os.system('shutdown /s /f /t 30')
            else:  # Linux/Unix
                os.system('shutdown -h +1')
            print("Shutdown command initiated. Computer will shutdown in 30 seconds.")
        except Exception as e:
            print(f"Error initiating shutdown: {str(e)}")
        
        return ()

NODE_CLASS_MAPPINGS = {
    "IsulionShutdown": ShutdownNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionShutdown": " Isulion Shutdown"
}
