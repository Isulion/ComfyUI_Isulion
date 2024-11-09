# Isulion Prompt Generator

Transform your creative workflow with advanced prompt generation technology.

![Showcase](https://github.com/user-attachments/assets/56d69f0a-d840-42de-93ef-5378293263ee)
[Source](https://civitai.com/user/Isulion/images?sort=Newest)

## Overview

Isulion Prompt Generator introduces a new way to create, refine, and enhance your image generation prompts. With its intuitive interface and powerful capabilities, you can craft precise, detailed prompts for any creative vision.

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

### Theme Categories

#### Core Themes

- 🎨 **Abstract**: Pure geometric and non-representational compositions
- 🎲 **Dynamic Random** (Default): Intelligently combines elements from various themes
- 📸 **Essential Realistic**: Professional photography with real-world subjects

#### Character Themes

- 🖼️ **Binet Surreal**: Anthropomorphic portraits inspired by Sylvain Binet
- 🦄 **Chimera Strange Animals**: Unique hybrid creatures with distinctive head-body combinations
- 🐰 **Fusion Cute Animals**: Adorable hybrid creature combinations
- 🎭 **Peaky Blinders Style**: 1920s gangster-themed anthropomorphic characters in period-accurate settings
- 🎩 **Vintage Anthropomorphic**: Photorealistic Victorian-era anthropomorphic characters

#### Environment Themes

- 🏛️ **Architectural**: Sophisticated building and structural designs
- 🌆 **Metropolis Futuristic City**: Advanced cityscape and urban environments
- 🔬 **Microscopic Universe**: Scientific visualizations of cellular and molecular landscapes
- 🏠 **Spaces Interior**: Interior design and architectural spaces
- 🌊 **Underwater Civilization**: Deep sea architecture and bioluminescent environments

#### Style Themes

- 📺 **Animation Cartoon**: Classic animated character styles
- 🎌 **Anime**: Japanese animation inspired artwork
- 🎅 **Christmas**: Magical holiday scenes with festive elements and decorations
- 🍳 **Culinary**: Professional food photography with elegant plating and styling
- 💠 **Dimension 3D**: Three-dimensional digital artwork
- 📱 **Lifestyle Instagram**: Professional social media photography
- 💫 **Pixar Animation**: 3D animation in the style of Pixar

#### Genre Themes

- 🧬 **Bio-Organic Technology**: Fusion of biological organisms with mechanical systems
- ✨ **Enchanted Fantasy**: Magical realms and mythical characters
- 👻 **Ethereal Halloween**: Spooky and atmospheric horror themes
- 🚀 **Futuristic Sci-Fi**: Advanced technology and space-age scenes
- ☢️ **Post-Apocalyptic Wasteland**: Dramatic scenes of survival in ruins
- ⚙️ **Steampunk World**: Victorian-era technology with brass and copper details

#### Franchise Themes

- 🦸‍♂️ **Marvel Universe**: Epic scenes featuring Marvel superheroes and villains
- 🎬 **Studio Cinema**: Movie and superhero character compositions
- ⭐ **Star Wars Universe**: Scenes and characters from the Star Wars galaxy

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

- 📝 Prompt Enhancer - Adds detail, mood, composition, lighting, or color enhancements
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
