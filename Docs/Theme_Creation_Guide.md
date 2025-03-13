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

---

## Required Files Checklist

- [ ] Handler file: `your_theme_handler.py`
- [ ] Config file: `your_theme.json`
- [ ] Import in `theme_handlers/__init__.py`
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

    def generate(self,
                 custom_subject: str = "",
                 custom_location: str = "",
                 include_environment: str = "yes",
                 include_style: str = "yes",
                 include_effects: str = "yes") -> Dict[str, str]:
        """Generates prompt components for the theme."""

        components = {}

        # Required: Subject generation
        if custom_subject:
            components["subject"] = (
                f"((themed {custom_subject})), "
                f"((main attribute)), ((supporting detail))"
            )
        else:
            main_element = self._get_random_choice("your_theme.main_elements")
            components["subject"] = f"((themed {main_element})), ((supporting detail))"

        # Optional: Environment
        if include_environment == "yes":
            setting = self._get_random_choice("your_theme.settings")
            components["environment"] = f"in ((themed {setting}))"

        # Optional: Style (example - expand as needed)
        if include_style == "yes":
            style = self._get_random_choice("your_theme.styles")
            components["style"] = f"in the style of ((themed {style}))"

        return components
```

### 2. Create Config File

```json
{
  "your_theme": {
    "main_elements": [
      "example1",
      "example2"
    ],
    "settings": [
      "settingA",
      "settingB"
    ],
    "styles": [
      "art nouveau",
      "cyberpunk",
      "impressionism"
    ]
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

## Common Errors & Solutions

1. **"Handler not found" error:**
   - Double-check the handler filename (no double underscores).
   - Verify the import statement in `theme_handlers/__init__.py` (e.g., `from .your_theme_handler import YourThemeHandler`).
   - Ensure the handler is correctly registered in `_init_handlers` in `mega_prompt_V3.py`.

2. **"Config not found" error:**
   - Ensure the config file is named `your_theme.json`.
   - Verify the file is located in the `Core_Nodes/configs/` directory.
   - Remove any JSON comments or trailing commas.  JSON is strict!

3. **"Theme not appearing" error:**
   - Check `_init_handlers` and `_init_mappings` in `mega_prompt_V3.py` for correct registration.
   - Restart ComfyUI after making changes to ensure the new theme is loaded.
   - Check the ComfyUI console for any error messages related to theme loading.

4. **Empty or unexpected results:**
   - Inspect the `generate()` method in your handler.  Are you returning the expected components?
   - Check the values in your `your_theme.json` file.  Are they valid and appropriate for your theme?

---

## Naming Conventions

- **Handler class**: Use `PascalCase` (e.g., `MedievalThemeHandler`).
- **Internal name**: Use `snake_case` (e.g., `medieval_theme`).
- **Display name**: Include an emoji + title case (e.g., `🎨 Medieval Theme`).

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
5. Check the dropdown menu in ComfyUI for your theme name.
6. Experiment with different `custom_subject` values to ensure the theme integrates correctly.

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

---

🚀 **Ready to create your theme?** Follow this guide strictly for seamless integration with ComfyUI!