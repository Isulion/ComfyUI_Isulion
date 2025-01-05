# Theme_Creation_Guide

This file is here to help you to create a new theme for the megaprompts nodes collection.
If you need to create a new theme, start by copying existing working theme.

## Important Notes
- Theme handlers should be placed directly in `theme_handlers/` directory (not in subdirectories)
- All themes must have matching config and handler names
- Always include proper error handling and fallbacks

## Directory Structure

```
ComfyUI_Isulion/
└── Core_Nodes/
    ├── theme_handlers/
    │   └── your_theme_handler.py    # Direct in handlers directory
    └── configs/
        └── your_theme_config.json
```

## Required Files

1. Theme Handler (`theme_handlers/your_theme_handler.py`)
2. Configuration File (`configs/your_theme_config.json`)
3. Entry in `mega_prompt_V3.py`

## Implementation Steps

### 1. Theme Handler Creation
```python
from .base_handler import BaseThemeHandler

class YourThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("your_theme")
        if not self.theme_config:
            raise ValueError("Missing your_theme configuration")
    
    def validate_config(self):
        """Validate theme configuration"""
        required_sections = ['primary_elements', 'settings', 'styles']
        for section in required_sections:
            if section not in self.theme_config:
                raise ValueError(f"Missing required section: {section}")
            if not isinstance(self.theme_config[section], list):
                raise ValueError(f"Section {section} must be a list")
    
    def get_fallback_value(self, section):
        """Provide fallback values for missing sections"""
        fallbacks = {
            'primary_elements': ['default element'],
            'settings': ['natural setting'],
            'styles': ['realistic style']
        }
        return fallbacks.get(section, [])
```

### 2. Create Config File
```json
{
    "your_theme": {
        "primary_elements": ["..."],
        "settings": ["..."],
        "styles": ["..."],
        "effects": ["..."],
        "atmosphere": ["..."],
        "ambiance": ["..."]
    }
}
```

### 3. Register Theme
```python
# In mega_prompt_V3.py
def _init_handlers(self):
    handler_classes = {
        # ...existing code...
        "your_theme": YourThemeHandler,
    }

def _init_mappings(self):
    emoji_mappings = {
        # ...existing code...
        "🎨 Your Theme": "your_theme",
    }
```

## Example Implementation: Historical Monuments Theme

Here's a working example of how to create a new theme:

### 1. Theme Handler Creation
Place in `theme_handlers/historical_monuments_handler.py`:
```python
from typing import Dict
from .base_handler import BaseThemeHandler

class HistoricalMonumentsHandler(BaseThemeHandler):
    """Handler for historical monuments theme generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        components = {}
        
        # Subject generation with proper weighting
        if custom_subject:
            components["subject"] = (
                f"((majestic {custom_subject})), "
                f"((architectural masterpiece)), ((monumental scale))"
            )
        else:
            monument = self._get_random_choice("historical_monuments.monuments")
            components["subject"] = f"((majestic {monument})), ((architectural masterpiece))"
        
        # Add optional components
        if include_environment == "yes":
            era = self._get_random_choice("historical_monuments.eras")
            setting = self._get_random_choice("historical_monuments.settings")
            components["environment"] = f"in ((historic {setting})), during ((the {era}))"
            
        # ... rest of implementation
```

### 2. Config Structure
Place in `configs/historical_monuments_config.json`:
```json
{
    "historical_monuments": {
        "monuments": ["Pyramids of Giza", "Parthenon", "Colosseum", ...],
        "eras": ["Ancient Egyptian Era", "Classical Antiquity", ...],
        "settings": ["ancient city", "royal court", ...],
        "artistic_styles": ["historical painting", "architectural illustration", ...],
        "lighting": ["golden hour", "dramatic sunset", ...],
        "atmosphere": ["mystical fog", "ancient dust", ...]
    }
}
```

### 3. Theme Registration
Add to `mega_prompt_V3.py`:
```python
def _init_handlers(self):
    handler_classes = {
        // ...existing code...
        "historical_monuments": HistoricalMonumentsHandler,
    }

def _init_mappings(self):
    emoji_mappings = {
        // ...existing code...
        "🏛️ Historical Monuments": "historical_monuments",
    }
```

## Prompt Structure

### Component Guidelines
1. Subject (Required)
```python
f"({main_element:1.3}), ({supporting_detail:1.2}), {composition}"
```

2. Environment (Optional)
```python
f"in {setting}, during {time}, with {atmosphere}"
```

3. Style (Optional)
```python
f"{style}, {technique}, ({additional_elements:1.1})"
```

4. Effects (Optional)
```python
f"((main effect:1.2)), ((supporting effects)), ((enhancements))"
```

### Configuration Validation

1. Required Structure:
```json
{
    "your_theme": {
        "primary_elements": ["at least 3 items"],
        "settings": ["at least 3 items"],
        "styles": ["at least 3 items"]
    }
}
```

2. Validation Rules:
- All sections must be lists
- Lists should contain unique items
- No empty strings allowed
- Minimum 3 items per required section

## Testing Checklist

- [ ] Handler loads without errors
- [ ] Config file is properly formatted
- [ ] All required sections exist in config
- [ ] Prompt generation works with:
  - Default settings
  - Custom subjects
  - Different component combinations
- [ ] Weights are balanced
- [ ] Error handling works

## Common Issues & Solutions

1. Theme not appearing:
   - Check handler is in correct directory
   - Verify registration in mega_prompt_V3.py
   - Ensure config key matches handler

2. Missing config errors:
   - Add all required sections
   - Match config key with handler
   - Include fallback values

3. Generation issues:
   - Check component building methods
   - Verify prompt structure
   - Test weight values

## Best Practices

1. Config Organization:
   - Use clear category names
   - Include 5-10 items per category
   - Group related elements

2. Error Handling:
   - Validate configurations
   - Provide fallbacks
   - Clear error messages

3. Naming Conventions:
   - Use snake_case for internal names
   - Clear, descriptive display names
   - Include relevant emoji

## Additional Best Practices

1. Component Organization:
   - Group related elements in config
   - Use clear, descriptive section names
   - Include 10-15 items per category for variety

2. Prompt Structure:
   - Use double parentheses for emphasis ((like this))
   - Keep weights balanced
   - Group related concepts together

3. Testing:
   - Test with both custom and default subjects
   - Verify all optional components work
   - Check prompt generation with different combinations
