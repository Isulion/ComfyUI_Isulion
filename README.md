# ComfyUI_Isulion Random Prompt Generator

--------------

ComfyUI Nodes that generate prompts with the help of LLM from local or remote Ollama.

--------------

# Requirement:

Recommended environment variables:
- OLLAMA_KEEP_ALIVE  	0
- OLLAMA_ORIGINS		*

ComfyUI installed node:
- Ollama_generator 

# Installation:

- cd your_ComfyUI_install_dir
- cd custom_nodes
- git clone https://github.com/Isulion/ComfyUI_Isulion

--------------

# Available Nodes:

## Core Generators
- Prompt  ✨ - Main prompt generation node
- Ollama  🤖 - LLM-based text generation
- Mega Prompt 🎯 - Advanced multi-theme prompt generator

## Mega Prompt Generator 🎯
The Mega Prompt Generator is an advanced node that combines multiple themes and generation capabilities:

### Available Themes:
- Fantasy: Epic fantasy scenes and characters
- Sci-Fi: Futuristic and technological scenes
- Realistic: Real-world photography style
- Cute Chimera: Hybrid cute animal combinations
- Cinema: Movie and superhero characters
- Cartoon: Classic animated characters
- Anime: Anime-style artwork
- Architecture: Building and structural designs
- Abstract: Pure abstract art compositions
- Food: Culinary and food photography
- Interior: Interior design and spaces
- 3D: Three-dimensional artwork
- Halloween: Spooky and horror themes
- Instagram: Social media influencer photography
- Random: Randomly selects from available themes

### Features:
- Theme-specific prefixes and styles
- Professional photography settings for relevant themes
- Adjustable complexity (simple/detailed/complex)
- Component control (subject/action/environment/style/effects)
- Randomization options
- Separate outputs for each prompt component

### Example Usage:
1. Select a theme
2. Choose complexity level
3. Enable/disable components as needed
4. Use randomization for variety
5. Connect to your preferred image generation node

The Mega Prompt Generator provides both a combined prompt and individual components, allowing for maximum flexibility in your workflows.

## Specific Nodes

### Animal Related
- Animal 🦁 - General animal selection
- Cute Animal 🐱 - Cute and baby animal selection
- Animal Behavior 🦊 - Animal actions and poses

### Character Elements
- Character Profession 👨‍🍳 - Occupations and roles
- Fantasy Race 🧝‍♂️ - Fantasy species and races
- Clothing Style 👔 - Outfit and fashion descriptions

### Scene Composition
- Action ⚔️ - Dynamic poses and activities
- Scene Composition 🎬 - Camera angles and shot types

### Environment
- Habitat 🌲 - Natural environments and landscapes
- Weather ⛅ - Weather conditions
- Time of Day 🌅 - Time and lighting conditions

### Style and Mood
- Art Style 🎨 - Artistic styles and techniques
- Emotion 😊 - Emotional characteristics

### Fantasy & Magic
- Magical Effect ✨ - Spell effects and magical phenomena
- Mythical Location 🏰 - Fantasy environments
- Artifact 📿 - Magical items and artifacts

### Sci-Fi Elements
- Tech 🤖 - Futuristic technology descriptions
- Alien World 🪐 - Exotic planet environments
- Spacecraft 🚀 - Space vehicle descriptions

### Enhancement Nodes
- Style Mixer 🎨 - Combines multiple art styles with adjustable blend modes
- Prompt Enhancer 📝 - Adds detail, mood, composition, lighting, or color enhancements
- Negative Prompt ⛔ - Creates matching negative prompts with adjustable strictness


# How to use:

## Basic Workflow
Use this example workflow to get started:

![Example_Isulion_Workflow](https://github.com/user-attachments/assets/ba6d7eaa-c068-4f88-a2c9-fb07aa95052b)

## Advanced Mode
For more flexibility and control:

![Example_Isulion_Workflow_Split](https://github.com/user-attachments/assets/e578ff7a-0c03-47a1-900f-a7e209a64914)

## Special Workflows
### Chimera Animals:
![workflowAnimals](https://github.com/user-attachments/assets/afd6916a-22d0-4c4b-9989-9b78b9eaf83f)

### Using Enhancement Nodes:
The enhancement nodes can be used to refine and improve your prompts:

1. **Style Mixer**: Combine two different art styles with control over their balance
   - Input two styles and choose blend mode (balanced/style1_dominant/style2_dominant)
   - Great for creating unique artistic combinations

2. **Prompt Enhancer**: Add specific improvements to your prompts
   - Choose enhancement level (subtle/moderate/dramatic)
   - Focus on specific aspects (detail/mood/composition/lighting/color)
   - Perfect for refining and elevating prompt quality

3. **Negative Prompt Generator**: Create matching negative prompts
   - Adjustable strictness levels (basic/standard/strict)
   - Automatically generates appropriate negative prompts
   - Helps prevent common artifacts and issues
