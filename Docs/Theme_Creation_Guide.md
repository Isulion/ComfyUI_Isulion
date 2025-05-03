# Theme Creation Guide 🎨

## Create Custom Themes for ComfyUI

This guide provides a step-by-step process for creating custom themes within ComfyUI, allowing you to tailor the generated prompts to your desired aesthetic.

## Required Directory Structure

```bash
ComfyUI/
├── Core_Nodes/
│   ├── theme_handlers/   # Handler files directory
│   │   └── your_theme_handler.py  # Your handler file
│   ├── configs/              # Config files directory
│   │   └── your_theme.json       # Your config file
└── mega_prompt_V3.py             # Registration file
```

---

## Critical Naming Rules

1. **Handler filename**: `Core_Nodes/theme_handlers/your_theme_handler.py` (no double underscores).
2. **Config filename**: `Core_Nodes/configs/your_theme.json`.
3. Use **consistent internal names** (`your_theme`) across all files.  This is crucial for linking the handler, config, and UI elements.
4. **Handler class name and config key must match the internal name** (e.g., `YourThemeHandler` for `your_theme`).

---

## Required Files Checklist

- [ ] Handler file: `your_theme_handler.py`
- [ ] Config file: `your_theme.json`
- [ ] Import in `theme_handlers/__init__.py`  
      _Example:_ `from .your_theme_handler import YourThemeHandler`
- [ ] Registration in `mega_prompt_V3.py`

---

## Step-by-Step Implementation

### 1. Create Handler File

```python
# filepath: Core_Nodes/theme_handlers/your_theme_handler.py
from typing import Dict
from .base_handler import BaseThemeHandler

class YourThemeHandler(BaseThemeHandler):
    """Handler for your custom theme."""

    def generate(
        self,
        custom_subject: str = "",
        custom_location: str = "",
        include_environment: bool = True,
        include_style: bool = True,
        include_effects: bool = True
    ) -> Dict[str, str]:
        """Generates prompt components for the theme."""

        components = {}

        # Subject
        if custom_subject:
            components["subject"] = (
                f"((themed {custom_subject})), ((main attribute)), ((supporting detail))"
            )
        else:
            main_element = self._get_random_choice("your_theme.main_elements")
            components["subject"] = f"((themed {main_element})), ((supporting detail))"

        # Environment
        if include_environment:
            if custom_location:
                components["environment"] = f"in ((themed {custom_location}))"
            else:
                setting = self._get_random_choice("your_theme.settings")
                components["environment"] = f"in ((themed {setting}))"
        else:
            components["environment"] = ""

        # Style
        if include_style:
            style = self._get_random_choice("your_theme.styles")
            components["style"] = f"in the style of ((themed {style}))"
        else:
            components["style"] = ""

        # Effects
        if include_effects:
            effect = self._get_random_choice("your_theme.effects")
            components["effects"] = f"with ((themed {effect}))"
        else:
            components["effects"] = ""

        return components
```

### 2. Create Config File

```json
{
  "your_theme": {
    "main_elements": ["example1", "example2"],
    "settings": ["settingA", "settingB"],
    "styles": ["art nouveau", "cyberpunk"],
    "effects": ["soft lighting", "dramatic shadows"]
  }
}
```

---

## Registration in `mega_prompt_V3.py`

```python
# Update these methods to add your theme:
def _init_handlers(self):
    handler_classes = {
        # ...existing handlers...
        "your_theme": YourThemeHandler,
    }

def _init_mappings(self):
    emoji_mappings = {
        # ...existing mappings...
        "🎨 Your Theme": "your_theme"
    }
```

---

## Example: 🚀 Space Colony Theme

### Handler File

```python
# filepath: Core_Nodes/theme_handlers/space_colony_handler.py
from typing import Dict
from .base_handler import BaseThemeHandler

class SpaceColonyHandler(BaseThemeHandler):
    """Handler for the Space Colony theme."""

    def generate(
        self,
        custom_subject: str = "",
        custom_location: str = "",
        include_environment: bool = True,
        include_style: bool = True,
        include_effects: bool = True
    ) -> Dict[str, str]:
        """Generates prompt components for the Space Colony theme."""

        components = {}

        # Subject
        if custom_subject:
            components["subject"] = (
                f"((space colony {custom_subject})), ((main structure)), ((supporting detail))"
            )
        else:
            main_element = self._get_random_choice("space_colony.main_elements")
            components["subject"] = f"((space colony {main_element})), ((supporting detail))"

        # Environment
        if include_environment:
            if custom_location:
                components["environment"] = f"in ((space environment {custom_location}))"
            else:
                setting = self._get_random_choice("space_colony.settings")
                components["environment"] = f"in ((space environment {setting}))"
        else:
            components["environment"] = ""

        # Style
        if include_style:
            style = self._get_random_choice("space_colony.styles")
            components["style"] = f"in the style of (({style}))"
        else:
            components["style"] = ""

        # Effects
        if include_effects:
            effect = self._get_random_choice("space_colony.effects")
            components["effects"] = f"with (({effect}))"
        else:
            components["effects"] = ""

        return components
```

### Config File

```json
{
  "space_colony": {
    "main_elements": [
      "dome habitat",
      "hydroponic farm",
      "command center",
      "solar array",
      "terraforming module"
    ],
    "settings": [
      "lunar surface",
      "Martian desert",
      "asteroid belt",
      "orbiting space station",
      "icy moon"
    ],
    "styles": [
      "sleek futuristic",
      "brutalist architecture",
      "biophilic design",
      "retro sci-fi",
      "high-tech minimalism"
    ],
    "effects": [
      "glowing neon lights",
      "dust storms",
      "starfield backdrop",
      "artificial gravity",
      "transparent domes"
    ]
  }
}
```

### Registration in `mega_prompt_V3.py`

```python
def _init_handlers(self):
    handler_classes = {
        # ...existing handlers...
        "space_colony": SpaceColonyHandler,
    }

def _init_mappings(self):
    emoji_mappings = {
        # ...existing mappings...
        "🚀 Space Colony": "space_colony"
    }
```

### Import in `theme_handlers/__init__.py`

```python
from .space_colony_handler import SpaceColonyHandler
```

---

## Common Errors & Solutions

1. **"Handler not found" error:**
   - Double-check the handler filename (no double underscores).
   - Verify the import statement in `theme_handlers/__init__.py` (e.g., `from .your_theme_handler import YourThemeHandler`).
   - Ensure the handler is correctly registered in `_init_handlers` in `mega_prompt_V3.py`.
   - **If you see a Python import error:** Check for typos or missing files in the `theme_handlers` directory.

2. **"Config not found" error:**
   - Ensure the config file is named `your_theme.json`.
   - Verify the file is located in the `Core_Nodes/configs/` directory.
   - Remove any JSON comments or trailing commas.  **JSON is strict!**  
     _Tip: Use a JSON validator if unsure._

3. **"Theme not appearing" error:**
   - Check `_init_handlers` and `_init_mappings` in `mega_prompt_V3.py` for correct registration.
   - Restart ComfyUI after making changes to ensure the new theme is loaded.
   - Check the ComfyUI console for any error messages related to theme loading.
   - The theme should appear in the Mega Prompt Generator V3 dropdown menu.

4. **Empty or unexpected results:**
   - Inspect the `generate()` method in your handler.  Are you returning the expected components?
   - Check the values in your `your_theme.json` file.  Are they valid and appropriate for your theme?
   - Test with different parameter combinations (e.g., `custom_subject`, `custom_location`, toggling environment/style/effects).

---

## Additional Tips & Reminders

- **Restart Required:**  
  After adding or modifying handler/config files, always restart ComfyUI to reload all themes and avoid caching issues.

- **File Placement:**  
  Place your handler file in `Core_Nodes/theme_handlers/` and your config file in `Core_Nodes/configs/`.

- **Python Syntax:**  
  Use a code editor with Python syntax checking to avoid indentation or syntax errors in your handler file.

- **Handler Inheritance:**  
  Your handler class must inherit from `BaseThemeHandler` for compatibility.

- **Random Choice Methods:**  
  Use `_get_random_choice` for standard random selection, or `_safe_choice` if you want to provide a fallback value.

- **Docstrings & Comments:**  
  Add docstrings and comments to your handler for clarity and maintainability.

- **Updating Existing Themes:**  
  To update a theme, edit the handler or config file, then restart ComfyUI. You can add new elements to the config or extend the handler logic as needed.

---

## Naming Conventions

- **Handler class**: Use `PascalCase` (e.g., `MedievalThemeHandler`).
- **Internal name**: Use `snake_case` (e.g., `medieval_theme`).
- **Display name**: Include an emoji + title case (e.g., `🎨 Medieval Theme`).
- **Config key**: Should match the internal name (e.g., `"medieval_theme": {...}`).

---

## Testing Steps

1. Create all files in the correct directories.
2. Restart ComfyUI to reload handlers.
3. Verify console logs for errors.
4. Test with:
   ```python
   prompt = handler.generate(custom_subject="medieval castle")
   print(prompt) # Inspect the generated prompt
   ```
5. Check the dropdown menu in ComfyUI for your theme name (Mega Prompt Generator V3 node).
6. Experiment with different `custom_subject` values and other parameters to ensure the theme integrates correctly.

---

## Advanced Customization

* **Conditional Logic:**  Add more complex logic to your `generate()` method to handle different scenarios or user inputs.
* **Weighted Random Choices:**  Use the `_get_random_choice()` method with weights to favor certain elements over others.
* **External Data:**  Load data from external files (e.g., text files, databases) to expand the possibilities of your theme.
* **Custom Parameters:** Add more parameters to the `generate()` method to allow users to fine-tune the theme.

---

## Best Practices

- Use double parentheses `(( ))` for emphasis.
- Provide fallback values to avoid missing data.
- Handle custom subjects gracefully.
- Keep your code clean and well-documented.
- Test your theme thoroughly before sharing it with others.

---

**Example Theme**: Medieval architecture with stained glass and grand halls.

```json
{
  "your_theme": {
    "main_elements": ["castle", "abbey", "cathedral"],
    "settings": ["forest glade", "snow-covered mountains", "rolling hills"],
    "styles": ["gothic", "romanesque", "byzantine"]
  }
}
```

**Example Theme**: "Starter Pack" figurine in a blister pack.

```json
{
  "starter_pack": {
    "names": ["Alex", "Jordan"],
    "genders": ["man", "woman"],
    "physical_traits": ["tall and athletic", "with glasses"],
    "jobs": ["developer", "artist"],
    "passions": ["hiking", "reading"],
    "objects": ["a laptop and headphones", "a sketchbook and pencils"],
    "styles": ["cartoon", "comic book"]
  }
}
```

---

🚀 **Ready to create your theme?** Follow this guide strictly for seamless integration with ComfyUI!