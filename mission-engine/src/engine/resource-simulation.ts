import { MissionConfig, MissionState, ResourcePool } from './engine.types';

export function validateMissionConfig(config: MissionConfig): string | null {
  if (!config || typeof config !== 'object') return 'Mission config is required.';
  const nonNegativeFields: (keyof MissionConfig)[] = [
    'oxygenConsumptionPerCrewPerCycle',
    'co2GenerationPerCrewPerCycle',
    'waterConsumptionPerCrewPerCycle',
    'foodConsumptionPerCrewPerCycle',
    'baseEnergyConsumptionPerCycle',
    'solarGenerationPerCycle',
    'minOxygenForEva',
    'minEnergyForEva',
  ];
  for (const field of nonNegativeFields) {
    const value = config[field];
    if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
      return `Invalid mission config: ${field} must be a finite non-negative number.`;
    }
  }
  for (const field of ['co2ScrubberEfficiency', 'waterRecyclerEfficiency'] as const) {
    const value = config[field];
    if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > 1) {
      return `Invalid mission config: ${field} must be between 0 and 1.`;
    }
  }
  return null;
}

export function validateMissionResources(state: MissionState): string | null {
  if (!state || typeof state !== 'object' || !state.resources || !state.crewStatus) {
    return 'Invalid mission state: resources and crew status are required.';
  }
  if (!Number.isSafeInteger(state.crewStatus.activeCrewSize) || state.crewStatus.activeCrewSize < 1) {
    return 'Invalid mission state: activeCrewSize must be a positive integer.';
  }
  for (const [resource, value] of Object.entries(state.resources)) {
    if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
      return `Invalid mission state: ${resource} must be a finite non-negative number.`;
    }
  }
  return null;
}

export function cloneMissionState(state: MissionState): MissionState {
  return structuredClone(state);
}

export function simulateCycleResources(
  state: MissionState,
  config: MissionConfig
): ResourcePool {
  const crewCount = Math.max(0, state.crewStatus.activeCrewSize);

  const heater = state.equipment.find((e) => e.id === 'heater-primary');
  const solar = state.equipment.find((e) => e.id === 'solar-array');
  const waterRecycler = state.equipment.find((e) => e.id === 'water-recycler');
  const co2Scrubber = state.equipment.find((e) => e.id === 'co2-scrubber');

  const solarMultiplier =
    solar?.status === 'OPERATIONAL' ? 1.0 : solar?.status === 'DEGRADED' ? 0.5 : 0.0;
  const scrubberMultiplier =
    co2Scrubber?.status === 'OPERATIONAL'
      ? 1.0
      : co2Scrubber?.status === 'DEGRADED'
      ? 0.4
      : 0.0;
  const recyclerMultiplier =
    waterRecycler?.status === 'OPERATIONAL'
      ? 1.0
      : waterRecycler?.status === 'DEGRADED'
      ? 0.5
      : 0.0;
  const heaterEnergyDraw = heater?.status === 'OFFLINE' ? 0 : 12;

  const oxygenDelta = -(crewCount * config.oxygenConsumptionPerCrewPerCycle);
  const rawCo2Generated = crewCount * config.co2GenerationPerCrewPerCycle;
  const co2Removed = rawCo2Generated * config.co2ScrubberEfficiency * scrubberMultiplier;
  const co2Delta = rawCo2Generated - co2Removed;

  const grossWaterUsed = crewCount * config.waterConsumptionPerCrewPerCycle;
  const waterRecovered = grossWaterUsed * config.waterRecyclerEfficiency * recyclerMultiplier;
  const waterDelta = -(grossWaterUsed - waterRecovered);

  const foodDelta = -(crewCount * config.foodConsumptionPerCrewPerCycle);

  const energyGenerated = config.solarGenerationPerCycle * solarMultiplier;
  const energyUsed = config.baseEnergyConsumptionPerCycle + heaterEnergyDraw;
  const energyDelta = energyGenerated - energyUsed;

  return {
    oxygen: Math.max(0, Number((state.resources.oxygen + oxygenDelta).toFixed(4))),
    carbonDioxide: Math.max(0, Number((state.resources.carbonDioxide + co2Delta).toFixed(4))),
    water: Math.max(0, Number((state.resources.water + waterDelta).toFixed(4))),
    food: Math.max(0, Number((state.resources.food + foodDelta).toFixed(4))),
    energy: Math.max(0, Number((state.resources.energy + energyDelta).toFixed(4))),
  };
}
