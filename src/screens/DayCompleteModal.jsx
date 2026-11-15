import React from 'react';
import { playSound } from '../utils/soundFX';

// Matches Abhinav's Screen 5: Day Complete modal transitioning to the Snake Trail Map
export default function DayCompleteModal({ dayData, onContinueToMap }) {
  return (
    <section className="w-full max-w-md bg-slate-900/95 border-2 border-amber-400 rounded-3xl p-6 backdrop-blur-xl shadow-2xl text-center">
      <div className="text-5xl mb-2 animate-bounce">🏆</div>
      <h2 className="font-scifi text-2xl font-black text-amber-300 uppercase tracking-wider mb-0.5">
        DAY {dayData.day} COMPLETE
      </h2>
      <p className="text-xs font-bold text-cyan-200 mb-5">
        {dayData.title}
      </p>

      <ul aria-label="Completed objectives" className="space-y-2 mb-5 text-left">
        {dayData.checklist.map(step => (
          <li key={step} className="bg-slate-800/80 border border-emerald-400/40 p-2.5 rounded-xl flex items-center gap-2.5">
            <span aria-hidden="true" className="text-emerald-400 text-sm">✔</span>
            <span className="text-xs font-bold text-slate-100">{step}</span>
          </li>
        ))}
      </ul>

      {/* What You Learned Card */}
      <div className="bg-indigo-950/70 border border-indigo-400/50 p-3.5 rounded-2xl text-left mb-6">
        <div className="flex items-center gap-1.5 text-xs font-scifi font-bold text-amber-300 mb-1">
          <span>💡</span> <span>WHAT YOU LEARNED</span>
        </div>
        <p className="text-xs text-slate-200 leading-snug">
          {dayData.learningTakeaway}
        </p>
      </div>

      <button
        onClick={() => {
          playSound('power');
          onContinueToMap();
        }}
        className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-sm px-8 py-3 rounded-2xl font-scifi uppercase cursor-pointer"
      >
        CONTINUE TO TRAIL MAP 🗺️
      </button>
    </section>
  );
}
