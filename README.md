# 🚀 LunaRangers — Junior Astronaut Mission Trainer
> **NASA Space Apps Challenge 2026** • Team Neural Knights  
> A child-friendly, interactive lunar mission trainer designed for ages 7–12.

---

## 🌟 Architecture Overview

```text
NASA Open Data Release (Fatima) 
       ↓
Python Pipeline (Data Clean & Map)
       ↓
TypeScript Simulation Engine (Ilma)
       ↓
React Mission Control Frontend (Muneeba)  <─── window.LunaRangersBridge ───>  Unity WebGL 3D Game (Abhinav)
```

1. **React Frontend (This Repo)**:
   - Owns the single-page application flow, Main Menu, Mission Guide, Full-Screen Orbital Expedition Trail Map, Day Goal Knowledge Bubbles, and Mission Debrief.
   - Hosts the **Full-Screen 3D WebGL Unity Viewport** with zero visual clutter.
   - Overlays non-overlapping corner HUDs (**Top-Left Checklist**, **Top-Center Action Prompt**, **Top-Right Suit & Crew Telemetry**).
   - Includes a responsive **2D High-Performance Schematic Fallback** for lower-end Chromebooks & mobile devices.

2. **Unity WebGL Integration (For Abhinav)**:
   - Employs a bidirectional JavaScript event bridge (`window.LunaRangersBridge`) to update checklists, timers, prompts, and trigger level completion callbacks without page reload.

3. **TypeScript Engine Integration (For Ilma & Fatima)**:
   - All state models and mission configurations are centralized in [`src/data/missionConfig.js`](./src/data/missionConfig.js), fully typed and ready to receive TypeScript engine state inputs.

---

## 🛠️ Prerequisites

Ensure you have installed on your system:
- **Node.js** (v18.0.0 or higher recommended; verified with v24.16.0)
- **npm** (comes with Node.js)
- A modern web browser (Chrome, Edge, Firefox, or Safari) supporting WebGL2

---

## 🚀 Quick Start (Local Setup)

1. **Clone the Repository & Checkout Feature Branch**:
   ```bash
   git clone <repo-url>
   cd luna-rangers-frontend
   git checkout -b feature/frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Start the Development Server**:
   ```bash
   npm run dev
   ```
   Open your browser at the displayed local URL (typically **`http://localhost:5173`**).

4. **Production Build**:
   ```bash
   npm run build
   ```

---

## 🎮 Game Controls (Day 1)

| Input | Action |
| :--- | :--- |
| **W, A, S, D** / Arrows | Move Astronaut across the lunar surface |
| **E / Click** | Interact with Airlock door or pick up Battery |
| **1, 2 / Drag** | Wire Connection Puzzle (Connect Positive & Relay wires) |
| **ESC / R** | Close wire repair panel / Restart Day 1 |

---

## 🔌 Unity ↔ React Event Bridge API (`window.LunaRangersBridge`)

Unity scripts can invoke React state updates directly from WebGL via `Application.ExternalCall` or WebGL jslib:

```javascript
// Check off an objective in the React HUD:
window.LunaRangersBridge.updateChecklist('step1', true);

// Update Suit countdown timer:
window.LunaRangersBridge.setSuitTimer(8);

// Update suit oxygen percentage:
window.LunaRangersBridge.setSuitOxygen(95);

// Update central action prompt:
window.LunaRangersBridge.setPrompt("Connect the heater wires");

// Trigger Day Completion modal:
window.LunaRangersBridge.completeDay();
```
