# UniGen 🚀  
**90% Faster, 100% Code-Free: MLLM-Driven Zero-Code 3D Game Development**

UniGen is the first end-to-end **multi-agent framework** for **automated Unity game creation**. From a **natural language description**, UniGen generates **runnable 3D games** without requiring a single line of manual code.  

Backed by **Multimodal Large Language Models (MLLMs)**, UniGen automates the entire pipeline:  
1. **Planning Agent** – interprets natural language into structured blueprints.  
2. **Generation Agent** – produces robust Unity C# scripts.  
3. **Automation Agent** – builds and configures Unity scenes.  
4. **Debugging Agent** – fixes issues interactively via conversational debugging.  

🎥 [Demo Video](https://youtube.com/[YourVideoLink])  
📄 [Paper](https://arxiv.org/abs/2509.26161v1)  

---

## ✨ Features

- **Zero-Code Development** – create Unity games with just natural language prompts.  
- **End-to-End Automation** – no manual engine configuration, component binding, or script integration.  
- **Multi-Agent Framework** – specialized agents for planning, code generation, scene assembly, and debugging.  
- **High Efficiency** – reduces development time by **91.4%** compared to manual workflows.  
- **High Functional Completeness** – achieves >89.5% correctness across diverse game prototypes.  
- **Unity Integration** – outputs a ready-to-run Unity project with Editor + Runtime scripts.  

---

## 📦 Installation

### Prerequisites
- Python **3.8+**  
- Unity **2021+** (tested with LTS versions)  
- An OpenAI / MLLM API key (e.g., GPT-4.1 or Gemini-2.5)  

---

## 🚀 Usage

1. **Describe your game idea** in plain English
2. **Run the pipeline**:```bash python blue_pipeline.py```
3. **UniGen** will:
a)Generate Unity C# scripts (PlayerController, UIManager, etc.).
b)Build a scene with configured objects and components.
c)Save all assets into UnityProject/Assets/.
d)Open the Unity project, press play, and your game is ready! 
4. open the Unity project, press play, and your game is ready! 🎮

---

## 📂 Project Structure
```bash
UniGen/
│── blue_pipeline.py         # Main automation pipeline
│── gpt_interface.py         # GPT/MLLM connector
│── requirements.txt
│── README.md
```

---

## 🧪 Benchmarks

UniGen was tested on three prototypes:

| Game Prototype             | Functional Completeness | Dev Time Reduction |
|-----------------------------|--------------------------|---------------------|
| Obstacle Run               | 100%                    | 91.4%               |
| Coin Collection            | 93.8%                   | 91.4%               |
| Haunted Jaunt (Unity demo) | 89.5%                   | 91.4%               |

- Average development reduced from **140 mins → <12 mins**.  
- Manual operations reduced from **75 → <5**.  

---

## 📊 Architecture

UniGen’s pipeline operates via four agents:

- **Planning Agent** → JSON blueprints of entities & logic.  
- **Generation Agent** → Unity-ready C# scripts.  
- **Automation Agent** → Scene construction via Unity Editor APIs.  
- **Debugging Agent** → Conversational, automated error correction.  

<p align="center">
  <img src="docs/unigen_architecture.png" width="500"/>
</p>

---

## ⚠️ Limitations

- Complex **NPC behavior trees** not yet fully automated.  
- **Multiplayer synchronization** requires future enhancements.  
- Currently optimized for **Unity**, but engine-agnostic by design.  

