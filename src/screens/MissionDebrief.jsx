import React from 'react';

// Matches Abhinav's Screen 6: Mission Complete debrief
export default function MissionDebrief({ onBackToMainMenu }) {
  return (
    <section className="w-full max-w-lg bg-slate-900/95 border-2 border-amber-400 rounded-3xl p-6 backdrop-blur-xl shadow-2xl text-center">
      <div className="text-6xl mb-2 animate-bounce">🏆</div>
      <h2 className="font-scifi text-2xl md:text-3xl font-black text-amber-300 uppercase tracking-wider mb-1">
        MISSION COMPLETE
      </h2>
      <p className="text-xs font-bold text-cyan-200 mb-5">
        You finished all 7 days.
      </p>

      {/* 3 Success Pillars */}
      <div className="grid grid-cols-3 gap-2.5 mb-5">
        <div className="bg-slate-950/80 border border-emerald-400/50 p-3 rounded-2xl">
          <span className="text-2xl">👨🚀</span>
          <h4 className="text-[11px] font-bold text-slate-200 mt-1">Crew safe</h4>
          <span className="text-emerald-400 font-bold text-sm block mt-0.5">✔</span>
        </div>

        <div className="bg-slate-950/80 border border-emerald-400/50 p-3 rounded-2xl">
          <span className="text-2xl">🪨</span>
          <h4 className="text-[11px] font-bold text-slate-200 mt-1">Samples returned</h4>
          <span className="text-emerald-400 font-bold text-sm block mt-0.5">✔</span>
        </div>

        <div className="bg-slate-950/80 border border-emerald-400/50 p-3 rounded-2xl">
          <span className="text-2xl">📅</span>
          <h4 className="text-[11px] font-bold text-slate-200 mt-1">7 days complete</h4>
          <span className="text-emerald-400 font-bold text-sm block mt-0.5">✔</span>
        </div>
      </div>

      {/* What You Learned Card */}
      <div className="bg-indigo-950/70 border border-indigo-400/50 p-3.5 rounded-2xl text-left mb-6">
        <div className="flex items-center gap-1.5 text-xs font-scifi font-bold text-amber-300 mb-1">
          <span>💡</span> <span>WHAT YOU LEARNED</span>
        </div>
        <p className="text-xs text-slate-200 leading-snug">
          Keep the crew safe, restore power, and collect samples when cleared.
        </p>
      </div>

      <button
        onClick={onBackToMainMenu}
        className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-sm px-8 py-3 rounded-2xl font-scifi uppercase cursor-pointer"
      >
        BACK TO MAIN MENU
      </button>
    </section>
  );
}
