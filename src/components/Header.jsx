import React from 'react';
import { playSound } from '../utils/soundFX';

// Sleek sci-fi futuristic home dome/station vector icon
function ModernHomeIcon({ className = "w-4 h-4" }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      {/* Outer outpost roof / dome */}
      <path d="M3 10.5L12 3L21 10.5V20C21 20.5523 20.5523 21 20 21H4C3.44772 21 3 20.5523 3 20V10.5Z" />
      {/* Pressurized airlock doorway */}
      <path d="M9 21V12H15V21" />
      {/* Top telemetry beacon point */}
      <circle cx="12" cy="7" r="1" fill="currentColor" />
    </svg>
  );
}

export default function Header({ cadetName, avatar, onHomeClick }) {
  return (
    <header className="relative z-10 px-5 py-2.5 flex items-center justify-between bg-slate-900/80 backdrop-blur-md border-b border-cyan-400/20 shadow-[0_4px_20px_rgba(6,182,212,0.08)]">
      {/* Brand Logo - Enlarged more as requested */}
      <div className="flex items-center">
        <img
          src="/lunarangers-logo.png"
          alt="LunaRangers - Dare to Dream. Defy the Odds."
          className="h-14 md:h-16 lg:h-20 w-auto object-contain filter drop-shadow-[0_0_16px_rgba(56,189,248,0.7)] hover:scale-105 transition-transform duration-300 cursor-pointer"
          onClick={() => {
            playSound('click');
            onHomeClick();
          }}
        />
      </div>

      {/* Right Controls - Enlarged Cadet badge and sleek Home button */}
      <div className="flex items-center gap-3.5">
        <div className="bg-cyan-950/90 border border-cyan-400/50 text-cyan-300 px-4 py-2 rounded-full font-bold text-sm flex items-center gap-2 shadow-md">
          <span className="text-base">{avatar}</span>
          <span className="font-scifi tracking-wide">{cadetName}</span>
        </div>

        <button
          onClick={() => {
            playSound('click');
            onHomeClick();
          }}
          aria-label="Return to Launchpad Home"
          className="group flex items-center gap-2 bg-gradient-to-r from-slate-800 to-slate-900 hover:from-cyan-950 hover:to-slate-800 text-slate-200 hover:text-cyan-200 px-4 py-2 rounded-xl border border-cyan-500/40 hover:border-cyan-400 transition-all font-semibold text-xs md:text-sm shadow-md cursor-pointer transform hover:scale-105"
        >
          <ModernHomeIcon className="w-4 h-4 text-cyan-400 group-hover:scale-110 transition-transform" />
          <span className="font-scifi font-bold tracking-wider">HOME</span>
        </button>
      </div>
    </header>
  );
}
