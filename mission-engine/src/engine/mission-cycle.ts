import { DispatchResult, MissionConfig, MissionState } from './engine.types';
import { cloneMissionState, simulateCycleResources, validateMissionConfig, validateMissionResources } from './resource-simulation';

export function advanceMissionCycle(
  state: MissionState,
  config: MissionConfig,
  cyclesToAdvance: number = 1
): DispatchResult {
  const configError = validateMissionConfig(config);
  if (configError) return { success: false, error: configError, state: null };
  const stateError = validateMissionResources(state);
  if (stateError) return { success: false, error: stateError, state: null };

  if (
    typeof cyclesToAdvance !== 'number' ||
    !Number.isFinite(cyclesToAdvance) ||
    !Number.isInteger(cyclesToAdvance) ||
    cyclesToAdvance <= 0
  ) {
    return {
      success: false,
      error: 'Invalid cycle increment: cyclesToAdvance must be a positive integer.',
      state: null,
    };
  }

  if (cyclesToAdvance !== 1) {
    return {
      success: false,
      error: 'Mission progression must advance exactly one day at a time.',
      state: null,
    };
  }

  if (
    !Number.isSafeInteger(state.currentCycle) ||
    state.currentCycle + cyclesToAdvance > Number.MAX_SAFE_INTEGER
  ) {
    return {
      success: false,
      error: 'Cycle overflow detected: resulting cycle exceeds MAX_SAFE_INTEGER.',
      state: null,
    };
  }

  const currentObjective = state.objectives.find((objective) => objective.day === state.currentCycle);
  if (!currentObjective || !currentObjective.completed) {
    return {
      success: false,
      error: `Cannot advance: Mission Day ${state.currentCycle} objective must be completed first.`,
      state: null,
    };
  }

  if (state.currentCycle + cyclesToAdvance > state.maxCycles) {
    return {
      success: false,
      error: `Cannot advance beyond max mission cycles (${state.maxCycles}).`,
      state: null,
    };
  }

  if (state.evaState.status === 'IN_PROGRESS') {
    return {
      success: false,
      error: 'Cannot advance mission cycle while an astronaut is outside on EVA.',
      state: null,
    };
  }

  const nextState = cloneMissionState(state);

  for (let i = 0; i < cyclesToAdvance; i++) {
    nextState.currentCycle += 1;
    nextState.resources = simulateCycleResources(nextState, config);

    if (nextState.resources.oxygen <= 0) {
      nextState.crewStatus.healthStatus = 'CRITICAL';
    } else if (nextState.resources.carbonDioxide > 5.0 || nextState.resources.energy <= 10) {
      nextState.crewStatus.healthStatus = 'CAUTION';
    } else {
      nextState.crewStatus.healthStatus = 'NOMINAL';
    }

    // Update Day 5 shelter objective if solar alert is active and crew is sheltered
    if (
      nextState.currentCycle === 5 &&
      nextState.hazards.solarRadiationAlertActive &&
      nextState.crewStatus.sheltered
    ) {
      const day5Obj = nextState.objectives.find((o) => o.day === 5);
      if (day5Obj) day5Obj.completed = true;
    }

    nextState.history.push(`Advanced to Mission Cycle ${nextState.currentCycle}.`);
  }

  return {
    success: true,
    error: null,
    state: nextState,
  };
}
