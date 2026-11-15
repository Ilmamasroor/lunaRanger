import React, { useState } from 'react';
import { playSound } from '../utils/soundFX';

// Interactive floating, bursting knowledge bubble with sound & visual burst effect
export default function KnowledgeBubble({ bubble, delay = 0 }) {
  const [popped, setPopped] = useState(false);
  const [bursting, setBursting] = useState(false);

  const handlePop = () => {
    if (popped) return;
    playSound('bubblePop');
    setBursting(true);
    setTimeout(() => {
      setBursting(false);
      setPopped(true);
    }, 280);
  };

  const handleClose = (e) => {
    e.stopPropagation();
    playSound('click');
    setPopped(false);
  };

  return (
    <div className="relative flex justify-center">
      {!popped ? (
        <button
          onClick={handlePop}
          style={{ animationDelay: `${delay}s` }}
          className={`floating relative flex items-center justify-between gap-4 w-full bg-gradient-to-r from-cyan-950/90 via-slate-900/90 to-indigo-950/90 hover:from-cyan-900 hover:to-indigo-900 border-2 border-cyan-400/50 hover:border-amber-300 p-3.5 rounded-2xl shadow-[0_0_20px_rgba(34,211,238,0.25)] hover:shadow-[0_0_30px_rgba(251,191,36,0.4)] transition-all transform hover:scale-[1.02] cursor-pointer text-left group ${
            bursting ? 'scale-110 opacity-70 animate-ping' : ''
          }`}
        >
          {/* Shimmer / Bubble shine reflection */}
          <div className="absolute top-1 left-4 w-12 h-2 bg-white/20 rounded-full blur-[1px] pointer-events-none"></div>

          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-2xl bg-cyan-950/80 border border-cyan-400/60 flex items-center justify-center text-2xl shadow-inner group-hover:scale-110 transition">
              {bubble.icon}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-scifi font-bold text-sm text-cyan-200 group-hover:text-amber-300 transition">
                  {bubble.title}
                </span>
                <span className="text-[10px] bg-cyan-500/25 border border-cyan-400/40 text-cyan-300 px-2 py-0.5 rounded-full font-bold">
                  Tap to pop! 🫧
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">{bubble.shortDesc}</p>
            </div>
          </div>

          <span className="text-xl text-cyan-400 group-hover:translate-x-1 group-hover:text-amber-300 transition shrink-0 pr-2">
            ✨
          </span>
        </button>
      ) : (
        /* The Popped Knowledge Burst Card */
        <div className="w-full bg-gradient-to-r from-indigo-950/95 via-slate-900/95 to-cyan-950/95 border-2 border-amber-400 p-4 rounded-2xl shadow-[0_0_35px_rgba(251,191,36,0.35)] transition-all animate-fadeIn">
          <div className="flex items-center justify-between gap-2 mb-2">
            <div className="flex items-center gap-2.5">
              <span className="text-2xl animate-bounce">💡</span>
              <div>
                <span className="font-scifi font-black text-xs text-amber-300 uppercase tracking-wider block">
                  Knowledge Burst • {bubble.title}
                </span>
                <span className="text-[10px] text-cyan-300 font-semibold">NASA Mission Science</span>
              </div>
            </div>
            <button
              onClick={handleClose}
              className="text-xs text-slate-300 hover:text-white px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-600 cursor-pointer font-bold transition"
            >
              Back to Bubble 🫧
            </button>
          </div>
          <p className="text-xs md:text-sm text-slate-100 leading-relaxed bg-slate-950/60 p-3 rounded-xl border border-cyan-500/30">
            {bubble.fact}
          </p>
        </div>
      )}
    </div>
  );
}
