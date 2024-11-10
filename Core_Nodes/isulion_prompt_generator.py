import random
import logging
from typing import Tuple, Dict, List, ClassVar, Optional
from pathlib import Path
from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Add near the top of the file, after imports
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    subjects: ClassVar[List[str]]
    styles: ClassVar[List[str]]
    color_palettes: ClassVar[List[str]]
    lightings: ClassVar[List[str]]
    
    def __init__(self) -> None:
        """Initialize the generator and load configurations"""
        self.load_config_files()

    @classmethod
    def load_config_files(cls) -> None:
        """Load all configuration files from the config directory"""
        config_dir = Path(__file__).parent / "config"
        
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        
        for file_name in cls.CONFIG_FILES:
            file_path = config_dir / f"{file_name}.txt"
            try:
                # Create empty file if it doesn't exist
                if not file_path.exists():
                    file_path.write_text("Default", encoding='utf-8')
                    
                with open(file_path, 'r', encoding='utf-8') as f:
                    setattr(cls, file_name, [
                        line.strip() for line in f 
                        if line.strip() and not line.startswith('#')
                    ])
            except FileNotFoundError:
                logger.error(f"Configuration file not found: {file_path}")
                setattr(cls, file_name, ["Default"])
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
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
        # Always generate a new seed if none provided
        if seed == 0:
            seed = random.randint(0, 999999999)
        random.seed(seed)
        
        selections = (
            random.choice(self.subjects),
            random.choice(self.styles),
            random.choice(self.color_palettes),
            random.choice(self.lightings)
        )
        
        # Reset the random seed to avoid affecting other operations
        random.seed()
        return selections

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
            # Always generate a new seed if none provided
            if seed == 0:
                seed = random.randint(0, 999999999)
                
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
            logger.error(f"Error generating prompt: {str(e)}")
            raise RuntimeError(
                f"Failed to generate prompt. Please check if all config files exist and "
                f"contain valid data. Error: {str(e)}"
            ) from e

# Register the node
NODE_CLASS_MAPPINGS["IsulionPromptGenerator"] = IsulionPromptGenerator
NODE_DISPLAY_NAME_MAPPINGS["IsulionPromptGenerator"] = "Isulion Prompt Generator ✨"
