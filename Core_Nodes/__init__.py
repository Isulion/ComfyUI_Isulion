from .display_image_from_url import DisplayImageFromURL
from .civitai_nodes.civitai_API_node import *

# Initialize the dictionaries
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Update the mappings
NODE_CLASS_MAPPINGS.update({
    "DisplayImageFromURL": DisplayImageFromURL,
})

NODE_DISPLAY_NAME_MAPPINGS.update({
    "DisplayImageFromURL": "Display Image From URL",
}) 