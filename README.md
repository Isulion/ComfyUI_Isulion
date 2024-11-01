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
- Prompt Generator ✨ - Main prompt generation node
- Ollama Generate 🤖 - LLM-based text generation

## Animal Related
- Animal Selector 🦁 - General animal selection
- Cute Animal Selector 🐱 - Cute and baby animal selection
- Animal Behavior Generator 🦊 - Animal actions and poses

## Character Elements
- Character Profession 👨‍🍳 - Occupations and roles
- Fantasy Race Generator 🧝‍♂️ - Fantasy species and races
- Clothing Style Generator 👔 - Outfit and fashion descriptions

## Scene Composition
- Action Generator ⚔️ - Dynamic poses and activities
- Scene Composition 🎬 - Camera angles and shot types

## Environment
- Habitat Generator 🌲 - Natural environments and landscapes
- Weather Generator ⛅ - Weather conditions
- Time of Day Generator 🌅 - Time and lighting conditions

## Style and Mood
- Art Style Generator 🎨 - Artistic styles and techniques
- Emotion Generator 😊 - Emotional characteristics

## Fantasy & Magic
- Magical Effect Generator ✨ - Spell effects and magical phenomena
- Mythical Location Generator 🏰 - Fantasy environments
- Artifact Generator 📿 - Magical items and artifacts

## Sci-Fi Elements
- Tech Generator 🤖 - Futuristic technology descriptions
- Alien World Generator 🪐 - Exotic planet environments
- Spacecraft Designer 🚀 - Space vehicle descriptions

## Enhancement Nodes
- Style Mixer 🎨 - Combines multiple art styles with adjustable blend modes
- Prompt Enhancer 📝 - Adds detail, mood, composition, lighting, or color enhancements
- Negative Prompt Generator ⛔ - Creates matching negative prompts with adjustable strictness

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
