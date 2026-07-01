# Classy Flappy Bird (Web Edition)

A fully playable, responsive browser-based arcade game built with a Python Flask backend and an HTML5 Canvas frontend, featuring custom background themes and dynamic difficulty scaling.

## 🚀 Live Demo / Play Now

Experience the game instantly in your web browser:
👉 **[Play the Live Demo on Replit](https://flappy-bird-game--dhruvpbuddy.replit.app)** 

---

## ⚡ Quick Start

Because this project is configured as a cloud web app, you don't need to install anything locally to check it out or test it.

1. Click the **Live Demo** link above to play the game immediately.
2. Control the bird by pressing the **SPACEBAR** to flap and jump, **P** to pause the action, or **R** to restart your run from the game-over screen.

---

## ✨ Features

* **Zero-Setup Web Play:** Converted dynamically from a local desktop script into a portable, modern web app playable directly inside any standard browser window.
* **On-Canvas Theme Selection:** Allows users to interactively choose a visual aesthetic (Sky Blue, Pink, Light Blue, Black, or Dark Blue) directly on the menu screen before starting.
* **3D Shadow & Highlight Layering:** Simulates a 3D depth-of-field effect using stacked vector circles, specialized drop-shadow offsets, light belly patches, and glossy eye reflections.
* **Arcade-Accurate Obstacles:** Includes classic green pipes generated with distinctive top rim caps, subtle edge shading, and multi-layered green tone variations.
* **Smart Pixel Scoring:** Points are assigned strictly using boundary calculations, updating only when the bird's horizontal asset layer safely exits past the trailing edge of a pipe.
* **Dynamic Acceleration Curve:** Automatically forces incoming obstacles to accelerate by 1.5 pixels per frame for every 3 points scored, keeping the difficulty scaling sharp.

---

## 🛠️ How to Run Locally

If you want to pull this web configuration out of Replit and run it locally on your computer, follow these configuration steps:

### Prerequisites
* **Python Version:** Python 3.10 or newer.
* **External Frameworks:** `Flask` (the Python web micro-framework).

### Installation & Execution
1. Clone the project and step into the local folder structure:
   ```bash
   git clone https://github.com/EinsteinTheEngineer/Flappy-Bird-Game.git
   cd Flappy-Bird-Game
---
---

## 🤖 AI Usage Declaration

AI was used in this project minimally to assist with development. Below are the specific details of its usage:

* **Tool Used:** Gemini
* **Purpose - Ideation:** Used to brainstorm structural concepts and visual design upgrades.
* **Purpose - Debugging & Learning:** Used for identifying runtime syntax bugs and expanding my program knowledge of graphical design (specifically exploring Tkinter and state-handling mechanics).
