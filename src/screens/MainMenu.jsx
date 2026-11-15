import React, { useState } from 'react';
import { AVATARS } from '../data/missionConfig';
import { playSound } from '../utils/soundFX';

export default function MainMenu({ cadetName, setCadetName, avatar, setAvatar, onStartMission }) {
  const [musicVol, setMusicVol] = useState(70);
  const [sfxVol, setSfxVol] = useState(85);
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <section aria-label="Cadet Launchpad" className="w-full max-w-xl text-center py-2 flex flex-col items-center">
      {/* Exact Mascot Moon Visual */}
      <div className="relative w-36 h-36 mx-auto mb-3">
        <div className="w-36 h-36 rounded-full bg-gradient-to-tr from-slate-200 via-white to-amber-100 energy-glow flex items-center justify-center relative overflow-hidden">
          <div className="absolute w-8 h-8 bg-slate-300/60 rounded-full top-5 left-6 blur-[1px]"></div>
          <div className="absolute w-10 h-10 bg-slate-300/60 rounded-full bottom-6 right-6 blur-[1px]"></div>
          <span className="text-5xl spinning-moon" aria-hidden="true">🌕</span>
        </div>
        <div className="absolute -bottom-2 -right-2 text-5xl floating drop-shadow-xl" title="Your Cadet Mascot">
          {avatar}
        </div>
      </div>

      <h1 className="font-scifi text-3xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-cyan-300 to-purple-400 mb-1 drop-shadow-md">
        MISSION TO THE MOON!
      </h1>
      <p className="text-sm md:text-base text-cyan-200 max-w-md mx-auto mb-4 font-medium leading-relaxed">
        Can you keep four astronauts safe at Shackleton Crater and bring home a Moon rock in seven days?
      </p>

      {/* Avatar & Name Selector Box */}
      <div className="w-full bg-slate-900/90 border-2 border-cyan-400/40 p-4 rounded-2xl max-w-md mx-auto mb-3 backdrop-blur-md shadow-2xl">
        <p className="text-xs font-bold text-cyan-300 uppercase tracking-wider mb-2">
          Pick Your Astronaut Avatar:
        </p>
        <div className="flex justify-center gap-3 mb-3 text-2xl" role="group" aria-label="Astronaut avatars">
          {AVATARS.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                playSound('click');
                setAvatar(item.emoji);
                setCadetName(item.label);
              }}
              aria-label={item.label}
              className={`avatar-opt p-2 rounded-xl transition cursor-pointer ${
                avatar === item.emoji
                  ? 'bg-cyan-500 scale-110 shadow-lg border-2 border-white'
                  : 'bg-slate-800 hover:bg-slate-700'
              }`}
            >
              {item.emoji}
            </button>
          ))}
        </div>

        <label htmlFor="cadetInput" className="sr-only">Enter Cadet Name</label>
        <input
          id="cadetInput"
          type="text"
          value={cadetName}
          onChange={(e) => setCadetName(e.target.value)}
          className="w-full bg-slate-950 border-2 border-cyan-500/60 rounded-xl px-4 py-2 text-center text-base font-bold text-amber-300 focus:outline-none focus:border-amber-400"
          placeholder="Enter Cadet Name"
        />
      </div>

      {/* Sound Settings Accordion */}
      <div className="w-full max-w-md bg-slate-900/80 border border-cyan-400/30 px-4 py-2.5 rounded-2xl mb-4 backdrop-blur-md text-left">
        <button
          onClick={() => {
            playSound('click');
            setSettingsOpen(!settingsOpen);
          }}
          className="w-full flex items-center justify-between text-xs font-scifi font-bold text-cyan-300 cursor-pointer"
        >
          <span className="flex items-center gap-1.5">⚙️ SOUND & MUSIC SETTINGS</span>
          <span>{settingsOpen ? '▲' : '▼'}</span>
        </button>

        {settingsOpen && (
          <div className="mt-3 space-y-2.5 pt-2 border-t border-slate-800">
            <div className="flex items-center justify-between text-xs text-slate-300">
              <span className="flex items-center gap-1">🎵 Music</span>
              <input
                type="range"
                min="0"
                max="100"
                value={musicVol}
                onChange={(e) => setMusicVol(e.target.value)}
                className="w-36 accent-cyan-400 cursor-pointer"
              />
            </div>
            <div className="flex items-center justify-between text-xs text-slate-300">
              <span className="flex items-center gap-1">🔊 Sound Effects</span>
              <input
                type="range"
                min="0"
                max="100"
                value={sfxVol}
                onChange={(e) => setSfxVol(e.target.value)}
                className="w-36 accent-cyan-400 cursor-pointer"
              />
            </div>
          </div>
        )}
      </div>

      {/* Launch Button */}
      <button
        onClick={() => {
          playSound('power');
          onStartMission();
        }}
        className="bouncy-btn bg-cyan-400 text-slate-950 font-black text-lg md:text-xl px-8 py-3.5 rounded-2xl font-scifi uppercase tracking-wider cursor-pointer transform"
      >
        Launch Cadet Mission! 🚀
      </button>
    </section>
  );
}
