# Theme Creation Guide

## Critical File Naming
1. Handler file must be named: `theme_handlers/your_theme_handler.py`
2. Config file must be named: `configs/your_theme.json` (not `your_theme_config.json`)
3. Names must match exactly in all references

## Required Files Checklist
- [ ] Handler file: `your_theme_handler.py`
- [ ] Config file: `your_theme.json`
- [ ] Import in `__init__.py`
- [ ] Registration in `mega_prompt_V3.py`

## Step-by-Step Implementation

### 1. Create Handler File
```python
# filepath: /theme_handlers/your_theme_handler.py
from typing import Dict
from .base_handler import BaseThemeHandler

class YourThemeHandler(BaseThemeHandler):
    """Handler description."""
    
    def generate(self, custom_subject: str = "",
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
// filepath: /configs/your_theme.json  <-- Note: no "_config" in filename
{
    "your_theme": {  // <-- Must match handler name
        "main_elements": [
            "at least",
            "three items",
            "in each category"
        ],
        "settings": [
            "minimum",
            "three",
            "settings"
        ]
    }
}
```

### 3. Add to __init__.py
```python
// filepath: /theme_handlers/__init__.py
from .your_theme_handler import YourThemeHandler

__all__ = [
    // ...existing code...
    'YourThemeHandler',  # <-- Add to __all__ list
]
```

### 4. Register in mega_prompt_V3.py
```python
def _init_handlers(self):
    handler_classes = {
        // ...existing code...
        "your_theme": YourThemeHandler,  # <-- Internal name (snake_case)
    }

def _init_mappings(self):
    emoji_mappings = {
        // ...existing code...
        "🎨 Your Theme": "your_theme",  # <-- Display name with emoji
    }
```

## Common Errors & Solutions

1. "Handler not found" error:
   ```
   ✓ Check handler filename matches exactly
   ✓ Verify import in __init__.py
   ✓ Confirm handler class name matches import
   ```

2. "Config not found" error:
   ```
   ✓ Config filename should be "your_theme.json" (not "your_theme_config.json")
   ✓ Config key must match handler's internal name
   ✓ Place config file directly in configs/ directory
   ```

3. "Theme not appearing" error:
   ```
   ✓ Check emoji_mappings entry
   ✓ Verify handler registration in _init_handlers
   ✓ Ensure consistent naming across all files
   ```

## Naming Conventions
- Handler class: `PascalCase` (e.g., `MedievalThemeHandler`)
- Internal theme name: `snake_case` (e.g., `medieval`)
- Config file: `snake_case.json` (e.g., `medieval.json`)
- Display name: `Emoji Title Case` (e.g., `⚔️ Medieval`)

## Testing Steps
1. Create all required files
2. Restart ComfyUI
3. Check console for errors
4. Verify theme appears in dropdown
5. Test with custom and default subjects
6. Verify all optional components work

## Best Practices
- Keep consistent naming across all files
- Include comprehensive config categories
- Use double parentheses for emphasis `((like this))`
- Always handle custom subject cases
- Provide fallback values
- Add clear error messages
