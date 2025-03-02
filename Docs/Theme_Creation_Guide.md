# Theme Creation Guide  
🎨 Create Custom Themes for ComfyUI  

## Required Directory Structure  
```bash
ComfyUI/
├── Core_Nodes/                     # Core module directory
│   ├── theme_handlers/            # Handler files directory
│   │   └── your_theme_handler.py  # Your handler file
│   └── configs/                   # Config files directory
│       └── your_theme.json        # Your config file
└── mega_prompt_V3.py              # Registration file
```

---

## Critical Naming Rules  
1. **Handler filename**: `Core_Nodes/theme_handlers/your_theme_handler.py` (no double underscores).  
2. **Config filename**: `Core_Nodes/configs/your_theme.json`.  
3. Use **consistent internal names** (`your_theme`) across all files.  

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

1. **"Handler not found" error**  
   - Check the handler filename (`no double underscores`).  
   - Verify import in `__init__.py` and registration steps.  

2. **"Config not found" error**  
   - Ensure config file is named `your_theme.json`.  
   - Remove any JSON comments or trailing commas.  

3. **"Theme not appearing" error**  
   - Check `_init_handlers` and `_init_mappings` for correct registration.  

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
   ```
5. Check dropdown menu for your theme name.  

---

## Best Practices  
- Use double parentheses `((  ))` for emphasis.  
- Provide fallback values to avoid missing data.  
- Handle custom subjects gracefully.  

--- 

**Example Theme**: Medieval architecture with stained glass and grand halls.  
```json
{
    "your_theme": {
        "main_elements": ["castle", "abbey"],
        "settings": ["forest glade", "snow-covered mountains"]
    }
}
```

---

🚀 **Ready to create your theme?** Follow this guide strictly for seamless integration with ComfyUI!