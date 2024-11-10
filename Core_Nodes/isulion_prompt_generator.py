import random
import logging
from typing import Tuple, Dict, List, ClassVar
from pathlib import Path
from nodes import NODE_CLASS_MAPPINGS

class IsulionPromptGenerator:
    """
    A ComfyUI node that generates creative prompts by combining subjects, styles, 
    color palettes, and lighting. Supports manual and random selection modes.
    """
    
    # Class variables
    CONFIG_FILES: ClassVar[List[str]] = ["subjects", "styles", "color_palettes", "lightings"]
    PROMPT_TEMPLATE: ClassVar[str] = """
Subject: {subject}
Style: {style}
Color Palette: {color_palette}
Lighting: {lighting}""".strip()
    
    def __init__(self) -> None:
        """Initialize the generator and load configurations"""
        self.load_config_files()

    @classmethod
    def load_config_files(cls) -> None:
        """Load all configuration files from the config directory"""
        config_dir = Path(__file__).parent / "config"
        
        for file_name in cls.CONFIG_FILES:
            file_path = config_dir / f"{file_name}.txt"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    setattr(cls, file_name, [
                        line.strip() for line in f 
                        if line.strip() and not line.startswith('#')
                    ])
            except FileNotFoundError:
                logging.error(f"Configuration file not found: {file_path}")
                setattr(cls, file_name, ["Default"])
            except Exception as e:
                logging.error(f"Error loading {file_path}: {str(e)}")
                setattr(cls, file_name, ["Error"])

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """Define input types for the node"""
        if not hasattr(cls, 'subjects'):
            cls.load_config_files()
            
        return {
            "required": {
                "subject": (cls.subjects,),
                "style": (cls.styles,),
                "color_palette": (cls.color_palettes,),
                "lighting": (cls.lightings,),
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "INT",)
    RETURN_NAMES = ("complete_prompt", "subject", "style", "color_palette", "lighting", "seed",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Art/Styles"

    def _get_random_selections(self, seed: int) -> Tuple[str, str, str, str]:
        """Generate random selections using the provided seed"""
        random.seed(seed or random.randint(0, 999999999))
        return (
            random.choice(self.subjects),
            random.choice(self.styles),
            random.choice(self.color_palettes),
            random.choice(self.lightings)
        )

    def generate_prompt(
        self,
        subject: str,
        style: str,
        color_palette: str,
        lighting: str,
        randomize: str,
        seed: int
    ) -> Tuple[str, str, str, str, str, int]:
        """
        Generate a creative prompt by combining various artistic elements.
        
        Args:
            subject: The main subject of the prompt
            style: The artistic style to apply
            color_palette: The color scheme to use
            lighting: The lighting setup
            randomize: Whether to randomize selections ("enable" or "disable")
            seed: Random seed for reproducibility
            
        Returns:
            Tuple containing (complete_prompt, subject, style, color_palette, lighting, seed)
        """
        try:
            if randomize == "enable":
                subject, style, color_palette, lighting = self._get_random_selections(seed)

            complete_prompt = self.PROMPT_TEMPLATE.format(
                subject=subject,
                style=style,
                color_palette=color_palette,
                lighting=lighting
            )

            return (complete_prompt, subject, style, color_palette, lighting, seed)

        except Exception as e:
            logging.error(f"Error generating prompt: {str(e)}")
            raise RuntimeError(f"Failed to generate prompt: {str(e)}") from e

# Register the node
NODE_CLASS_MAPPINGS["IsulionPromptGenerator"] = IsulionPromptGenerator
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionPromptGenerator": "Isulion Prompt Generator ✨"
}
