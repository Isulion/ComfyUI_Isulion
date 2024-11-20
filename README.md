# Mega Prompt Generator Node

The Mega Prompt Generator is a sophisticated ComfyUI node that generates detailed, thematic prompts for image generation. It supports multiple themes and styles with extensive customization options.

![Showcase](https://github.com/user-attachments/assets/56d69f0a-d840-42de-93ef-5378293263ee)
[Source](https://civitai.com/user/Isulion/images?sort=Newest)

## Installation

### Quick Start

Use [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager), got to "<span style="color: #00ff00">Custome Nodes Manager</span>" and search  "<span style="color: #00ff00">Isulion</span>" !

### Old install

```bash
cd "your_ComfyUI_install_dir"
cd custom_nodes
git clone https://github.com/Isulion/ComfyUI_Isulion
```

--------------

## Available Nodes

### Core Generators

- 💡 **Mega Prompt V2** - Latest version with enhanced features and organization
- 💡 **Mega Prompt** - Advanced multi-theme prompt generator
- 💻 Prompt - Main prompt generation node

## 🎯 Mega Prompt V2 🎯

The Mega Prompt V2 is an enhanced version of the original generator with improved organization and additional features. It provides more granular control over prompt generation and better theme handling.

### New Features in V2

- **Enhanced Theme Organization**: Better structured theme handling with dedicated handlers for each theme
- **Improved Component Control**: Separate toggles for environment, style, and effects
- **Custom Location Support**: Added ability to specify custom locations for more precise scene setting
- **Expanded Theme Support**: Now includes 35+ distinct themes
- **Improved Configuration System**: Better organized config file with expanded options

### Supported Themes in V2

- 🎲 Dynamic Random (Default)
- 🎨 Abstract
- 📺 Animation Cartoon
- 🎌 Anime
- 🏛️ Architectural
- 🧬 Bio-Organic Technology
- 🖼️ Binet Surreal
- ✏️ Caricature
- 🦄 Chimera Animals
- 🐰 Chimera Cute Animals
- 🎅 Christmas
- 🎬 Cinema Studio
- 🍳 Culinary/Food
- 👗 Curvy Fashion
- 💠 Dimension 3D
- ✨ Enchanted Fantasy
- 📸 Essential Realistic
- 🌆 Futuristic City Metropolis
- 🚀 Futuristic Sci-Fi
- 👻 Halloween Ethereal
- 👙 Instagram Lifestyle
- 🏠 Interior Spaces
- 🏷️ Logo
- 📖 Manga Panel
- 🦸‍♂️ Marvel Universe
- 🔬 Microscopic Universe
- 🎭 Peaky Blinders Style
- 💫 Pixar Animation
- ☢️ Post-Apocalyptic Wasteland
- 🏫 School Manga
- 📱 Selfie
- 🖤 Star Wars Universe
- ⚙️ Steampunk Cities
- 🌊 Underwater Civilization
- 🏘️ Village Of the World
- 🧸 Vintage Anthropomorphic

### Input Parameters

- **Theme**: Select from 35+ themed generators
- **Complexity**: Choose between simple, detailed, or complex outputs
- **Randomization**: Enable/disable random generation
- **Custom Inputs**:
  - Custom Subject: Define specific subjects
  - Custom Location: Specify scene locations
  - Include Environment: Toggle environment descriptions
  - Include Style: Toggle style elements
  - Include Effects: Toggle special effects
- **Seed**: Control randomization with specific seeds

### Outputs

- **Complete Prompt**: The full generated prompt
- **Individual Components**:
  - Subject: Main focus of the image
  - Environment: Scene and location details
  - Style: Artistic style and rendering approach
  - Effects: Special effects and enhancements
- **Seed**: The seed used for generation

### Theme-Specific Features

Each theme in V2 comes with dedicated handlers that provide:

- Theme-specific vocabulary and terminology
- Specialized composition elements
- Custom effect combinations
- Appropriate style modifiers
- Theme-relevant environmental details

### Enhanced Configuration

The V2 configuration system includes

- Expanded vocabulary lists
- Theme-specific element collections
- Detailed style variations
- Enhanced effect combinations
- Improved color palettes
- Specialized lighting setups
- Cultural variations
- Mood and atmosphere options

### Specific Nodes

- 🦊 Animal Behavior - Animal actions and poses
- 🦁 Animal - General animal selection
- 🐱 Cute Animal - Cute and baby animal selection
- 👔 Clothing Style - Outfit and fashion descriptions
- 👨‍🍳 Character Profession - Occupations and roles
- 🧝‍♂️ Fantasy Race - Fantasy species and races
- ⚔️ Action - Dynamic poses and activities
- 🎥 Scene Composition - Camera angles and shot types
- 🌲 Habitat - Natural environments and landscapes
- 🌅 Time of Day - Time and lighting conditions
- ⛅ Weather - Weather conditions
- 🖌️ Art Style - Artistic styles and techniques
- 😊 Emotion - Emotional characteristics
- 🏰 Artifact - Magical items and artifacts
- 🌟 Magical Effect - Spell effects and magical phenomena
- 🏰 Mythical Location - Fantasy environments
- 🪐 Alien World - Exotic planet environments
- 🛸 Spacecraft - Space vehicle descriptions
- 🤖 Tech - Futuristic technology descriptions

#### 🔧 Enhancement Nodes

- 📝 Prompt Enhancer - More details, mood, composition, lighting, or color enhancements
- ⛔ Negative Prompt - Creates matching negative prompts with adjustable strictness
- 🎨 Style Mixer - Combines multiple art styles with adjustable blend modes

--------------

## FLUX Worflow Examples

[More Workflows and Examples](https://civitai.com/articles/8673/discover-the-mega-prompt-generator-for-comfyui)

### Basic MegaPrompt Workflow

![IsulionFLUX_00468_](https://github.com/user-attachments/assets/91e7db26-9315-45d3-8461-83f0bba457b1)

### Chimera (with Ollama) Work

![IsulionFlux_00492_](https://github.com/user-attachments/assets/0e097a70-3821-4440-94d9-589703ab7ad1)

### MegaPrompt + Ollama + LoRa Workflow

![IsulionFLUX_00484_](https://github.com/user-attachments/assets/6cbc3ea8-650b-44b3-9a59-a3476a7e513c)
[LoRa used for this](https://civitai.com/models/673513/will-smith-flux-dev-lora)

## 🦙 Ollama Requirements

- Ollama_generator node installed in ComfyUI

### Environment Variables

- OLLAMA_KEEP_ALIVE: 0
- OLLAMA_ORIGINS: *
