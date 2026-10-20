import os
import subprocess
import shutil

import logging
logger = logging.getLogger(__name__)

# The node only actually shuts down the machine when explicitly armed:
#   ISULION_ENABLE_SHUTDOWN=1
ISULION_ENABLE_SHUTDOWN = os.getenv("ISULION_ENABLE_SHUTDOWN", "0") == "1"

if ISULION_ENABLE_SHUTDOWN:
    print("\033[93m⚠️  SECURITY WARNING: '💤 IsulionShutdown' is ARMED (ISULION_ENABLE_SHUTDOWN=1).\033[0m")
    print("\033[93m   Executing this node will shut down the entire system.\033[0m")


class ShutdownNode:
    """
    A node that can shut down the computer when the workflow reaches it.
    It stays registered for workflow compatibility, but performs a no-op
    unless the environment variable ISULION_ENABLE_SHUTDOWN=1 is set.
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

    def shutdown_computer(self, any, delay):
        if not ISULION_ENABLE_SHUTDOWN:
            logger.info("IsulionShutdown: disabled (set ISULION_ENABLE_SHUTDOWN=1 to arm). Skipping shutdown.")
            return ()
        try:
            if os.name == 'nt':  # Windows
                args = ["shutdown", "/s", "/f", "/t", str(delay)]
            else:  # Linux/Unix
                minutes = max(1, round(delay / 60))  # Convert seconds to minutes, minimum 1 minute
                args = ["shutdown", "-h", f"+{minutes}"]
            if shutil.which(args[0]) is None:
                logger.error(f"IsulionShutdown: '{args[0]}' not found on PATH. Cannot shut down.")
                return ()
            subprocess.run(args, check=False)
            logger.info(f"Shutdown command initiated. Computer will shutdown in {delay} seconds.")
        except Exception as e:
            logger.error(f"Error initiating shutdown: {str(e)}")

        return ()

NODE_CLASS_MAPPINGS = {
    "💤 IsulionShutdown": ShutdownNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "💤 IsulionShutdown": "💤 Isulion Shutdown"
}
