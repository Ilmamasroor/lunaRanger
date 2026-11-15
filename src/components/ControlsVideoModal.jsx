import React, { useState } from 'react';
import { playSound } from '../utils/soundFX';

export default function ControlsVideoModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="controlsModalTitle"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fadeIn"
    >
      <div className="relative w-full max-w-3xl bg-slate-900 border-2 border-cyan-400/80 rounded-3xl p-5 md:p-6 shadow-[0_0_50px_rgba(6,182,212,0.4)] flex flex-col gap-4 overflow-hidden">
        
        {/* Modal Top Header */}
        <div className="flex items-center justify-between border-b border-cyan-500/20 pb-3">
          <div className="flex items-center gap-2.5">
            <span className="text-2xl animate-bounce">🎮</span>
            <div>
              <h3 id="controlsModalTitle" className="font-scifi text-lg md:text-xl font-black text-amber-300 uppercase tracking-wider">
                HOW TO PLAY • DAY 1 CONTROLS
              </h3>
              <p className="text-xs text-cyan-200">
                Unity Engine Gameplay Preview • Artemis Outpost Alpha
              </p>
            </div>
          </div>

          <button
            onClick={() => {
              playSound('click');
              onClose();
            }}
            aria-label="Close controls modal"
            className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-3 py-1.5 rounded-xl border border-slate-600 font-bold cursor-pointer transition"
          >
            ✕ Close
          </button>
        </div>

        {/* Video Player Display Container */}
        <div className="relative w-full aspect-video bg-black rounded-2xl overflow-hidden border border-cyan-500/40 shadow-inner flex items-center justify-center">
          <video
            src="/day1-controls-demo.mp4"
            controls
            autoPlay
            loop
            muted
            playsInline
            className="w-full h-full object-contain"
          >
            Your browser does not support the video tag.
          </video>
        </div>

        {/* Actionable Keybindings Breakdown Cards (Exact specifications from Abhinav) */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-center text-xs">
          
          <div className="bg-slate-950/80 border border-cyan-400/40 p-2.5 rounded-xl">
            <span className="font-scifi text-amber-300 font-bold block text-sm">W A S D</span>
            <span className="text-[10px] text-slate-300">Move Astronaut / Rover</span>
          </div>

          <div className="bg-slate-950/80 border border-emerald-400/40 p-2.5 rounded-xl">
            <span className="font-scifi text-emerald-300 font-bold block text-sm">E / CLICK</span>
            <span className="text-[10px] text-slate-300">Interact with objects</span>
          </div>

          <div className="bg-slate-950/80 border border-amber-400/40 p-2.5 rounded-xl">
            <span className="font-scifi text-amber-300 font-bold block text-sm">1 , 2 / DRAG</span>
            <span className="text-[10px] text-slate-300">Heater wire connections</span>
          </div>

          <div className="bg-slate-950/80 border border-rose-400/40 p-2.5 rounded-xl">
            <span className="font-scifi text-rose-300 font-bold block text-sm">ESC / R</span>
            <span className="text-[10px] text-slate-300">Close Panel / Restart</span>
          </div>

        </div>

        {/* Bottom Acknowledgment Button */}
        <div className="flex justify-end pt-1">
          <button
            onClick={() => {
              playSound('power');
              onClose();
            }}
            className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-xs md:text-sm px-6 py-2.5 rounded-xl font-scifi uppercase cursor-pointer"
          >
            READY TO PLAY 🚀
          </button>
        </div>

      </div>
    </div>
  );
}
