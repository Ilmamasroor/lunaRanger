import { useEffect, useRef, useState } from 'react';
import { playSound } from '../utils/soundFX';
import { createMissionSession } from '../data/missionSession';

const buildPath = import.meta.env.BASE_URL + 'Build/';
const unityObject = 'Day 1 training';
let loaderPromise;

function loadUnity() {
  if (window.createUnityInstance) return Promise.resolve(window.createUnityInstance);
  loaderPromise ??= new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = buildPath + 'LunaRangers.loader.js';
    script.onload = () => {
      if (window.createUnityInstance) resolve(window.createUnityInstance);
      else reject(new Error('Invalid Unity loader'));
    };
    script.onerror = () => {
      script.remove();
      reject(new Error('Unity loader unavailable'));
    };
    document.head.append(script);
  }).catch(error => {
    loaderPromise = undefined;
    throw error;
  });
  return loaderPromise;
}

export default function Gameplay({ active, dayData, onCompleteDay }) {
  const canvas = useRef(null);
  const instance = useRef(null);
  const launch = useRef(null);
  const [mode, setMode] = useState('3d');
  const [status, setStatus] = useState('loading');
  const [progress, setProgress] = useState(0);
  const [snapshot, setSnapshot] = useState(null);
  const [mission] = useState(createMissionSession);
  const [engine, setEngine] = useState(null);
  const [engineError, setEngineError] = useState('');
  const [alertResult, setAlertResult] = useState('');
  const [practice, setPractice] = useState({ day: dayData.day, step: 0 });
  const practiceStep = practice.day === dayData.day ? practice.step : 0;
  const { requestSpacewalk, getSpacewalkRequest } = mission;
  const finished = mode === '2d'
    ? practiceStep === dayData.checklist.length
    : snapshot?.day === dayData.day && snapshot.finished && engine?.dayComplete && !engineError;

  useEffect(() => {
    function publish(event) {
      if (instance.current) {
        try {
          setEngine(mission.observe(event.detail));
          setEngineError('');
          setSnapshot(event.detail);
          setStatus('ready');
        } catch (error) {
          setEngineError(error.message);
        }
      }
    }
    window.addEventListener('lunarangers-campaign', publish);
    return () => window.removeEventListener('lunarangers-campaign', publish);
  }, [mission]);

  useEffect(() => {
    let accepting = true;
    async function request(event) {
      const current = instance.current;
      if (!current) return;
      const { token, day } = event.detail;
      let result = { approved: false, message: 'Spacewalk clearance unavailable. Try again.' };
      try {
        const input = getSpacewalkRequest?.(day);
        if (input?.astronautId && input.taskId) {
          const response = await requestSpacewalk(input);
          if (typeof response?.approved === 'boolean' && response.requestId &&
              response.astronautId === input.astronautId && response.taskId === input.taskId) result = response;
        }
      } catch { /* The airlock stays closed when the engine is unavailable. */ }
      if (accepting && instance.current === current) {
        current.SendMessage(unityObject, 'ApplySpacewalkDecision', JSON.stringify({ ...result, token }));
      }
    }
    window.addEventListener('lunarangers-spacewalk', request);
    return () => {
      accepting = false;
      window.removeEventListener('lunarangers-spacewalk', request);
    };
  }, [requestSpacewalk, getSpacewalkRequest]);

  useEffect(() => {
    if (mode !== '3d') return;
    let cancelled = false;
    let handshakeTimeout;
    const target = canvas.current;

    // React Strict Mode runs setup twice. Both setups share the same canvas launch.
    if (!launch.current) {
      launch.current = loadUnity().then(create => create(target, {
        dataUrl: buildPath + 'LunaRangers.data',
        frameworkUrl: buildPath + 'LunaRangers.framework.js',
        codeUrl: buildPath + 'LunaRangers.wasm',
        streamingAssetsUrl: import.meta.env.BASE_URL + 'StreamingAssets',
        companyName: 'Neural Knights',
        productName: 'LunaRangers',
        productVersion: '1.0',
        devicePixelRatio: Math.min(window.devicePixelRatio || 1, 1.5),
      }, setProgress));
    }
    const pending = launch.current;
    pending.then(unity => {
      if (cancelled) return;
      instance.current = unity;
      unity.SendMessage(unityObject, 'SetCampaignHost', 'engine');
      handshakeTimeout = setTimeout(() => setStatus(value => value === 'ready' ? value : 'unavailable'), 8000);
    }).catch(() => {
      if (!cancelled) setStatus('unavailable');
    });
    return () => {
      cancelled = true;
      clearTimeout(handshakeTimeout);
      instance.current = null;
      // Leave the pending launch available to Strict Mode's immediate second setup.
      queueMicrotask(() => {
        if (target.isConnected) return;
        pending.then(unity => unity.Quit()).catch(() => {});
        if (launch.current === pending) launch.current = null;
      });
    };
  }, [mode]);

  useEffect(() => {
    if (!active || mode !== '3d' || status !== 'ready') return;
    if (snapshot?.finished && snapshot.day + 1 === dayData.day) {
      instance.current?.SendMessage(unityObject, 'ResumeCampaignDay', String(dayData.day));
    }
    if (snapshot?.day === dayData.day) canvas.current?.focus();
  }, [active, dayData.day, mode, snapshot?.day, snapshot?.finished, status]);

  useEffect(() => {
    if (!active || !finished) return;
    const completion = setTimeout(() => {
      playSound('power');
      onCompleteDay();
    }, 700);
    return () => clearTimeout(completion);
  }, [active, finished, onCompleteDay]);

  function advancePractice() {
    playSound('click');
    setPractice({ day: dayData.day, step: practiceStep + 1 });
  }

  const canChoosePractice = dayData.day === 1 && !snapshot?.step;
  return (
    <section hidden={!active} className="w-full">
      <div className="mx-auto w-full max-w-7xl">
        <div className="mb-2 flex min-h-7 flex-wrap items-center justify-between gap-2 text-xs text-cyan-200">
          <span>{mode === '2d' ? '2D walkthrough' : 'Mission control'}</span>
          {mode === '3d' && engine && (
            <span aria-label="Mission engine supplies">
              Oxygen {engine.resources.oxygen.toFixed(1)} kg · Water {engine.resources.water.toFixed(1)} kg ·
              {' '}Food {engine.resources.food.toFixed(1)} kg · Energy {engine.resources.energy.toFixed(1)} kWh
              {engine.sampleSecured && ' · Sample secured'}
            </span>
          )}
          {mode === '3d' && dayData.day === 5 && engine?.alert && (
            <button type="button"
              className="rounded border border-amber-500 px-3 py-1 text-amber-300"
              onClick={() => {
                const result = requestSpacewalk(getSpacewalkRequest(5));
                setAlertResult(result.approved ? 'Spacewalk cleared.' : result.message);
                canvas.current?.focus();
              }}>
              Check spacewalk clearance
            </button>
          )}
          {mode === '3d' && canChoosePractice && (
            <button type="button" onClick={() => setMode('2d')} className="rounded border border-cyan-700 px-3 py-1">
              Use 2D walkthrough
            </button>
          )}
        </div>
        {mode === '3d' ? (
          <div className="relative aspect-video w-full overflow-hidden rounded-2xl border border-cyan-900 bg-slate-950">
            <canvas ref={canvas} id="unity-canvas" tabIndex={0} width={1280} height={720}
              aria-label="LunaRangers lunar outpost game" className="block h-full w-full" />
            {status !== 'ready' && (
              <div role="status" className="absolute inset-0 grid place-content-center bg-slate-950 px-6 text-center text-slate-200">
                {status === 'loading' ? 'Loading lunar outpost ' + Math.round(progress * 100) + '%' :
                  'The 3D outpost could not load. Use the 2D walkthrough to continue.'}
              </div>
            )}
          </div>
        ) : (
          <div className="rounded-2xl border border-cyan-900 bg-slate-900 p-6">
            <h2 className="mb-2 text-xl font-bold text-cyan-200">Day {dayData.day} · {dayData.title}</h2>
            <p className="mb-4 text-sm text-slate-300">{dayData.subtitle}</p>
            <ol className="mb-4 list-inside list-decimal space-y-2">
              {dayData.checklist.map((label, index) => (
                <li key={label} className={index < practiceStep ? 'text-emerald-300 line-through' : 'text-slate-200'}>
                  {label}
                </li>
              ))}
            </ol>
            <button type="button" onClick={advancePractice} disabled={finished}
              className="rounded-lg bg-amber-400 px-4 py-2 font-bold text-slate-950 disabled:opacity-60">
              {finished ? 'Walkthrough complete' : dayData.checklist[practiceStep]}
            </button>
          </div>
        )}
        {mode === '3d' && dayData.day === 5 && alertResult && <p role="status" className="mt-1 text-sm text-amber-300">{alertResult}</p>}
        {mode === '3d' && engineError && <p role="alert" className="mt-1 text-sm text-amber-300">Mission engine: {engineError}</p>}
      </div>
    </section>
  );
}
