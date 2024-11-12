# Mega Prompt Generator Node

The Mega Prompt Generator is a sophisticated ComfyUI node that generates detailed, thematic prompts for image generation. It supports multiple themes and styles with extensive customization options.

![Showcase](https://github.com/user-attachments/assets/56d69f0a-d840-42de-93ef-5378293263ee)
[Source](https://civitai.com/user/Isulion/images?sort=Newest)

## Installation

### Quick Start

Use [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager), got to "Custome Nodes Manager" and search  "Isulion" !

### Old install

```bash
cd "your_ComfyUI_install_dir"
cd custom_nodes
git clone https://github.com/Isulion/ComfyUI_Isulion
```

--------------

## Available Nodes

### Core Generators

- 💡 **Mega Prompt** - Advanced multi-theme prompt generator
- 💻 Prompt - Main prompt generation node

## 🎯 Mega Prompt Generator 🎯

The Mega Prompt Generator is an advanced node that combines multiple themes and generation capabilities. It provides both combined prompts and individual components for maximum flexibility in your workflows.

### Core Features

- **30 distinct themes including**
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
  - 💠 Dimension 3D
  - ✨ Enchanted Fantasy
  - 📸 Essential Realistic
  - 🌆 Futuristic City Metropolis
  - 🚀 Futuristic Sci-Fi
  - 👻 Halloween Ethereal
  - 📱 Instagram Lifestyle
  - 🏠 Interior Spaces
  - 🏷️ Logo
  - 🦸‍♂️ Marvel Universe
  - 🔬 Microscopic Universe
  - 🎭 Peaky Blinders Style
  - 💫 Pixar Animation
  - ☢️ Post-Apocalyptic Wasteland
  - ⭐ Star Wars Universe
  - ⚙️ Steampunk Cities
  - 🌊 Underwater Civilization
  - 🎩 Vintage Anthropomorphic
  - 🏘️ Villages of the World

- **Complexity Levels**:
  - Simple: Basic prompt with minimal elements
  - Detailed: Balanced prompt with key elements (default)
  - Complex: Rich prompt with additional details and effects

- **Enhancement System**:
  - Levels: Subtle, Moderate (default), Dramatic
  - Focus Areas: Detail, Composition, Lighting, Color

- **Customization**:
  - Custom Subject Input
  - Component Toggle (Subject, Action, Environment, Style, Effects)
  - Randomization Options
  - Seed Control

- **Configuration File**

  The node uses a configuration file (`config_mega.txt`) that contains all theme-specific elements and common components.

  You can modify the file to add elements:
  - Add new items to existing lists
  - Customize existing elements to match your needs

  The configuration file uses standard Python syntax for lists and dictionaries, making it easy to edit and maintain.

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

#### 🏘️ Villages of the World Theme
Captures the beauty and character of traditional villages and inspiring landscapes worldwide:
- Diverse village types from mountain settlements to coastal towns
- Traditional architecture and cultural elements
- Stunning natural landscapes and atmospheric conditions
- Cultural authenticity and environmental harmony
- Professional travel photography style
