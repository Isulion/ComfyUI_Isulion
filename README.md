# Mega Prompt Generator Node

The Mega Prompt Generator is a sophisticated ComfyUI node that generates detailed, thematic prompts for image generation. It supports multiple themes and styles with extensive customization options.

![Showcase](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/82d13074-b383-49ab-a19f-5633c8c109a5/original=true,quality=90/Batman_v3.jpeg)
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

## 🎯 Mega Prompt Generator 🎯

### Supported Themes  

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
- 🏺 Clay Art
- 🖌️ Crayon Art
- 🍳 Culinary/Food
- 👗 Curvy Fashion
- 💠 Dimension 3D
- 🖼️ Digital Art
- ✨ Enchanted Fantasy
- 📸 Essential Realistic
- 💥 Futuristic Battlefield
- 🌆 Futuristic City Metropolis
- 🚀 Futuristic Sci-Fi
- 🎨 Impressionist
- 👻 Halloween Ethereal
- 🎭 Horror
- 👙 Instagram Lifestyle
- 🏠 Interior Spaces
- 🏷️ Logo
- 📖 Manga Panel
- 🦸‍♂️ Marvel Universe
- 🔬 Microscopic Universe
- 🎭 Peaky Blinders Style
- 💫 Pixar Animation
- ☢️ Post-Apocalyptic Wasteland
- 🌌 Quantum Weapons
- 🏫 School Manga
- 📱 Selfie
- 🖤 Star Wars Universe
- ⚙️ Steampunk Cities
- 🌸 Studio Ghibli
- 🌊 Underwater Civilization
- 🎨 Urban Tag
- 🏘️ Village Of the World
- 🧸 Vintage Anthropomorphic

### Input Parameters

- **Theme**: Select from 40+ themed generators
- **Complexity**: Choose between simple, detailed, or complex outputs
- **Randomization**: Enable/disable random generation
- **Custom Inputs**:
- ![Custom Subject and location example](https://github.com/user-attachments/assets/10e6a34d-b509-48e7-bac5-7a8c78615371)
  - Custom Subject: Define specific subjects
  - Custom Location: Specify scene locations

## 🖼️ Load Images Node

The Load Images node allows you to load multiple images from a specified directory, making it easy to work with batches of images in your workflow.

## 🎭 Image Collage Node

The Image Collage node enables you to create visually appealing collages from multiple input images, perfect for showcasing collections or creating mood boards.

## Specific Nodes

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

### 🔧 Enhancement Nodes

- 📝 Prompt Enhancer - More details, mood, composition, lighting, or color enhancements
- ⛔ Negative Prompt - Creates matching negative prompts with adjustable strictness
- 🎨 Style Mixer - Combines multiple art styles with adjustable blend modes

--------------

## Directory Structure

```
ComfyUI_Isulion/
├── Core_Nodes/         # Core functionality nodes
├── animals_nodes/      # Animal-related node implementations
├── character_nodes/    # Character generation nodes
├── configs/           # Configuration files
├── enhancement_nodes/ # Enhancement and improvement nodes
├── fantasy_nodes/    # Fantasy-themed node implementations
├── scene_nodes/      # Scene generation nodes
├── scifi_nodes/      # Science fiction themed nodes
├── theme_handlers/   # Theme-specific handling logic
├── isucollage_node.py   # Collage generation functionality
├── load_images_node.py  # Image loading utilities
└── mega_prompt_V3.py    # Latest version of Mega Prompt generator
```

--------------

## FLUX Worflow (old) Examples

[More Workflows and Examples](https://civitai.com/articles/8673/discover-the-mega-prompt-generator-for-comfyui)

### Basic MegaPrompt (old) Workflow

![IsulionFLUX_00468_](https://github.com/user-attachments/assets/91e7db26-9315-45d3-8461-83f0bba457b1)

### Chimera (with Ollama) (old) Workflow

![IsulionFlux_00492_](https://github.com/user-attachments/assets/0e097a70-3821-4440-94d9-589703ab7ad1)

### MegaPrompt + Ollama + LoRa (old) Workflow

![IsulionFLUX_00484_](https://github.com/user-attachments/assets/6cbc3ea8-650b-44b3-9a59-a3476a7e513c)
[LoRa used for this](https://civitai.com/models/673513/will-smith-flux-dev-lora)

## 🦙 Ollama Requirements

- Ollama_generator node installed in ComfyUI

### Environment Variables

- OLLAMA_KEEP_ALIVE: 0
- OLLAMA_ORIGINS: *
