import { dispatchMissionAction } from '../../mission-engine/src/index.ts';
import { MISSION_DAYS } from './missionConfig.js';
import pipeline from './pipeline-snapshot.json';

const value = id => pipeline.parameters[id].value;
const config = {
  oxygenConsumptionPerCrewPerCycle: value('crew_oxygen_consumption'),
  co2GenerationPerCrewPerCycle: value('crew_co2_production'),
  waterConsumptionPerCrewPerCycle: value('crew_water_requirement'),
  foodConsumptionPerCrewPerCycle: value('crew_food_mass'),
  waterRecyclerEfficiency: value('overall_iss_water_recovery_milestone') / 100,
  // Trainer energy budget and clearance thresholds, in kWh and kg.
  baseEnergyConsumptionPerCycle: 20, solarGenerationPerCycle: 45,
  co2ScrubberEfficiency: .9, minOxygenForEva: 50, minEnergyForEva: 80,
};
const equipment = [
  ['heater-primary', 'Heater', 'OFFLINE'],
  ['solar-array', 'Solar array', 'DEGRADED'],
  ['water-recycler', 'Water recycler', 'DEGRADED'],
  ['co2-scrubber', 'Air scrubber', 'OPERATIONAL'],
];
const evaTasks = { 1: 'recover-battery', 5: 'shelter-clearance-check', 6: 'excavate-sample' };

export function createMissionSession() {
  let state = {
    missionId: 'lunarangers', currentCycle: 1, maxCycles: MISSION_DAYS.length,
    crewStatus: { activeCrewSize: pipeline.crewSize, healthStatus: 'NOMINAL', sheltered: true },
    resources: { oxygen: 70, carbonDioxide: .5, water: 170, food: 90, energy: 140 },
    equipment: equipment.map(([id, name, status]) => ({ id, name, status, damageLevel: 0, diagnosed: false })),
    hazards: { solarRadiationAlertActive: false, micrometeoriteWarningActive: false },
    evaState: { status: 'STANDBY', cleared: false, astronautId: null, targetDurationMinutes: 0 },
    sampleCollectionState: { sampleId: null, containerId: null, collected: false, securedInHabitat: false },
    objectives: MISSION_DAYS.map(({ day, title }) => ({ id: 'day-' + day, day, description: title, completed: false })),
    history: [],
  };
  let checkpoint = state;
  let sequence = 0;
  let previous;

  function dispatch(type, payload) {
    const result = dispatchMissionAction(state, { type, payload }, config);
    if (!result.success) throw new Error(result.error);
    state = result.state;
  }

  function getSpacewalkRequest(day) {
    return { astronautId: 'cadet', taskId: evaTasks[day] };
  }

  function requestSpacewalk(input) {
    const result = { ...input, requestId: 'eva-' + ++sequence };
    if (input.astronautId !== 'cadet' || !input.taskId || input.taskId !== evaTasks[state.currentCycle] ||
        state.evaState.status === 'IN_PROGRESS') {
      return { ...result, approved: false, message: 'Spacewalk unavailable for this task.' };
    }
    const before = state;
    try {
      dispatch('REQUEST_EVA_CLEARANCE', { astronautId: input.astronautId, targetDurationMinutes: 10 });
      dispatch('START_EVA');
      return { ...result, approved: true };
    } catch (error) {
      state = before;
      return { ...result, approved: false, message: error.message };
    }
  }

  function observe(snapshot) {
    const { day, step, outside, finished } = snapshot;
    if (!Number.isInteger(day) || day < 1 || day > MISSION_DAYS.length ||
        !Number.isInteger(step) || step < 0 || typeof outside !== 'boolean' || typeof finished !== 'boolean') {
      throw new Error('Invalid outpost state.');
    }
    if (day !== state.currentCycle) {
      if (day !== state.currentCycle + 1) throw new Error('Mission days must advance in order.');
      if (day === 5) {
        state = {
          ...state,
          hazards: { ...state.hazards, solarRadiationAlertActive: pipeline.donki.hazard_type === 'solar_particle_event' },
          crewStatus: { ...state.crewStatus, sheltered: false },
        };
      }
      if (day === 6) state = { ...state, hazards: { ...state.hazards, solarRadiationAlertActive: false } };
      dispatch('ADVANCE_CYCLE');
      checkpoint = state;
    }
    if (!outside && previous?.day === day && step < previous.step) {
      if (state.evaState.status === 'IN_PROGRESS') dispatch('ABORT_EVA');
      // The retry respawns the pickup, including an unsecured lunar sample.
      state = checkpoint;
    }
    if (outside && state.evaState.status !== 'IN_PROGRESS') throw new Error('The airlock needs engine clearance.');
    if (day === 6 && step >= 3 && !state.sampleCollectionState.collected) {
      dispatch('COLLECT_LUNAR_SAMPLE', { sampleId: 'MOON-ROCK-01', containerId: 'SAMPLE-CASE-01' });
    }
    if (!outside && previous?.outside && state.evaState.status === 'IN_PROGRESS') {
      dispatch('COMPLETE_EVA_AND_RETURN');
    }
    if (finished && !state.objectives[day - 1].completed) {
      if (day <= 4) {
        const equipmentId = equipment[day - 1][0];
        dispatch('DIAGNOSE_EQUIPMENT', { equipmentId });
        dispatch('REPAIR_EQUIPMENT', { equipmentId });
      } else if (day === 5) {
        dispatch('TOGGLE_SHELTER', { sheltered: true });
      } else if (day === 7) {
        dispatch('VERIFY_FINAL_MISSION_STATUS');
      }
    }
    previous = snapshot;
    return {
      resources: state.resources,
      alert: state.hazards.solarRadiationAlertActive,
      dayComplete: state.objectives[day - 1].completed,
      sampleSecured: state.sampleCollectionState.securedInHabitat,
    };
  }

  return { getSpacewalkRequest, requestSpacewalk, observe };
}
