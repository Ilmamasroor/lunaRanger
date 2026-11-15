# 📋 Instructions for Teammates (Integration Guide)

This guide provides instructions for team members to integrate their deliverables with the React frontend.

---

## 🎮 For Abhinav (Unity WebGL Lead)

### 1. Where to Mount the Unity WebGL Canvas
In [`src/screens/Gameplay.jsx`](./src/screens/Gameplay.jsx), look for the container with `id="unity-container"`.
Simply replace the placeholder mockup with your Unity WebGL instantiation code:

```javascript
createUnityInstance(document.querySelector("#unity-canvas"), {
  dataUrl: "Build/LunaRangers.data",
  frameworkUrl: "Build/LunaRangers.framework.js",
  codeUrl: "Build/LunaRangers.wasm",
  streamingAssetsUrl: "StreamingAssets",
  companyName: "NeuralKnights",
  productName: "LunaRangers",
  productVersion: "1.0",
});
```

### 2. Communicating with the React HUD
React exposes `window.LunaRangersBridge` globally:
- **`updateChecklist(stepId: string, done: boolean)`**: Checks off items on the Top-Left overlay.
- **`setSuitTimer(seconds: number)`**: Updates the 10-second countdown on the Top-Right overlay.
- **`setSuitOxygen(percentage: number)`**: Updates telemetry live.
- **`setPrompt(text: string)`**: Changes the top-center action banner (e.g., *"E • Pick up battery"*).
- **`completeDay()`**: Transitions into the Day Complete celebration modal.

### 3. 2D Fallback
The `viewMode` toggle inside `Gameplay.jsx` is active. If WebGL2 crashes or drops below 25 FPS, toggle `viewMode = '2D'` to render the lightweight 2D schematic.

---

## ⚙️ For Ilma & Fatima (Data Pipeline & TypeScript Engine)

### 1. How Real NASA Data Feeds the Frontend
Fatima extracts NASA data (e.g. Shackleton crater temperature, radiation levels, ECLSS oxygen/water metrics) and processes it via Python. That output generates application parameters for the TypeScript simulation engine.

### 2. The Bridge to React
All daily mission rules, scientific numbers, knowledge bubbles, and learning takeaways live in [`src/data/missionConfig.js`](./src/data/missionConfig.js).
Whenever the TypeScript engine outputs updated mission parameters, you can:
1. Export the schema directly as JSON or TypeScript objects into `src/data/`.
2. The React HUD, Checklist, and Bubbles will immediately render the updated science without touching any UI component code!

---

## 💻 Running the Feature Branch

```bash
git checkout -b feature/frontend
npm install
npm run dev
```
