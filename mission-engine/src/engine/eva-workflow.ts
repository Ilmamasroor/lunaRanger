import { DispatchResult, MissionConfig, MissionState } from './engine.types';
import { cloneMissionState, validateMissionConfig, validateMissionResources } from './resource-simulation';

export function requestEvaClearance(
  state: MissionState,
  config: MissionConfig,
  astronautId: string,
  targetDurationMinutes: number
): DispatchResult {
  if (!astronautId || typeof astronautId !== 'string' || astronautId.trim().length === 0) {
    return {
      success: false,
      error: 'Invalid astronautId provided for EVA clearance.',
      state: null,
    };
  }

  if (
    typeof targetDurationMinutes !== 'number' ||
    !Number.isFinite(targetDurationMinutes) ||
    targetDurationMinutes <= 0 ||
    targetDurationMinutes > 240
  ) {
    return {
      success: false,
      error: 'EVA duration must be between 1 and 240 minutes.',
      state: null,
    };
  }

  if (state.hazards.solarRadiationAlertActive) {
    return {
      success: false,
      error: 'EVA clearance denied: Active solar radiation alert in progress. Habitat lockdown enforced.',
      state: null,
    };
  }

  if (state.hazards.micrometeoriteWarningActive) {
    return {
      success: false,
      error: 'EVA clearance denied: Active micrometeorite hazard warning.',
      state: null,
    };
  }

  if (state.crewStatus.healthStatus !== 'NOMINAL') {
    return {
      success: false,
      error: `EVA clearance denied: Crew health status is ${state.crewStatus.healthStatus}.`,
      state: null,
    };
  }

  if (state.resources.oxygen < config.minOxygenForEva) {
    return {
      success: false,
      error: `EVA clearance denied: Oxygen (${state.resources.oxygen}) below threshold (${config.minOxygenForEva}).`,
      state: null,
    };
  }

  if (state.resources.energy < config.minEnergyForEva) {
    return {
      success: false,
      error: `EVA clearance denied: Energy (${state.resources.energy}) below threshold (${config.minEnergyForEva}).`,
      state: null,
    };
  }

  const nextState = cloneMissionState(state);
  nextState.evaState = {
    status: 'CLEARED',
    cleared: true,
    astronautId: astronautId.trim(),
    targetDurationMinutes,
  };
  nextState.crewStatus.sheltered = false;
  nextState.history.push(
    `EVA cleared for ${astronautId.trim()} (${targetDurationMinutes} mins) on Cycle ${nextState.currentCycle}.`
  );

  return {
    success: true,
    error: null,
    state: nextState,
  };
}

export function startEvaExecution(state: MissionState, config: MissionConfig): DispatchResult {
  const configError = validateMissionConfig(config);
  const stateError = validateMissionResources(state);
  if (configError || stateError) {
    return { success: false, error: configError ?? stateError, state: null };
  }

  if (state.crewStatus.healthStatus !== 'NOMINAL') {
    return { success: false, error: `Cannot begin EVA: crew health is ${state.crewStatus.healthStatus}.`, state: null };
  }
  if (state.resources.oxygen < config.minOxygenForEva || state.resources.energy < config.minEnergyForEva) {
    return { success: false, error: 'Cannot begin EVA: oxygen or energy is below the configured clearance threshold.', state: null };
  }

  if (!state.evaState.cleared || state.evaState.status !== 'CLEARED') {
    return {
      success: false,
      error: 'Cannot begin EVA: Spacewalk has not been cleared by the Mission Engine.',
      state: null,
    };
  }

  if (state.hazards.solarRadiationAlertActive || state.hazards.micrometeoriteWarningActive) {
    return {
      success: false,
      error: 'Cannot begin EVA: Environmental hazard triggered prior to airlock depressurization.',
      state: null,
    };
  }

  const nextState = cloneMissionState(state);
  nextState.evaState.status = 'IN_PROGRESS';
  nextState.history.push(
    `Astronaut ${nextState.evaState.astronautId} exited airlock for EVA.`
  );

  return {
    success: true,
    error: null,
    state: nextState,
  };
}
