import React, { useEffect } from 'react';
import { MISSION_DAYS } from '../data/missionConfig';
import { playSound } from '../utils/soundFX';

// OPTION B: Full-Screen Cinematic Orbital Flight Path across the Lunar Horizon
export default function MissionMapScreen({ currentDayIndex, onSelectDay, onBackToHome }) {
  const activeDayIndex = Math.min(currentDayIndex, MISSION_DAYS.length - 1);
  const activeDay = MISSION_DAYS[activeDayIndex];

  // 7 3D Orbital Coordinates sweeping gracefully across the lunar curve (in percentages for full responsiveness)
  const waypoints = [[12, 72], [26, 52], [40, 64], [54, 38], [67, 55], [80, 32], [92, 48]]
    .map(([x, y], i) => ({ x, y, ...MISSION_DAYS[i], badge: MISSION_DAYS[i].knowledgeBubbles[0].title }));
  const trail = 'M 120 720 Q 200 400 260 520 T 400 640 T 540 380 T 670 550 T 800 320 T 920 480';

  // Active rocket coordinates
  const currentTarget = waypoints[activeDayIndex];

  useEffect(() => {
    playSound('power');
  }, [currentDayIndex]);

  return (
    <div className="fixed inset-0 top-[68px] bottom-[30px] z-10 w-full overflow-hidden flex flex-col justify-between select-none font-scifi">
      
      {/* ================= 1. DEEP SPACE COSMOS WITH NEBULA ================= */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_#1e1b4b_0%,_#090d16_50%,_#020408_100%)] pointer-events-none"></div>

      {/* Distant Colorful Nebula Glows */}
      <div className="absolute top-10 left-1/4 w-[500px] h-[350px] bg-cyan-600/10 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute top-1/3 right-1/4 w-[400px] h-[400px] bg-indigo-600/15 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 left-1/3 w-[600px] h-[300px] bg-amber-500/10 rounded-full blur-[130px] pointer-events-none"></div>

      {/* Earthrise: Earth glowing in deep space */}
      <div className="absolute top-6 left-8 flex items-center gap-3 z-10 bg-slate-950/60 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-cyan-400/30 shadow-[0_0_20px_rgba(34,211,238,0.2)]">
        <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-blue-700 via-sky-400 to-emerald-300 shadow-[0_0_15px_rgba(56,189,248,0.8)] relative overflow-hidden flex items-center justify-center">
          <div className="absolute w-3 h-2 bg-white/40 rounded-full top-1 left-1.5 blur-[0.5px]"></div>
          <div className="w-full h-full bg-blue-900/20 mix-blend-overlay"></div>
        </div>
        <div>
          <span className="font-scifi text-[10px] text-cyan-200 font-bold block uppercase tracking-wider">
            Earthrise Altitude
          </span>
          <span className="text-[9px] text-slate-400">Lunar Orbit • 110 km</span>
        </div>
      </div>

      {/* Trail Progress Pill in top right */}
      <div className="absolute top-6 right-8 z-10 flex items-center gap-2 bg-slate-950/80 backdrop-blur-md border border-cyan-400/40 px-4 py-2 rounded-full shadow-lg">
        <span className="text-sm">🏆</span>
        <span className="font-scifi text-xs font-black text-amber-300 tracking-wider">
          {currentDayIndex} / 7 DAYS COMPLETED
        </span>
      </div>

      {/* ================= 2. GIANT CURVED 3D LUNAR HORIZON AT BOTTOM ================= */}
      <div className="absolute -bottom-[32vw] left-[-15vw] right-[-15vw] h-[55vw] rounded-[100%] bg-gradient-to-t from-slate-950 via-slate-900 to-slate-800 border-t-2 border-cyan-300/40 shadow-[0_-20px_80px_rgba(56,189,248,0.25)] pointer-events-none overflow-hidden">
        {/* Lunar Regolith Crater Textures & Light Highlights */}
        <div className="absolute inset-0 opacity-25 bg-[radial-gradient(#94a3b8_1.5px,transparent_1.5px)] [background-size:28px_28px]"></div>
        <div className="absolute top-10 left-1/4 w-36 h-20 rounded-full bg-slate-950/50 border border-slate-700/60 blur-[1px]"></div>
        <div className="absolute top-16 right-1/3 w-52 h-28 rounded-full bg-slate-950/60 border border-slate-700/60 blur-[1px]"></div>
        <div className="absolute top-8 right-1/5 w-24 h-14 rounded-full bg-slate-950/40 border border-slate-700/50 blur-[1px]"></div>
        {/* Soft lunar surface rim light glow */}
        <div className="absolute top-0 inset-x-0 h-10 bg-gradient-to-b from-cyan-400/20 to-transparent"></div>
      </div>

      {/* ================= 3. FULL-SCREEN SVG COSMIC RIVER & WAYPOINTS ================= */}
      <div className="relative flex-1 w-full h-full z-20">
        <svg viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-hidden="true"
          className="w-full h-full absolute inset-0 pointer-events-none overflow-visible">
          <defs>
            {/* Iridescent glowing cosmic trail gradient */}
            <linearGradient id="orbitalPathGrad" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#06B6D4" stopOpacity="0.9" />
              <stop offset="35%" stopColor="#3B82F6" stopOpacity="0.8" />
              <stop offset="70%" stopColor="#8B5CF6" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#F59E0B" stopOpacity="1" />
            </linearGradient>

            <filter id="hyperGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Deep Ambient Shadow Guide Trail */}
          <path
            d={trail}
            fill="none"
            stroke="rgba(2, 6, 23, 0.95)"
            strokeWidth="24"
            strokeLinecap="round"
          />

          {/* Glowing Cosmic Energy Ribbon */}
          <path
            d={trail}
            fill="none"
            stroke="url(#orbitalPathGrad)"
            strokeWidth="5"
            strokeLinecap="round"
            filter="url(#hyperGlow)"
          />

          {/* Pulsing Starlight Energy Particles along path */}
          <path
            d={trail}
            fill="none"
            stroke="#FFFFFF"
            strokeWidth="3"
            strokeDasharray="8 24"
            strokeLinecap="round"
            className="animate-pulse"
          />
        </svg>

        {/* ================= 4. THE 7 FLOATING HOLOGRAPHIC WAYPOINT SPHERES ================= */}
        {waypoints.map((pt, i) => {
          const isCompleted = i < currentDayIndex;
          const isCurrent = i === currentDayIndex;
          const isLocked = i > currentDayIndex;

          return (
            <div
              key={pt.day}
              style={{ left: `${pt.x}%`, top: `${pt.y}%` }}
              className="absolute -translate-x-1/2 -translate-y-1/2 z-20 group"
            >
              {/* Sci-Fi Target Reticle Ping for Current Mission */}
              {isCurrent && (
                <div className="absolute -inset-5 rounded-full border-2 border-dashed border-amber-400 animate-spin opacity-80 pointer-events-none"></div>
              )}
              {isCurrent && (
                <div className="absolute -inset-3 rounded-full border border-cyan-400 animate-ping opacity-60 pointer-events-none"></div>
              )}

              {/* Holographic Sphere Button */}
              <button
                onClick={() => {
                  if (isCurrent) {
                    playSound('power');
                    onSelectDay(i);
                  }
                }}
                disabled={!isCurrent}
                className={`relative w-14 h-14 md:w-16 md:h-16 rounded-full flex flex-col items-center justify-center transition-all duration-300 transform cursor-pointer select-none ${
                  isCurrent
                    ? 'scale-125 bg-gradient-to-tr from-amber-600 via-yellow-400 to-amber-200 shadow-[0_0_35px_rgba(251,191,36,0.9)] border-2 border-white'
                    : isCompleted
                    ? 'bg-gradient-to-tr from-emerald-700 via-teal-400 to-cyan-300 shadow-[0_0_25px_rgba(16,185,129,0.7)] border-2 border-emerald-200 hover:scale-115'
                    : 'bg-slate-900/90 border border-slate-700 opacity-60 cursor-not-allowed'
                }`}
              >
                {/* Sphere 3D Curvature Highlight */}
                <div className="absolute top-1 left-2 w-5 h-2.5 bg-white/60 rounded-full blur-[0.5px] pointer-events-none"></div>

                {/* Sphere Icon */}
                <span className="text-xl md:text-2xl filter drop-shadow">
                  {isCompleted ? '✓' : isLocked ? '🔒' : pt.icon}
                </span>

                <span className={`font-scifi text-[9px] font-black ${isCurrent ? 'text-slate-950' : 'text-white'}`}>
                  D{pt.day}
                </span>
              </button>

              {/* Title Tag Below Sphere */}
              <div className="absolute top-full mt-2 left-1/2 -translate-x-1/2 whitespace-nowrap pointer-events-none">
                <span className={`px-2.5 py-0.5 rounded-full font-scifi text-[10px] font-black tracking-wider shadow-md ${
                  isCurrent
                    ? 'bg-amber-400 text-slate-950 shadow-[0_0_12px_rgba(251,191,36,0.7)]'
                    : isCompleted
                    ? 'bg-emerald-950/90 text-emerald-300 border border-emerald-500/50'
                    : 'bg-slate-950/80 text-slate-400'
                }`}>
                  {pt.title}
                </span>
              </div>
            </div>
          );
        })}

        {/* ================= 5. THE ACTIVE ROCKET FLYING OVER ACTIVE NODE ================= */}
        <div
          style={{
            left: `${currentTarget.x}%`,
            top: `${currentTarget.y}%`,
            transition: 'all 0.9s cubic-bezier(0.34, 1.56, 0.64, 1)'
          }}
          className="absolute -translate-x-1/2 -translate-y-[115%] pointer-events-none z-30"
        >
          <div className="floating flex flex-col items-center">
            {/* The Transparent Custom Rocket PNG */}
            <img
              src="/favicon.png"
              alt="Cadet Rocket"
              className="w-12 h-12 md:w-14 md:h-14 object-contain filter drop-shadow-[0_0_20px_rgba(56,189,248,1)]"
            />
            {/* Pulsing Active Beacon Tag */}
            <div className="mt-1 bg-cyan-400 text-slate-950 font-scifi font-black text-[9px] px-2.5 py-0.5 rounded-full shadow-lg border border-white animate-bounce">
              YOU ARE HERE 📍
            </div>
          </div>
        </div>
      </div>

      {/* ================= 6. BOTTOM MISSION CONTROL COMMAND HUD ================= */}
      <div className="relative z-30 px-6 py-2 flex flex-col sm:flex-row items-center justify-between gap-4 bg-slate-950/85 backdrop-blur-xl border-t border-cyan-400/30">
        
        {/* Left: Back to Home */}
        <button
          onClick={() => {
            playSound('click');
            onBackToHome();
          }}
          className="bouncy-btn bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-bold px-5 py-2.5 rounded-xl border border-slate-600 flex items-center gap-2 cursor-pointer transition shrink-0"
        >
          <span>←</span>
          <span className="font-scifi">MAIN MENU</span>
        </button>

        {/* Center: Mission Preview Details */}
        <div className="flex items-center gap-3 text-center sm:text-left">
          <div className="w-10 h-10 rounded-xl bg-cyan-950/80 border border-cyan-400/50 flex items-center justify-center text-2xl shadow-inner shrink-0">
            {activeDay.icon}
          </div>
          <div>
            <div className="flex items-center justify-center sm:justify-start gap-2">
              <span className="font-scifi text-xs md:text-sm font-black text-amber-300 uppercase">
                DAY {activeDay.day}: {activeDay.title}
              </span>
              <span className="text-[9px] bg-cyan-500/20 text-cyan-300 border border-cyan-400/40 px-2 py-0.2 rounded-full font-semibold">
                Next Objective
              </span>
            </div>
            <p className="text-[11px] text-slate-300 max-w-lg truncate">
              {activeDay.subtitle}
            </p>
          </div>
        </div>

        {/* Right: Enter Mission Action Button */}
        <button
          onClick={() => {
            playSound('power');
            onSelectDay(activeDayIndex);
          }}
          className="bouncy-btn bouncy-btn-amber bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs md:text-sm px-8 py-3 rounded-2xl font-scifi uppercase tracking-wider shadow-[0_0_20px_rgba(251,191,36,0.6)] cursor-pointer shrink-0"
        >
          ENTER DAY {activeDay.day} 🚀
        </button>
      </div>

    </div>
  );
}
