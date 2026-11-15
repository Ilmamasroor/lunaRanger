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

function createBaseState(): MissionState {
  return {
    missionId: 'test-mission',
    currentCycle: 1,
    maxCycles: 7,
    crewStatus: { activeCrewSize: 4, healthStatus: 'NOMINAL', sheltered: false },
    resources: { oxygen: 100, carbonDioxide: 0.5, water: 100, food: 100, energy: 150 },
    equipment: [
      { id: 'heater-primary', name: 'Primary Heater', status: 'DEGRADED', damageLevel: 0.4, diagnosed: false },
      { id: 'solar-array', name: 'Solar Array', status: 'OPERATIONAL', damageLevel: 0, diagnosed: true },
      { id: 'water-recycler', name: 'Water Recycler', status: 'OPERATIONAL', damageLevel: 0, diagnosed: true },
      { id: 'co2-scrubber', name: 'CO2 Scrubber', status: 'OPERATIONAL', damageLevel: 0, diagnosed: true },
    ],
    hazards: { solarRadiationAlertActive: false, micrometeoriteWarningActive: false },
    evaState: { status: 'STANDBY', cleared: false, astronautId: null, targetDurationMinutes: 0 },
    sampleCollectionState: { sampleId: null, containerId: null, collected: false, securedInHabitat: false },
    objectives: [
      { id: 'day-1', day: 1, description: 'Restore heat', completed: false },
      { id: 'day-2', day: 2, description: 'Solar array', completed: true },
      { id: 'day-3', day: 3, description: 'Water recycler', completed: true },
      { id: 'day-4', day: 4, description: 'CO2 scrubber', completed: true },
      { id: 'day-5', day: 5, description: 'Solar shelter', completed: true },
      { id: 'day-6', day: 6, description: 'Sample collection', completed: false },
      { id: 'day-7', day: 7, description: 'Final check', completed: false },
    ],
    history: [],
  };
}

describe('Mission Cycle & Dispatcher Hardening', () => {
  it('rejects negative, fractional, NaN, and Infinity cycle increments without mutating state', () => {
    const initial = createBaseState();
    for (const invalid of [-1, 0, 1.5, NaN, Infinity]) {
      const res = dispatchMissionAction(
        initial,
        { type: 'ADVANCE_CYCLE', payload: { cyclesToAdvance: invalid } },
        defaultConfig
      );
      expect(res.success).toBe(false);
      expect(res.state).toBeNull();
      expect(initial.currentCycle).toBe(1);
    }
  });

  it('rejects null or malformed actions safely', () => {
    const initial = createBaseState();
    // @ts-expect-error testing malformed runtime input
    const res = dispatchMissionAction(initial, null, defaultConfig);
    expect(res.success).toBe(false);
    expect(res.error).toContain('Malformed action payload');
  });
  it('rejects skipping mission days even when the current objective is complete', () => {
    const state = createBaseState();
    state.objectives[0].completed = true;
    const res = dispatchMissionAction(
      state,
      { type: 'ADVANCE_CYCLE', payload: { cyclesToAdvance: 2 } },
      defaultConfig
    );
    expect(res.success).toBe(false);
    expect(res.error).toContain('exactly one day');
    expect(state.currentCycle).toBe(1);
  });

  it('does not allow repairing equipment before its assigned mission day', () => {
    const state = createBaseState();
    state.equipment[0].diagnosed = true;
    const res = dispatchMissionAction(
      state,
      { type: 'REPAIR_EQUIPMENT', payload: { equipmentId: 'solar-array' } },
      defaultConfig
    );
    expect(res.success).toBe(false);
    expect(res.error).toContain('Mission Day 2');
    expect(state.equipment[1].status).toBe('OPERATIONAL');
  });

  it('rejects invalid resource configuration before advancing', () => {
    const state = createBaseState();
    state.objectives[0].completed = true;
    const invalidConfig = { ...defaultConfig, waterRecyclerEfficiency: 1.5 };
    const res = dispatchMissionAction(state, { type: 'ADVANCE_CYCLE' }, invalidConfig);
    expect(res.success).toBe(false);
    expect(res.error).toContain('waterRecyclerEfficiency');
    expect(state.currentCycle).toBe(1);
  });

});
