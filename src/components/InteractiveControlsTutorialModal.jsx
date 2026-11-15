import React, { useState } from 'react';
import { playSound } from '../utils/soundFX';

// Interactive Animated Cartoon Walkthrough for Kids (Enlarged & Comfortable Layout)
export default function InteractiveControlsTutorialModal({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState('wasd'); // 'wasd', 'e_key', 'wires'
  const [pressedKey, setPressedKey] = useState(null);
  const [astronautPos, setAstronautPos] = useState({ x: 45, y: 55 });
  const [interacted, setInteracted] = useState(false);
  const [connectedWires, setConnectedWires] = useState([false, false]);

  const triggerKeyAction = (key) => {
    playSound('click');
    setPressedKey(key);

    if (key === 'W') setAstronautPos((prev) => ({ ...prev, y: Math.max(25, prev.y - 12) }));
    if (key === 'S') setAstronautPos((prev) => ({ ...prev, y: Math.min(75, prev.y + 12) }));
    if (key === 'A') setAstronautPos((prev) => ({ ...prev, x: Math.max(20, prev.x - 12) }));
    if (key === 'D') setAstronautPos((prev) => ({ ...prev, x: Math.min(75, prev.x + 12) }));
    if (key === 'E') {
      playSound('power');
      setInteracted(true);
      setTimeout(() => setInteracted(false), 2000);
    }

    setTimeout(() => setPressedKey(null), 300);
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-6 bg-slate-950/90 backdrop-blur-md animate-fadeIn"
    >
      {/* Broadened modal width (max-w-5xl) and comfortable height for widescreen */}
      <div className="relative w-full max-w-5xl bg-slate-900 border-2 border-cyan-400 rounded-3xl p-6 md:p-8 shadow-[0_0_60px_rgba(6,182,212,0.5)] flex flex-col gap-5 overflow-hidden">
        
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyan-500/30 pb-4">
          <div className="flex items-center gap-3.5">
            <span className="text-3xl md:text-4xl animate-bounce">🕹️</span>
            <div>
              <h3 className="font-scifi text-xl md:text-2xl font-black text-amber-300 uppercase tracking-wider">
                CADET TRAINING SIMULATOR • INTERACTIVE CONTROLS
              </h3>
              <p className="text-xs md:text-sm text-cyan-200">
                Click keys to watch your astronaut move and interact in real time!
              </p>
            </div>
          </div>

          <button
            onClick={() => {
              playSound('click');
              onClose();
            }}
            className="text-xs md:text-sm bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-4 py-2 rounded-xl border border-slate-600 font-bold cursor-pointer transition"
          >
            ✕ Close
          </button>
        </div>

        {/* Lesson Tabs */}
        <div className="flex flex-wrap gap-2.5">
          <button
            onClick={() => setActiveTab('wasd')}
            className={`px-5 py-2.5 rounded-xl font-scifi text-xs md:text-sm font-bold transition cursor-pointer ${
              activeTab === 'wasd'
                ? 'bg-cyan-400 text-slate-950 shadow-md'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            1. WASD (Walking)
          </button>

          <button
            onClick={() => setActiveTab('e_key')}
            className={`px-5 py-2.5 rounded-xl font-scifi text-xs md:text-sm font-bold transition cursor-pointer ${
              activeTab === 'e_key'
                ? 'bg-amber-400 text-slate-950 shadow-md'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            2. Press 'E' (Open Airlock / Collect)
          </button>

          <button
            onClick={() => setActiveTab('wires')}
            className={`px-5 py-2.5 rounded-xl font-scifi text-xs md:text-sm font-bold transition cursor-pointer ${
              activeTab === 'wires'
                ? 'bg-emerald-400 text-slate-950 shadow-md'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            3. Connect Wires (Restore Heat)
          </button>
        </div>

        {/* Enlarged Interactive Animated Stage (h-84 md:h-96) */}
        <div className="relative w-full h-80 md:h-96 bg-gradient-to-b from-slate-950 to-slate-900 border-2 border-cyan-500/40 rounded-2xl overflow-hidden p-5 shadow-inner flex flex-col justify-between">
          
          {/* Top Instruction Banner */}
          <div className="bg-slate-900/90 border border-cyan-400/40 px-4 py-2 rounded-xl self-start text-xs md:text-sm font-scifi text-cyan-300 z-10 flex items-center gap-2">
            <span>💡</span>
            <span>
              {activeTab === 'wasd' && "Press W, A, S, D below to steer the cadet across the lunar terrain!"}
              {activeTab === 'e_key' && "Approach an object and press [E] to open airlock door or pick up battery!"}
              {activeTab === 'wires' && "Click matching wire plugs to restore heater power before base freezes!"}
            </span>
          </div>

          {/* TAB 1 & 2 ANIMATION: Animated Lunar Terrain Stage */}
          {activeTab !== 'wires' ? (
            <div className="relative w-full h-full flex items-center justify-center">
              {/* Habitat Dome Silhouette */}
              <div className="absolute right-16 top-6 bg-slate-800 border-2 border-cyan-400/50 rounded-t-full w-48 h-32 flex flex-col items-center justify-center shadow-2xl">
                <span className="text-3xl">🏛️</span>
                <span className="text-[10px] font-scifi text-cyan-300 font-bold mt-1">HABITAT DOME</span>
                <div className="w-12 h-16 bg-amber-500/80 rounded-t-lg mt-1 border-2 border-white flex items-center justify-center text-xs font-black text-slate-950">
                  {interacted ? "OPEN!" : "AIRLOCK"}
                </div>
              </div>

              {/* Spare Battery Object */}
              <div className="absolute left-20 bottom-8 flex flex-col items-center">
                <div className="w-14 h-10 bg-amber-500 rounded-lg border-2 border-white flex items-center justify-center text-xs font-black text-slate-950 shadow-[0_0_20px_rgba(251,191,36,0.9)] animate-pulse">
                  BATTERY
                </div>
                <span className="text-[10px] text-amber-300 font-bold mt-1">Target Object</span>
              </div>

              {/* Animated Floating Astronaut Character */}
              <div
                style={{
                  left: `${astronautPos.x}%`,
                  top: `${astronautPos.y}%`,
                  transition: 'all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)'
                }}
                className="absolute -translate-x-1/2 -translate-y-1/2 z-20 flex flex-col items-center pointer-events-none"
              >
                <div className="w-14 h-14 rounded-full bg-cyan-500/30 border-2 border-cyan-400 flex items-center justify-center text-4xl shadow-[0_0_25px_rgba(34,211,238,0.9)]">
                  👨‍🚀
                </div>
                {pressedKey && (
                  <span className="bg-amber-400 text-slate-950 font-scifi font-black text-[10px] px-2.5 py-0.5 rounded-full mt-1.5 animate-bounce">
                    KEY [{pressedKey}] PRESSED!
                  </span>
                )}
                {interacted && (
                  <span className="bg-emerald-400 text-slate-950 font-scifi font-black text-xs px-3 py-1 rounded-full mt-1.5 animate-ping">
                    INTERACTION SUCCESSFUL! ✨
                  </span>
                )}
              </div>
            </div>
          ) : (
            /* TAB 3 ANIMATION: The Wire Connection Puzzle Simulator */
            <div className="relative w-full h-full flex flex-col items-center justify-center gap-5">
              <span className="text-base font-scifi font-bold text-amber-300">
                HEATER CIRCUIT RELAY PUZZLE (1 & 2 / DRAG)
              </span>

              <div className="flex gap-10 items-center">
                {/* Wire 1 */}
                <button
                  onClick={() => {
                    playSound('power');
                    setConnectedWires((prev) => [!prev[0], prev[1]]);
                  }}
                  className={`p-4 rounded-2xl border-2 flex items-center gap-3.5 transition cursor-pointer ${
                    connectedWires[0]
                      ? 'bg-emerald-950 border-emerald-400 text-emerald-300 shadow-[0_0_20px_rgba(52,211,153,0.6)]'
                      : 'bg-slate-800 border-amber-400 text-amber-200'
                  }`}
                >
                  <span className="text-3xl">🔌</span>
                  <div className="text-left">
                    <span className="text-sm font-bold block">Wire 1: Positive Lead</span>
                    <span className="text-xs">{connectedWires[0] ? "CONNECTED ✔" : "Click to Connect"}</span>
                  </div>
                </button>

                {/* Wire 2 */}
                <button
                  onClick={() => {
                    playSound('power');
                    setConnectedWires((prev) => [prev[0], !prev[1]]);
                  }}
                  className={`p-4 rounded-2xl border-2 flex items-center gap-3.5 transition cursor-pointer ${
                    connectedWires[1]
                      ? 'bg-emerald-950 border-emerald-400 text-emerald-300 shadow-[0_0_20px_rgba(52,211,153,0.6)]'
                      : 'bg-slate-800 border-cyan-400 text-cyan-200'
                  }`}
                >
                  <span className="text-3xl">⚡</span>
                  <div className="text-left">
                    <span className="text-sm font-bold block">Wire 2: Heater Relay</span>
                    <span className="text-xs">{connectedWires[1] ? "CONNECTED ✔" : "Click to Connect"}</span>
                  </div>
                </button>
              </div>

              {connectedWires[0] && connectedWires[1] && (
                <div className="bg-emerald-500 text-slate-950 font-scifi font-black text-xs md:text-sm px-5 py-2 rounded-full shadow-lg animate-bounce">
                  🔥 CIRCUIT COMPLETE! HEATER POWER RESTORED (+100%)
                </div>
              )}
            </div>
          )}

          {/* Bottom Interactive Keypad */}
          <div className="flex flex-wrap justify-between items-center z-10 pt-3 border-t border-slate-800 gap-3">
            {activeTab === 'wasd' && (
              <div className="flex items-center gap-2.5">
                <span className="text-xs md:text-sm text-slate-400 font-bold">Try keys:</span>
                <button onClick={() => triggerKeyAction('W')} className="bg-slate-800 hover:bg-cyan-500 hover:text-black font-scifi font-bold px-3.5 py-1.5 rounded-lg border border-cyan-400/50 text-xs md:text-sm cursor-pointer">W</button>
                <button onClick={() => triggerKeyAction('A')} className="bg-slate-800 hover:bg-cyan-500 hover:text-black font-scifi font-bold px-3.5 py-1.5 rounded-lg border border-cyan-400/50 text-xs md:text-sm cursor-pointer">A</button>
                <button onClick={() => triggerKeyAction('S')} className="bg-slate-800 hover:bg-cyan-500 hover:text-black font-scifi font-bold px-3.5 py-1.5 rounded-lg border border-cyan-400/50 text-xs md:text-sm cursor-pointer">S</button>
                <button onClick={() => triggerKeyAction('D')} className="bg-slate-800 hover:bg-cyan-500 hover:text-black font-scifi font-bold px-3.5 py-1.5 rounded-lg border border-cyan-400/50 text-xs md:text-sm cursor-pointer">D</button>
              </div>
            )}

            {activeTab === 'e_key' && (
              <div className="flex items-center gap-2.5">
                <span className="text-xs md:text-sm text-slate-400 font-bold">Try interaction:</span>
                <button onClick={() => triggerKeyAction('E')} className="bg-amber-400 hover:bg-amber-300 text-slate-950 font-scifi font-black px-5 py-2 rounded-xl text-xs md:text-sm cursor-pointer shadow">
                  Press [ E ] Action
                </button>
              </div>
            )}

            {activeTab === 'wires' && (
              <span className="text-xs md:text-sm text-cyan-300 font-bold">
                Press [1] or [2] on keyboard or click the buttons above!
              </span>
            )}

            <button
              onClick={() => {
                playSound('power');
                onClose();
              }}
              className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-xs md:text-sm px-6 py-2.5 rounded-xl font-scifi uppercase cursor-pointer"
            >
              I Understand! Start Mission 🚀
            </button>
          </div>

        </div>

      </div>
    </div>
  );
}
