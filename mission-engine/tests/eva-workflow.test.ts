import { describe, it, expect } from 'vitest';
import { dispatchMissionAction } from '../src/engine/mission-action-dispatcher';
import { MissionConfig, MissionState } from '../src/engine/engine.types';

const defaultConfig: MissionConfig = {
  oxygenConsumptionPerCrewPerCycle: 2.0,
  co2GenerationPerCrewPerCycle: 1.5,
  waterConsumptionPerCrewPerCycle: 3.0,
  foodConsumptionPerCrewPerCycle: 2.0,
  baseEnergyConsumptionPerCycle: 20.0,
  solarGenerationPerCycle: 45.0,
  co2ScrubberEfficiency: 0.9,
  waterRecyclerEfficiency: 0.85,
  minOxygenForEva: 50.0,
  minEnergyForEva: 80.0,
};

function createReadyForEvaState(): MissionState {
  return {
    missionId: 'test-eva',
    currentCycle: 6,
    maxCycles: 7,
    crewStatus: { activeCrewSize: 4, healthStatus: 'NOMINAL', sheltered: true },
    resources: { oxygen: 90, carbonDioxide: 0.5, water: 90, food: 90, energy: 140 },
    equipment: [],
    hazards: { solarRadiationAlertActive: false, micrometeoriteWarningActive: false },
    evaState: { status: 'STANDBY', cleared: false, astronautId: null, targetDurationMinutes: 0 },
    sampleCollectionState: { sampleId: null, containerId: null, collected: false, securedInHabitat: false },
    objectives: [
      { id: 'day-1', day: 1, description: 'Heat', completed: true },
      { id: 'day-2', day: 2, description: 'Solar', completed: true },
      { id: 'day-3', day: 3, description: 'Water', completed: true },
      { id: 'day-4', day: 4, description: 'CO2', completed: true },
      { id: 'day-5', day: 5, description: 'Shelter', completed: true },
      { id: 'day-6', day: 6, description: 'Sample', completed: false },
      { id: 'day-7', day: 7, description: 'Final', completed: false },
    ],
    history: [],
  };
}

describe('EVA & Lunar Sample Collection Workflow', () => {
  it('blocks EVA clearance during active solar radiation alert', () => {
    const state = createReadyForEvaState();
    state.hazards.solarRadiationAlertActive = true;

    const res = dispatchMissionAction(
      state,
      { type: 'REQUEST_EVA_CLEARANCE', payload: { astronautId: 'ASTRO-1', targetDurationMinutes: 90 } },
      defaultConfig
    );
    expect(res.success).toBe(false);
    expect(res.error).toContain('solar radiation alert');
  });

  it('completes full Day 6 EVA, sample collection, safe return, and Day 7 verification', () => {
    let state = createReadyForEvaState();

    // 1. Request EVA clearance
    let res = dispatchMissionAction(
      state,
      { type: 'REQUEST_EVA_CLEARANCE', payload: { astronautId: 'ASTRO-1', targetDurationMinutes: 90 } },
      defaultConfig
    );
    expect(res.success).toBe(true);
    state = res.state!;

    // 2. Start EVA
    res = dispatchMissionAction(state, { type: 'START_EVA' }, defaultConfig);
    expect(res.success).toBe(true);
    state = res.state!;

    // 3. Collect Lunar Sample
    res = dispatchMissionAction(
      state,
      { type: 'COLLECT_LUNAR_SAMPLE', payload: { sampleId: 'LUNA-ROCK-04', containerId: 'CONT-01' } },
      defaultConfig
    );
    expect(res.success).toBe(true);
    state = res.state!;

    // 4. Complete EVA & Return
    res = dispatchMissionAction(state, { type: 'COMPLETE_EVA_AND_RETURN' }, defaultConfig);
    expect(res.success).toBe(true);
    state = res.state!;
    expect(state.sampleCollectionState.securedInHabitat).toBe(true);
    expect(state.objectives.find((o) => o.day === 6)?.completed).toBe(true);

    // 5. Advance to Day 7 before final verification
    res = dispatchMissionAction(state, { type: 'ADVANCE_CYCLE' }, defaultConfig);
    expect(res.success).toBe(true);
    state = res.state!;

    // 6. Day 7 Final Check
    res = dispatchMissionAction(state, { type: 'VERIFY_FINAL_MISSION_STATUS' }, defaultConfig);
    expect(res.success).toBe(true);
    expect(res.state!.objectives.find((o) => o.day === 7)?.completed).toBe(true);
  });
  it('aborts an active EVA safely without crediting an unsecured sample', () => {
    let state = createReadyForEvaState();
    let res = dispatchMissionAction(
      state,
      { type: 'REQUEST_EVA_CLEARANCE', payload: { astronautId: 'ASTRO-2', targetDurationMinutes: 45 } },
      defaultConfig
    );
    expect(res.success).toBe(true);
    state = res.state!;
    res = dispatchMissionAction(state, { type: 'START_EVA' }, defaultConfig);
    expect(res.success).toBe(true);
    state = res.state!;
    res = dispatchMissionAction(state, { type: 'COLLECT_LUNAR_SAMPLE', payload: { sampleId: 'S-2', containerId: 'C-2' } }, defaultConfig);
    expect(res.success).toBe(true);
    state = res.state!;
    res = dispatchMissionAction(state, { type: 'ABORT_EVA' }, defaultConfig);
    expect(res.success).toBe(true);
    expect(res.state!.evaState.status).toBe('ABORTED');
    expect(res.state!.crewStatus.sheltered).toBe(true);
    expect(res.state!.sampleCollectionState.collected).toBe(true);
    expect(res.state!.sampleCollectionState.securedInHabitat).toBe(false);
    expect(res.state!.objectives.find((o) => o.day === 6)?.completed).toBe(false);
  });


  it('rechecks crew health and resources immediately before EVA starts', () => {
    let state = createReadyForEvaState();
    let res = dispatchMissionAction(
      state,
      { type: 'REQUEST_EVA_CLEARANCE', payload: { astronautId: 'ASTRO-3', targetDurationMinutes: 30 } },
      defaultConfig
    );
    expect(res.success).toBe(true);
    state = res.state!;
    state.crewStatus.healthStatus = 'CRITICAL';
    res = dispatchMissionAction(state, { type: 'START_EVA' }, defaultConfig);
    expect(res.success).toBe(false);
    expect(res.error).toContain('crew health');
  });

});
