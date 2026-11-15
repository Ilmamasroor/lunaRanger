import React, { useState } from 'react';
import { playSound } from '../utils/soundFX';

// Authentic circular bubble with iridescent shine, rise-up float motion, and bursting particle sound
export default function CircularBubble({ bubble, index, onSelectBubble }) {
  const [bursting, setBursting] = useState(false);

  // Snappy, energetic rise timing: bubbles appear immediately and stay bright
  const floatSpeeds = [5.5, 6.2, 5.8, 6.5, 6.0];
  const duration = floatSpeeds[index % floatSpeeds.length];
  // Immediate initial staggering so bubbles are visible right when screen loads
  const delay = (index * 0.7) % 3;

  const handlePop = () => {
    playSound('bubblePop');
    setBursting(true);
    setTimeout(() => {
      setBursting(false);
      onSelectBubble(bubble);
    }, 250);
  };

  return (
    <div
      style={{
        animationDuration: `${duration}s`,
        animationDelay: `-${delay}s`,
      }}
      className="rising-bubble inline-block relative cursor-pointer select-none"
    >
      <button
        onClick={handlePop}
        className={`bubble-sphere w-24 h-24 md:w-28 md:h-28 flex flex-col items-center justify-center p-2 relative transition-transform transform hover:scale-115 active:scale-95 group cursor-pointer ${
          bursting ? 'scale-130 opacity-30 animate-ping' : ''
        }`}
        title={`Tap to pop ${bubble.title}!`}
      >
        {/* Curvature Light Glint */}
        <div className="absolute top-2.5 left-4 w-7 h-3 bg-white/60 rounded-full blur-[0.6px] rotate-[-25deg] pointer-events-none"></div>
        <div className="absolute top-5 left-3 w-2 h-2 bg-white/40 rounded-full pointer-events-none"></div>

        {/* Bubble Content */}
        <span className="text-3xl md:text-4xl filter drop-shadow group-hover:scale-110 transition">
          {bubble.icon}
        </span>
        <span className="font-scifi text-[10px] md:text-[11px] font-black text-white group-hover:text-amber-300 tracking-tight leading-tight mt-1 text-center drop-shadow-md">
          {bubble.title}
        </span>
        <span className="text-[8px] bg-cyan-900/60 text-cyan-200 px-1.5 py-0.2 rounded-full font-bold border border-cyan-400/40 mt-0.5">
          {bubble.badge || 'Pop!'}
        </span>
      </button>
    </div>
  );
}
