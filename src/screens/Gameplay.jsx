import React, { useState, useEffect, useRef } from 'react';
import { playSound } from '../utils/soundFX';

// Step name from Abhinav's DayOneSimulation → checklist index to mark done (Day 1)
const STEP_TO_DONE_UP_TO = { Collect: 0, Return: 1, Dock: 2, Repair: 3 };

// Matches User Request: Full-Screen Unity Viewport with zero clutter,
// and translucent HUD overlay positioned unobtrusively in the corners (never overlapping game elements)
export default function Gameplay({ dayData, onCompleteDay }) {
  const [viewMode, setViewMode] = useState('3D'); // '3D' WebGL or '2D' Fallback
  const [checklist, setChecklist] = useState(dayData.checklist);
  const [suitTimer, setSuitTimer] = useState(null);   // null = not outside / timer inactive
  const [waterReserve, setWaterReserve] = useState(100);
  const [cadetHealth, setCadetHealth] = useState(100);
  const [currentPrompt, setCurrentPrompt] = useState("E \u2022 Open the airlock");
  const [unityLoaded, setUnityLoaded] = useState(false);
  const unityInstanceRef = useRef(null);

  // ─── Abhinav's Unity CustomEvent Bridge ───────────────────────────────────
  // ResearchBridge.jslib fires: new CustomEvent("unity-research-state", { detail: { step, feedback, secondsLeft, water, health, outside, finished, needsRetry, objectiveName } })
  // AirlockBridge.jslib fires:  new CustomEvent("unity-airlock", { detail: "open" | "close" })
  useEffect(() => {
    const handleResearchState = (e) => {
      const d = e.detail;
      if (!d) return;

      // Suit timer — only show when cadet is outside the habitat
      if (typeof d.secondsLeft === 'number') {
        setSuitTimer(d.outside ? Math.round(d.secondsLeft) : null);
      }
      if (typeof d.water === 'number') setWaterReserve(d.water);
      if (typeof d.health === 'number') setCadetHealth(d.health);
      if (typeof d.feedback === 'string' && d.feedback) setCurrentPrompt(d.feedback);

      // Map Unity step name → checklist items done (Day 1 logic)
      if (typeof d.step === 'string' && dayData.day === 1) {
        const doneUpTo = STEP_TO_DONE_UP_TO[d.step] ?? -1;
        setChecklist((prev) =>
          prev.map((item, idx) => ({ ...item, done: idx <= doneUpTo }))
        );
      }

      // Day / mission complete
      if (d.finished) {
        playSound('power');
        setCurrentPrompt('Mission complete! Outstanding work, Cadet! \uD83D\uDE80');
        setTimeout(() => onCompleteDay(), 1400);
      }

      if (d.needsRetry) {
        setCurrentPrompt('Training paused — press R to restart.');
      }
    };

    const handleAirlock = (e) => {
      const type = e.detail;
      if (type === 'open') {
        setCurrentPrompt('You are outside \u2014 suit timer active! Find the battery. \uD83D\uDD0B');
      } else if (type === 'close') {
        setCurrentPrompt('Back inside the habitat. Good job, Cadet!');
        setSuitTimer(null);
      }
    };

    window.addEventListener('unity-research-state', handleResearchState);
    window.addEventListener('unity-airlock', handleAirlock);

    return () => {
      window.removeEventListener('unity-research-state', handleResearchState);
      window.removeEventListener('unity-airlock', handleAirlock);
    };
  }, [dayData.day, onCompleteDay]);

  // ─── Unity WebGL Loader (injected dynamically — silent if Build/ absent) ───
  // When Abhinav drops his compiled Build/ folder into public/, this auto-activates.
  useEffect(() => {
    if (viewMode !== '3D') return;

    const BUILD_PATH = '/Build/';
    const LOADER = BUILD_PATH + 'LunaRangers.loader.js';

    // Probe for loader without crashing the page if Build/ doesn't exist yet
    fetch(LOADER, { method: 'HEAD' })
      .then((res) => {
        if (!res.ok) return; // Build/ not present — stay on 2D mockup silently

        // Inject loader script once only
        if (document.querySelector(`script[src="${LOADER}"]`)) {
          mountUnity(BUILD_PATH);
          return;
        }
        const script = document.createElement('script');
        script.src = LOADER;
        script.onload = () => mountUnity(BUILD_PATH);
        script.onerror = () => console.warn('[LunaRangers] Unity loader failed.');
        document.body.appendChild(script);
      })
      .catch(() => {}); // Build/ missing — silent fallback, no errors

    function mountUnity(buildPath) {
      const canvas = document.querySelector('#unity-canvas');
      if (!canvas || unityInstanceRef.current) return;

      /* global createUnityInstance */
      createUnityInstance(canvas, {
        dataUrl: buildPath + 'LunaRangers.data',
        frameworkUrl: buildPath + 'LunaRangers.framework.js',
        codeUrl: buildPath + 'LunaRangers.wasm',
        streamingAssetsUrl: 'StreamingAssets',
        companyName: 'Neural Knights',
        productName: 'LunaRangers',
        devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
      })
        .then((instance) => {
          unityInstanceRef.current = instance;
          setUnityLoaded(true);
        })
        .catch((err) => console.error('[LunaRangers] Unity failed:', err));
    }

    return () => {
      // Gracefully quit Unity instance on React unmount
      if (unityInstanceRef.current) {
        unityInstanceRef.current.Quit?.().catch(() => {});
        unityInstanceRef.current = null;
      }
    };
  }, [viewMode]);

  // ─── 2D Demo simulator: clicking checklist items advances manually when no Unity ───
  const handleChecklistClick = (index) => {
    if (unityLoaded) return; // let Unity drive when loaded
    playSound('click');
    const updated = [...checklist];
    updated[index].done = !updated[index].done;
    setChecklist(updated);

    if (index === 0 && updated[0].done) {
      setCurrentPrompt("Collect the spare battery");
    } else if (index === 1 && updated[1].done) {
      setCurrentPrompt("Return to the orange airlock");
    } else if (index === 2 && updated[2].done) {
      setCurrentPrompt("Plug in the battery & connect wires");
    }

    if (updated.every((item) => item.done)) {
      playSound('power');
      setCurrentPrompt("Heat Restored! Mission Accomplished.");
      setTimeout(() => {
        onCompleteDay();
      }, 1200);
    }
  };

  return (
    <div className="fixed inset-0 top-[68px] bottom-[30px] z-10 w-full overflow-hidden flex flex-col justify-between select-none bg-slate-950">

      {/* ================= 1. THE FULL-SCREEN 3D WEBGL UNITY VIEWPORT (OR 2D FALLBACK) ================= */}
      <div className="relative w-full h-full flex items-center justify-center overflow-hidden bg-gradient-to-b from-slate-950 via-[#121624] to-[#0a0d14]">

        {viewMode === '3D' ? (
          /* Unity WebGL Canvas Container — canvas is always present; Unity mounts onto it when Build/ exists */
          <div id="unity-container" className="relative w-full h-full flex items-center justify-center">

            {/* Unity renders onto this canvas when the WebGL build is present */}
            <canvas
              id="unity-canvas"
              className={`block w-full h-full ${unityLoaded ? 'opacity-100' : 'opacity-0 pointer-events-none absolute'}`}
              tabIndex={0}
              width="1280"
              height="720"
              aria-label="LunaRangers lunar outpost game"
            />

            {/* 2D Mockup — shown while Unity Build/ is absent */}
            {!unityLoaded && (
              <div className="relative w-full max-w-5xl h-full flex items-center justify-center">

                {/* Isometric Hab Modules & Solar Panels Visual */}
                <div className="relative flex items-center scale-90 md:scale-105">

                  {/* Hab Dome Cylinders */}
                  <div className="relative flex items-center">
                    <div className="w-56 h-36 rounded-full bg-gradient-to-b from-slate-200 via-slate-300 to-slate-400 border-4 border-slate-500 shadow-2xl flex items-center justify-center relative">
                      <div className="w-16 h-8 bg-slate-800 rounded-md border-2 border-cyan-400/80"></div>
                    </div>

                    {/* Tube link */}
                    <div className="w-16 h-16 bg-slate-400 border-y-4 border-slate-600"></div>

                    {/* Second Module with Orange Airlock */}
                    <div className="w-64 h-40 rounded-full bg-gradient-to-b from-slate-200 via-slate-300 to-slate-400 border-4 border-slate-500 shadow-2xl flex items-center justify-center relative">
                      {/* Orange Airlock Doorway */}
                      <div className="absolute left-6 bottom-4 w-16 h-24 bg-amber-500 rounded-t-lg border-2 border-white flex flex-col items-center justify-center shadow-lg">
                        <span className="text-[9px] font-black font-scifi text-slate-950">AIRLOCK</span>
                        <div className="w-3 h-3 rounded-full bg-cyan-300 mt-2 animate-pulse"></div>
                      </div>
                    </div>
                  </div>

                  {/* Solar Panel Array */}
                  <div className="absolute -bottom-10 right-10 w-48 h-28 bg-gradient-to-tr from-blue-950 via-blue-800 to-cyan-700 border-4 border-slate-300 rounded-lg shadow-2xl transform rotate-[-12deg] skew-x-6 flex items-center justify-center">
                    <div className="w-full h-full grid grid-cols-4 grid-rows-3 gap-1 p-1">
                      {Array.from({ length: 12 }).map((_, i) => (
                        <div key={i} className="border border-cyan-300/40 bg-blue-600/30"></div>
                      ))}
                    </div>
                  </div>

                  {/* Spare Battery Box */}
                  <button
                    onClick={() => handleChecklistClick(1)}
                    className="absolute -bottom-8 left-20 bg-amber-500 border-2 border-white rounded px-3 py-1 font-scifi font-black text-xs text-slate-950 shadow-[0_0_20px_rgba(251,191,36,0.9)] animate-bounce cursor-pointer"
                  >
                    🔋 BATTERY
                  </button>

                  {/* Astronaut Cadet */}
                  <div className="absolute bottom-2 left-44 floating flex flex-col items-center">
                    <div className="w-14 h-14 rounded-full bg-white border-2 border-slate-300 flex items-center justify-center text-4xl shadow-2xl">
                      👨‍🚀
                    </div>
                  </div>

                  {/* "Waiting for Unity" badge */}
                  <div className="absolute top-4 inset-x-0 flex justify-center pointer-events-none">
                    <div className="bg-slate-900/90 border border-amber-400/60 px-4 py-1.5 rounded-xl text-amber-300 font-scifi text-[11px] font-bold">
                      ⚡ Unity WebGL loading… (Build/ not yet detected)
                    </div>
                  </div>
                </div>
              </div>
            )}

          </div>
        ) : (
          /* ================= 2D RESPONSIVE FALLBACK MODE ================= */
          <div className="w-full max-w-2xl bg-slate-900 border-2 border-cyan-400/50 rounded-3xl p-6 text-center">
            <span className="font-scifi text-emerald-400 text-sm font-bold block mb-2">
              📐 2D HIGH-PERFORMANCE SCHEMATIC ACTIVE
            </span>
            <p className="text-xs text-slate-300 mb-4">
              Running in lightweight 2D fallback mode (Safe for low-spec Chromebooks and mobile browsers).
            </p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-2xl border border-cyan-500/40">
                <span className="text-3xl">🏛️</span>
                <span className="font-scifi text-xs font-bold text-cyan-200 block mt-2">Living Dome Alpha</span>
                <span className="text-[10px] text-emerald-300">Pressure: 101.3 kPa</span>
              </div>
              <div className="bg-slate-950 p-4 rounded-2xl border border-amber-500/40">
                <span className="text-3xl">⚡</span>
                <span className="font-scifi text-xs font-bold text-amber-200 block mt-2">Heater Relays</span>
                <span className="text-[10px] text-amber-300">Battery: 35%</span>
              </div>
            </div>
          </div>
        )}

        {/* ================= 2. UNOBTRUSIVE HUD OVERLAYS ================= */}

        {/* TOP-LEFT HUD: Objective & Checklist Overlay */}
        <div className="absolute top-4 left-5 z-20 bg-slate-950/85 backdrop-blur-md border border-cyan-400/50 rounded-2xl p-4 shadow-2xl max-w-xs pointer-events-auto">
          <div className="font-scifi text-[10px] text-cyan-300 font-bold tracking-wider uppercase mb-0.5">
            DAY {dayData.day} // {dayData.title}
          </div>
          <div className="font-scifi text-sm font-black text-amber-300 uppercase mb-2">
            Checklist
          </div>

          <div className="space-y-1.5 text-xs">
            {checklist.map((item, idx) => (
              <div
                key={item.id}
                onClick={() => handleChecklistClick(idx)}
                className="flex items-center gap-2 cursor-pointer hover:bg-slate-900/60 p-1 rounded-lg transition"
              >
                <span className={item.done ? "text-emerald-400 font-bold" : "text-slate-500 font-mono"}>
                  {item.done ? "[x]" : ">"}
                </span>
                <span className={`font-sans ${
                  item.done
                    ? "text-emerald-300 line-through opacity-70"
                    : item.active
                    ? "text-amber-300 font-bold"
                    : "text-slate-200"
                }`}>
                  {item.label}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* TOP-CENTER HUD: Active Action Prompt */}
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
          <div className="bg-slate-950/90 border-2 border-cyan-400/80 px-6 py-2 rounded-2xl shadow-[0_0_25px_rgba(6,182,212,0.4)] backdrop-blur-md flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
            <span className="font-scifi font-black text-sm md:text-base text-cyan-200 tracking-wider">
              {currentPrompt}
            </span>
          </div>
        </div>

        {/* TOP-RIGHT HUD: Suit & Crew Telemetry */}
        <div className="absolute top-4 right-5 z-20 bg-slate-950/85 backdrop-blur-md border border-cyan-400/50 rounded-2xl p-4 shadow-2xl w-56 pointer-events-auto">
          <div className="font-scifi text-[11px] font-black text-cyan-300 tracking-wider uppercase mb-2 border-b border-slate-800 pb-1 flex justify-between items-center">
            <span>SUIT &amp; CREW</span>
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          </div>

          <div className="space-y-1 text-xs font-mono text-slate-300 mb-3">
            <div className="flex justify-between">
              <span>Water reserve:</span>
              <span className="text-blue-300 font-bold">{waterReserve}%</span>
            </div>
            <div className="flex justify-between">
              <span>Cadet health:</span>
              <span className={`font-bold ${cadetHealth > 60 ? 'text-emerald-400' : cadetHealth > 30 ? 'text-amber-400' : 'text-red-400'}`}>
                {cadetHealth}%
              </span>
            </div>
          </div>

          {/* Golden Suit Timer — only shown when cadet is outside the habitat */}
          {suitTimer !== null && (
            <div className={`border rounded-xl px-3 py-1.5 flex items-center justify-between shadow ${
              suitTimer > 10 ? 'bg-amber-950/80 border-amber-400/60' : 'bg-red-950/90 border-red-400/80 animate-pulse'
            }`}>
              <span className={`font-scifi font-black text-xs ${suitTimer > 10 ? 'text-amber-300' : 'text-red-300'}`}>SUIT TIMER</span>
              <span className={`font-scifi font-black text-sm ${suitTimer > 10 ? 'text-amber-300' : 'text-red-300'}`}>
                {suitTimer < 10 ? `0${suitTimer}s` : `${suitTimer}s`}
              </span>
            </div>
          )}
        </div>

        {/* BOTTOM CONTROLS & VIEW SWITCHER BAR */}
        <div className="absolute bottom-3 inset-x-6 z-20 flex justify-between items-center text-xs pointer-events-auto">

          {/* Key Hint Bar */}
          <div className="bg-slate-950/80 border border-slate-800 px-4 py-1.5 rounded-xl text-slate-400 font-mono text-[11px] hidden sm:flex items-center gap-4">
            <span><strong className="text-white">WASD</strong> Move</span>
            <span><strong className="text-white">E</strong> Interact</span>
            <span><strong className="text-white">1, 2</strong> Connect Wires</span>
            <span><strong className="text-white">R</strong> Restart</span>
          </div>

          {/* View Switcher + Complete Level */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                playSound('click');
                setViewMode(viewMode === '3D' ? '2D' : '3D');
              }}
              className="bg-slate-900/90 hover:bg-slate-800 border border-cyan-400/40 text-cyan-300 px-3 py-1.5 rounded-xl font-scifi text-[10px] font-bold cursor-pointer transition shadow"
            >
              {viewMode === '3D' ? '🖥️ View: 3D WebGL (Switch 2D)' : '📐 View: 2D Schematic (Switch 3D)'}
            </button>
            <button
              onClick={() => {
                playSound('power');
                onCompleteDay();
              }}
              className="bouncy-btn bouncy-btn-green bg-emerald-400 text-slate-950 font-black text-xs px-4 py-1.5 rounded-xl font-scifi uppercase cursor-pointer"
            >
              Complete Level ✔
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}
