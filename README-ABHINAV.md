# 🚀 Abhinav's Unity WebGL Build Instructions

Hey Abhinav! Your Unity source code has been integrated into the React frontend.
The bridge is **fully wired** to your `ResearchBridge.jslib` and `AirlockBridge.jslib`.

All you need to do is **export a WebGL build** and drop the files in the right place.

---

## Step 1 — Open Unity Project

Open the `unity/` folder from the repo root in Unity Hub.
Recommended: **Unity 6** (LTS) with the **WebGL Build Support** module installed.

---

## Step 2 — Set the WebGL Template

In Unity:
1. Go to **Edit → Project Settings → Player**
2. Under **WebGL** tab, find **Resolution and Presentation**
3. Set **WebGL Template** to **LunaRangers** (already in `Assets/WebGLTemplates/LunaRangers/`)

---

## Step 3 — Build for WebGL

1. **File → Build Settings**
2. Select **WebGL** as the platform (switch if needed)
3. Make sure the **DayOne scene** is in the build list
4. Click **Build** and choose an output folder (e.g. `D:\unity-webgl-build\`)

---

## Step 4 — Copy Build Files to React

After Unity finishes, copy **only the `Build/` subfolder** from your output into:

```
D:\NASA\luna-rangers-frontend\public\Build\
```

Then rename the files so they match exactly:

| Unity output filename | Rename to |
|----------------------|-----------|
| `*.loader.js` | `LunaRangers.loader.js` |
| `*.data` or `*.data.br` | `LunaRangers.data` |
| `*.framework.js` | `LunaRangers.framework.js` |
| `*.wasm` or `*.wasm.br` | `LunaRangers.wasm` |

> **Note:** If Unity exported compressed files (`.br` or `.gz`), you'll need to either:
> - Rebuild with **Compression Format: Disabled** in Player Settings → WebGL, OR
> - Configure the Vite dev server to serve them with correct Content-Encoding headers

---

## Step 5 — Test the Integration

```powershell
cd D:\NASA\luna-rangers-frontend
node "C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js" run dev
```

Open `http://localhost:5173`, start a mission — your Unity game should load inside the React HUD!

---

## How the Bridge Works (Already Wired!)

Your `.jslib` files dispatch CustomEvents. React listens to them automatically:

```js
// Your ResearchBridge.jslib (fires from Unity C#):
window.dispatchEvent(new CustomEvent("unity-research-state", {
  detail: {
    step: "Collect",        // "Exit" | "Collect" | "Return" | "Dock" | "Repair"
    feedback: "Bring the spare battery inside.",
    secondsLeft: 180.0,
    water: 100,
    health: 100,
    outside: false,
    finished: false,
    needsRetry: false,
    objectiveName: "Spare battery"
  }
}));

// Your AirlockBridge.jslib (fires from Unity C#):
window.dispatchEvent(new CustomEvent("unity-airlock", { detail: "open" }));
window.dispatchEvent(new CustomEvent("unity-airlock", { detail: "close" }));
```

React HUD responds to these automatically:
- ✅ Checklist items tick off based on `step`
- ✅ Suit timer appears / disappears based on `outside`
- ✅ Water & health bars update
- ✅ Action prompt updates from `feedback`
- ✅ Day Complete triggers when `finished: true`

---

## Testing Without a Build (Browser Console)

You can test the bridge right now in the browser console:

```js
// Simulate player picking up battery
window.dispatchEvent(new CustomEvent('unity-research-state', {
  detail: { step: 'Collect', feedback: 'Battery collected!', secondsLeft: 180, water: 95, health: 100, outside: false, finished: false, needsRetry: false }
}));

// Simulate going outside (triggers suit timer)
window.dispatchEvent(new CustomEvent('unity-airlock', { detail: 'open' }));

// Simulate day complete
window.dispatchEvent(new CustomEvent('unity-research-state', {
  detail: { step: 'Repair', feedback: 'Heater is on!', secondsLeft: 120, water: 90, health: 100, outside: false, finished: true, needsRetry: false }
}));
```
