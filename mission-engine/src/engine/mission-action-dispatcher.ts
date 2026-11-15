import { DispatchResult, MissionAction, MissionConfig, MissionState } from './engine.types';
import { advanceMissionCycle } from './mission-cycle';
import { requestEvaClearance, startEvaExecution } from './eva-workflow';
import { collectLunarSample, completeEvaAndReturnSample, abortEva } from './sample-collection';
import { cloneMissionState } from './resource-simulation';

export function dispatchMissionAction(
  state: MissionState,
  action: MissionAction,
  config: MissionConfig
): DispatchResult {
  if (!state || typeof state !== 'object') {
    return {
      success: false,
      error: 'Invalid mission state provided to dispatcher.',
      state: null,
    };
  }

  if (!action || typeof action !== 'object' || typeof action.type !== 'string') {
    return {
      success: false,
      error: 'Malformed action payload: missing valid action type.',
      state: null,
    };
  }

  const payload = action.payload ?? {};

  switch (action.type) {
    case 'ADVANCE_CYCLE': {
      const cycles =
        payload.cyclesToAdvance !== undefined ? (payload.cyclesToAdvance as number) : 1;
      return advanceMissionCycle(state, config, cycles);
    }

    case 'DIAGNOSE_EQUIPMENT': {
      const equipmentId = payload.equipmentId as string;
      if (!equipmentId || typeof equipmentId !== 'string') {
        return { success: false, error: 'Missing equipmentId for diagnosis.', state: null };
      }
      const nextState = cloneMissionState(state);
      const item = nextState.equipment.find((e) => e.id === equipmentId);
      if (!item) {
        return { success: false, error: `Equipment not found: ${equipmentId}`, state: null };
      }
      item.diagnosed = true;
      nextState.history.push(`Diagnosed equipment: ${item.name} (${item.status}).`);
      return { success: true, error: null, state: nextState };
    }

    case 'REPAIR_EQUIPMENT': {
      const equipmentId = payload.equipmentId as string;
      if (!equipmentId || typeof equipmentId !== 'string') {
        return { success: false, error: 'Missing equipmentId for repair.', state: null };
      }
      const nextState = cloneMissionState(state);
      const item = nextState.equipment.find((e) => e.id === equipmentId);
      if (!item) {
        return { success: false, error: `Equipment not found: ${equipmentId}`, state: null };
      }
      const objectiveMap: Record<string, number> = {
        'heater-primary': 1,
        'solar-array': 2,
        'water-recycler': 3,
        'co2-scrubber': 4,
      };
      const targetDay = objectiveMap[item.id];
      if (targetDay && state.currentCycle !== targetDay) {
        return {
          success: false,
          error: `${item.name} can only be repaired during Mission Day ${targetDay}.`,
          state: null,
        };
      }
      if (!item.diagnosed) {
        return {
          success: false,
          error: `Equipment ${item.name} must be diagnosed before repair.`,
          state: null,
        };
      }
      item.status = 'OPERATIONAL';
      item.damageLevel = 0;

      // Mark the objective associated with this day's equipment repair.
      if (targetDay) {
        const obj = nextState.objectives.find((o) => o.day === targetDay);
        if (obj) obj.completed = true;
      }

      nextState.history.push(`Repaired equipment: ${item.name} is now OPERATIONAL.`);
      return { success: true, error: null, state: nextState };
    }

    case 'TOGGLE_SHELTER': {
      if (typeof payload.sheltered !== 'boolean') {
        return { success: false, error: 'sheltered must be a boolean.', state: null };
      }
      if (state.evaState.status === 'IN_PROGRESS') {
        return { success: false, error: 'Cannot change habitat shelter state while an astronaut is outside on EVA.', state: null };
      }
      const sheltered = payload.sheltered;
      if (!sheltered && state.hazards.solarRadiationAlertActive) {
        return { success: false, error: 'Cannot leave radiation shelter during an active solar radiation alert.', state: null };
      }
      const nextState = cloneMissionState(state);
      nextState.crewStatus.sheltered = sheltered;
      nextState.history.push(
        sheltered ? 'Crew entered radiation shelter.' : 'Crew exited radiation shelter.'
      );
      return { success: true, error: null, state: nextState };
    }

    case 'REQUEST_EVA_CLEARANCE': {
      return requestEvaClearance(
        state,
        config,
        payload.astronautId as string,
        payload.targetDurationMinutes as number
      );
    }

    case 'START_EVA': {
      return startEvaExecution(state, config);
    }

    case 'COLLECT_LUNAR_SAMPLE': {
      return collectLunarSample(
        state,
        payload.sampleId as string,
        payload.containerId as string
      );
    }

    case 'COMPLETE_EVA_AND_RETURN': {
      return completeEvaAndReturnSample(state);
    }

    case 'ABORT_EVA': {
      return abortEva(state);
    }

    case 'VERIFY_FINAL_MISSION_STATUS': {
      const priorObjectivesComplete =
        [1, 2, 3, 4, 5, 6].every((day) =>
          state.objectives.some((objective) => objective.day === day && objective.completed)
        );

      if (
        state.currentCycle < 7 ||
        state.evaState.status === 'IN_PROGRESS' ||
        !state.crewStatus.sheltered ||
        !priorObjectivesComplete ||
        !state.sampleCollectionState.collected ||
        !state.sampleCollectionState.securedInHabitat
      ) {
        return {
          success: false,
          error: 'Mission completion check failed: Reach Day 7, complete Days 1–6, return from EVA, shelter the crew, and secure the lunar sample.',
          state: null,
        };
      }

      const nextState = cloneMissionState(state);
      const day7Obj = nextState.objectives.find((o) => o.day === 7);
      if (day7Obj) day7Obj.completed = true;
      nextState.history.push('Day 7 final verification passed: Mission Ready & Complete.');
      return { success: true, error: null, state: nextState };
    }

    default:
      return {
        success: false,
        error: `Unsupported mission action type: ${(action as { type: string }).type}`,
        state: null,
      };
  }
}
