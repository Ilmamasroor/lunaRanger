import React, { useState } from 'react';
import { playSound } from '../utils/soundFX';
import InteractiveControlsTutorialModal from '../components/InteractiveControlsTutorialModal';

// Enhanced Mission Guide: Clean kid-friendly cards + interactive cartoon controls tutorial
export default function MissionGuide({ onContinue, onBack }) {
  const [showControlsTutorial, setShowControlsTutorial] = useState(false);

  return (
    <>
      <section className="w-full max-w-3xl bg-slate-900/95 border-2 border-cyan-400/40 rounded-3xl p-6 md:p-8 backdrop-blur-xl shadow-2xl">
        
        {/* Header Bar */}
        <div className="flex items-center justify-between gap-3 mb-5 border-b border-cyan-500/20 pb-4">
          <div className="flex items-center gap-3.5">
            <span className="text-4xl" aria-hidden="true">📡</span>
            <div>
              <h2 className="font-scifi text-2xl md:text-3xl font-black text-amber-300">MISSION GUIDE</h2>
              <p className="text-xs text-cyan-200">Artemis Outpost Alpha • Lunar South Pole (Shackleton Crater)</p>
            </div>
          </div>
          <span className="bg-purple-900/60 border border-purple-400/50 text-purple-200 text-xs font-bold px-3 py-1.5 rounded-full uppercase tracking-wider">
            Mission Briefing
          </span>
        </div>

        {/* 3 Main Guidance Cards */}
        <div className="space-y-4 mb-8">
          
          {/* Card 1: Your crew */}
          <div className="bg-slate-800/80 border border-cyan-400/30 hover:border-cyan-400/60 transition p-4 md:p-5 rounded-2xl flex items-center gap-4 shadow-md">
            <div className="w-12 h-12 rounded-2xl bg-cyan-950/80 border border-cyan-400/40 flex items-center justify-center text-3xl shrink-0">
              👨‍🚀
            </div>
            <div>
              <h3 className="font-bold text-base text-cyan-300 font-scifi">Your Crew</h3>
              <p className="text-xs md:text-sm text-slate-200 mt-0.5">
                You are one of four astronauts stationed at Shackleton Base.
              </p>
            </div>
          </div>

          {/* Card 2: Your mission */}
          <div className="bg-slate-800/80 border border-cyan-400/30 hover:border-cyan-400/60 transition p-4 md:p-5 rounded-2xl flex items-center gap-4 shadow-md">
            <div className="w-12 h-12 rounded-2xl bg-cyan-950/80 border border-cyan-400/40 flex items-center justify-center text-3xl shrink-0">
              🪨
            </div>
            <div>
              <h3 className="font-bold text-base text-cyan-300 font-scifi">Your Mission</h3>
              <p className="text-xs md:text-sm text-slate-200 mt-0.5">
                Scrape the lunar surface, excavate rock samples, and keep your crew safe across the seven-day shift.
              </p>
            </div>
          </div>

          {/* Card 3: How to play - Interactive Watch Controls Button */}
          <div className="bg-slate-800/80 border-2 border-cyan-400/50 hover:border-cyan-400 transition p-4 md:p-5 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-lg group">
            
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-cyan-950/80 border border-cyan-400/50 flex items-center justify-center text-3xl shrink-0 group-hover:scale-105 transition">
                🎮
              </div>
              <div>
                <h3 className="font-bold text-base text-cyan-300 font-scifi">How To Play</h3>
                <p className="text-xs md:text-sm text-slate-200 mt-0.5">
                  Move with <strong>WASD / Arrow Keys</strong>, and press <strong>E</strong> or click to interact with station modules.
                </p>
              </div>
            </div>

            {/* The Dedicated Watch Controls Tutorial Button */}
            <button
              onClick={() => {
                playSound('power');
                setShowControlsTutorial(true);
              }}
              className="bouncy-btn bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black text-xs px-4 py-2.5 rounded-xl font-scifi flex items-center gap-2 cursor-pointer uppercase shadow-md shrink-0 self-end sm:self-center"
            >
              <span>▶</span>
              <span>Watch Controls</span>
            </button>

          </div>

        </div>

        {/* Footer Navigation */}
        <div className="flex justify-between items-center pt-2">
          <button
            onClick={() => {
              playSound('click');
              onBack();
            }}
            aria-label="Go back to Main Menu"
            className="bouncy-btn bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs md:text-sm font-bold px-6 py-3 rounded-xl border border-slate-600 flex items-center gap-2 cursor-pointer transition"
          >
            <span className="text-base font-black text-cyan-300">←</span>
            <span className="font-scifi tracking-wider">BACK</span>
          </button>

          <button
            onClick={() => {
              playSound('power');
              onContinue();
            }}
            className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-sm md:text-base px-8 py-3 rounded-2xl font-scifi uppercase cursor-pointer"
          >
            CONTINUE 🚀
          </button>
        </div>

      </section>

      {/* Animated Interactive Controls Simulator Modal */}
      <InteractiveControlsTutorialModal
        isOpen={showControlsTutorial}
        onClose={() => setShowControlsTutorial(false)}
      />
    </>
  );
}
