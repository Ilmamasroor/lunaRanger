import React, { useState } from 'react';
import CircularBubble from '../components/CircularBubble';
import { playSound } from '../utils/soundFX';
import pipeline from '../data/pipeline-snapshot.json';

// Custom Sci-Fi Vector Badges for Lightning & Battery
function PowerRelayBadge() {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-950/80 border border-amber-400/50 shadow-[0_0_15px_rgba(251,191,36,0.3)] mb-2">
      {/* High-tech Lightning Bolt SVG */}
      <svg className="w-4 h-4 text-amber-400 drop-shadow-[0_0_6px_rgba(251,191,36,0.8)]" viewBox="0 0 24 24" fill="currentColor">
        <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" />
      </svg>
      {/* High-tech Battery Cell SVG */}
      <svg className="w-5 h-5 text-emerald-400 drop-shadow-[0_0_6px_rgba(52,211,153,0.8)]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="2" y="6" width="17" height="12" rx="2" fill="rgba(16,185,129,0.2)" stroke="#34D399" />
        <path d="M21 10V14" stroke="#34D399" strokeLinecap="round" />
        <rect x="5" y="9" width="7" height="6" rx="1" fill="#34D399" />
      </svg>
      <span className="font-scifi text-[10px] font-bold text-amber-300 uppercase tracking-widest">
        CRITICAL POWER RELAY
      </span>
    </div>
  );
}

export default function DayGoalModal({ dayData, onStartDay, onBack }) {
  const [activeBurst, setActiveBurst] = useState(null);

  return (
    <section className="w-full max-w-4xl bg-slate-900/95 border-2 border-cyan-400/60 rounded-3xl p-6 md:p-8 backdrop-blur-xl shadow-2xl text-center relative overflow-hidden">
      
      {/* Top Realistic Sci-Fi Power Badge */}
      {dayData.day === 1 && <div className="flex justify-center"><PowerRelayBadge /></div>}

      <h2 className="font-scifi text-2xl md:text-3xl font-black text-cyan-300 uppercase tracking-wider mb-0.5 drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]">
        DAY {dayData.day} OF 7
      </h2>
      <h3 className="font-scifi text-xl font-black text-amber-300 mb-1">
        {dayData.title}
      </h3>
      <p className="text-xs md:text-sm text-slate-200 mb-4 max-w-xl mx-auto leading-relaxed">
        {dayData.subtitle}
      </p>
      {dayData.day === 5 && (
        <aside className="mb-4 rounded-xl border border-cyan-800 bg-slate-950 p-3 text-left text-sm text-slate-200">
          <p><a className="text-cyan-300 underline" href="https://ccmc.gsfc.nasa.gov/tools/DONKI/" target="_blank" rel="noreferrer">NASA DONKI</a> archived event · {pipeline.donki.provenance.activity_id} ({pipeline.donki.noaa_scale}). Mission Control replays this alert and blocks spacewalks until the next training day.</p>
          <p className="mt-2"><a className="text-cyan-300 underline" href={pipeline.radlab.iss.source} target="_blank" rel="noreferrer">NASA RadLab</a> · ISS {pipeline.radlab.iss.instrument} recorded {pipeline.radlab.iss.absorbedDoseRate.toFixed(2)} μGy/hour on {pipeline.radlab.iss.timestamp.slice(0, 10)}. The team’s pipeline also references the <a className="text-cyan-300 underline" href={pipeline.radlab.reference} target="_blank" rel="noreferrer">Chang’e-4 lunar measurement</a> of {pipeline.radlab.absorbedDoseRate} ± {pipeline.radlab.uncertainty} μGy/hour in silicon. These readings describe detector exposure in two different places.</p>
        </aside>
      )}
      {dayData.day === 7 && (
        <aside className="mb-4 rounded-xl border border-cyan-800 bg-slate-950 p-3 text-left text-sm text-slate-200">
          <p><a className="text-cyan-300 underline" href="https://osdr.nasa.gov/bio/repo/data/studies/OSD-269" target="_blank" rel="noreferrer">NASA OSDR {pipeline.osdr.studyId}</a> · This ISS study compared space-grown lettuce with lettuce grown on Earth. Fresh crops can supplement packaged food on longer missions.</p>
        </aside>
      )}

      {/* Broad Lunar Bubble Chamber Container */}
      <div className="relative w-full h-72 md:h-80 bg-gradient-to-b from-indigo-950/80 via-slate-950/95 to-slate-900/90 border-2 border-cyan-500/40 rounded-2xl p-4 overflow-hidden shadow-inner flex flex-col justify-between mb-6">
        
        {/* Top chamber bar - Clean with no "Rising Bubbles" tag */}
        <div className="flex items-center z-20">
          <span className="text-[11px] font-scifi font-bold text-cyan-300 flex items-center gap-2 bg-slate-950/80 px-3 py-1 rounded-full border border-cyan-500/40">
            <span>🫧</span> <span>KNOWLEDGE BUBBLE CHAMBER • TAP CIRCLES TO POP</span>
          </span>
        </div>

        {/* Ambient rising bubble particles floating from bottom to 75%+ height */}
        <div className="absolute inset-0 flex justify-around items-end px-6 pointer-events-auto z-10">
          {dayData.knowledgeBubbles.map((bubble, idx) => (
            <CircularBubble
              key={bubble.id}
              bubble={bubble}
              index={idx}
              onSelectBubble={(b) => setActiveBurst(b)}
            />
          ))}
        </div>

        {/* Bottom chamber floor grate */}
        <div className="w-full h-3 bg-gradient-to-t from-cyan-500/20 to-transparent border-t border-cyan-500/30 z-20"></div>

        {/* Modal Popup when a Circular Bubble is Popped */}
        {activeBurst && (
          <div className="absolute inset-0 bg-slate-950/85 backdrop-blur-md z-30 flex items-center justify-center p-4">
            <div className="bg-gradient-to-b from-indigo-950 to-slate-900 border-2 border-amber-400 p-5 rounded-3xl shadow-[0_0_40px_rgba(251,191,36,0.4)] max-w-md w-full text-left animate-fadeIn">
              <div className="flex items-center justify-between gap-3 mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-4xl animate-bounce">{activeBurst.icon}</span>
                  <div>
                    <span className="font-scifi font-black text-sm text-amber-300 uppercase block">
                      {activeBurst.title}
                    </span>
                    <span className="text-[10px] text-cyan-300 font-bold uppercase">
                      Knowledge Burst Unlocked! ✨
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => {
                    playSound('click');
                    setActiveBurst(null);
                  }}
                  className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white px-2.5 py-1 rounded-xl border border-slate-600 font-bold cursor-pointer"
                >
                  ✕ Close
                </button>
              </div>

              <div className="bg-slate-950/70 border border-cyan-500/30 p-3.5 rounded-2xl text-xs md:text-sm text-slate-100 leading-relaxed mb-4">
                {activeBurst.fact}
              </div>

              <div className="flex justify-end">
                <button
                  onClick={() => {
                    playSound('click');
                    setActiveBurst(null);
                  }}
                  className="bouncy-btn bouncy-btn-green bg-emerald-400 text-slate-950 font-bold text-xs px-4 py-2 rounded-xl font-scifi uppercase cursor-pointer"
                >
                  Got It! 🫧
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Navigation */}
      <div className="flex justify-between items-center pt-1 z-20 relative">
        <button
          onClick={() => {
            playSound('click');
            onBack();
          }}
          className="bouncy-btn bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs md:text-sm font-bold px-6 py-2.5 rounded-xl cursor-pointer"
        >
          ← Back
        </button>
        <button
          onClick={() => {
            playSound('power');
            onStartDay();
          }}
          className="bouncy-btn bouncy-btn-amber bg-amber-400 text-slate-950 font-black text-sm md:text-base px-9 py-3.5 rounded-2xl font-scifi uppercase cursor-pointer"
        >
          START DAY {dayData.day} 🚀
        </button>
      </div>
    </section>
  );
}
