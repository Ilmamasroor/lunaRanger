import React from 'react';

export function StylizedRocketIcon({ className = "w-7 h-7" }) {
  return (
    <svg
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`${className} shrink-0 filter drop-shadow-[0_0_8px_rgba(56,189,248,0.7)]`}
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="rocketBodyGrad" x1="16" y1="16" x2="48" y2="48" gradientUnits="userSpaceOnUse">
          <stop stopColor="#E0F2FE" />
          <stop offset="0.5" stopColor="#38BDF8" />
          <stop offset="1" stopColor="#0284C7" />
        </linearGradient>
        <linearGradient id="rocketNoseGrad" x1="38" y1="6" x2="58" y2="26" gradientUnits="userSpaceOnUse">
          <stop stopColor="#F43F5E" />
          <stop offset="1" stopColor="#E11D48" />
        </linearGradient>
        <linearGradient id="rocketFlameGrad" x1="10" y1="54" x2="2" y2="62" gradientUnits="userSpaceOnUse">
          <stop stopColor="#FBBF24" />
          <stop offset="0.5" stopColor="#F97316" />
          <stop offset="1" stopColor="#EF4444" />
        </linearGradient>
      </defs>

      <path d="M17 47 L6 58 C5 59 7 61 9 60 L19 51 Z" fill="url(#rocketFlameGrad)" />
      <circle cx="12" cy="52" r="3" fill="#FEF08A" opacity="0.8" />
      <path d="M23 43 L12 47 C10 48 11 51 13 51 L25 47 Z" fill="#0369A1" />
      <path d="M43 23 L47 12 C48 10 51 11 51 13 L47 25 Z" fill="#0369A1" />
      <path d="M20 44 C26 44 42 38 52 24 C54 21 54 18 51 15 C48 12 45 12 42 14 C28 24 22 40 22 46 Z" fill="url(#rocketBodyGrad)" />
      <path d="M45 15 C48 12 51 12 54 15 C54 18 54 21 51 24 Z" fill="url(#rocketNoseGrad)" />
      <circle cx="36" cy="28" r="4.5" fill="#0C4A6E" stroke="#38BDF8" strokeWidth="1.5" />
      <circle cx="35" cy="26.5" r="1.5" fill="#BAE6FD" />
    </svg>
  );
}
