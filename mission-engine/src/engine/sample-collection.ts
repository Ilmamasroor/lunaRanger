import { DispatchResult, MissionState } from './engine.types';
import { cloneMissionState } from './resource-simulation';

export function collectLunarSample(
  state: MissionState,
  sampleId: string,
  containerId: string
): DispatchResult {
  if (state.currentCycle !== 6) {
    return {
      success: false,
      error: 'Lunar sample collection is only available during Mission Day 6.',
      state: null,
    };
  }

  if (state.evaState.status !== 'IN_PROGRESS' || !state.evaState.cleared) {
    return {
      success: false,
      error: 'Sample collection rejected: Astronaut must be actively executing an authorized EVA.',
      state: null,
    };
  }

  if (!sampleId || typeof sampleId !== 'string' || sampleId.trim().length === 0) {
    return {
      success: false,
      error: 'Invalid sampleId provided for lunar sample collection.',
      state: null,
    };
  }

  if (!containerId || typeof containerId !== 'string' || containerId.trim().length === 0) {
    return {
      success: false,
      error: 'Invalid containerId provided for sample containment.',
      state: null,
    };
  }

  if (state.sampleCollectionState.collected) {
    return {
      success: false,
      error: `Sample ${state.sampleCollectionState.sampleId} has already been collected.`,
      state: null,
    };
  }

  const nextState = cloneMissionState(state);
  nextState.sampleCollectionState = {
    sampleId: sampleId.trim(),
    containerId: containerId.trim(),
    collected: true,
    securedInHabitat: false,
  };
  nextState.history.push(
    `Collected lunar sample ${sampleId.trim()} into container ${containerId.trim()}.`
  );

  return {
    success: true,
    error: null,
    state: nextState,
  };
}

export function completeEvaAndReturnSample(state: MissionState): DispatchResult {
  if (state.evaState.status !== 'IN_PROGRESS') {
    return {
      success: false,
      error: 'Cannot complete EVA return: No active EVA in progress.',
      state: null,
    };
  }

  const nextState = cloneMissionState(state);
  nextState.evaState.status = 'COMPLETED';
  nextState.evaState.cleared = false;
  nextState.crewStatus.sheltered = true;

  if (nextState.sampleCollectionState.collected) {
    nextState.sampleCollectionState.securedInHabitat = true;
    const day6Obj = nextState.objectives.find((o) => o.day === 6);
    if (day6Obj) {
      day6Obj.completed = true;
    }
    nextState.history.push(
      `Astronaut ${nextState.evaState.astronautId} returned safely and secured sample ${nextState.sampleCollectionState.sampleId} in habitat storage.`
    );
  } else {
    nextState.history.push(
      `Astronaut ${nextState.evaState.astronautId} returned safely to habitat without sample collection.`
    );
  }

  return {
    success: true,
    error: null,
    state: nextState,
  };
}

/**
 * Aborts an active EVA and returns the astronaut to the habitat.
 * A collected sample remains unsecured and is not counted as a completed objective.
 */
export function abortEva(state: MissionState): DispatchResult {
  if (state.evaState.status !== 'IN_PROGRESS') {
    return {
      success: false,
      error: 'Cannot abort EVA: no active EVA is in progress.',
      state: null,
    };
  }

  const nextState = cloneMissionState(state);
  nextState.evaState.status = 'ABORTED';
  nextState.evaState.cleared = false;
  nextState.crewStatus.sheltered = true;
  nextState.history.push(
    `EVA aborted. Astronaut ${nextState.evaState.astronautId ?? 'unknown'} returned to habitat.`
  );
  return { success: true, error: null, state: nextState };
}
