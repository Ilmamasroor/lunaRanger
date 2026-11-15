export type HealthStatus = 'NOMINAL' | 'CAUTION' | 'CRITICAL';
export type EquipmentStatus = 'OPERATIONAL' | 'DEGRADED' | 'OFFLINE';
export type EvaStatus = 'STANDBY' | 'CLEARED' | 'IN_PROGRESS' | 'COMPLETED' | 'ABORTED';

export interface ResourcePool {
  oxygen: number;
  carbonDioxide: number;
  water: number;
  food: number;
  energy: number;
}

export interface CrewStatus {
  activeCrewSize: number;
  healthStatus: HealthStatus;
  sheltered: boolean;
}

export interface EquipmentItem {
  id: string;
  name: string;
  status: EquipmentStatus;
  damageLevel: number; // 0.0 to 1.0
  diagnosed: boolean;
}

export interface EvaState {
  status: EvaStatus;
  cleared: boolean;
  astronautId: string | null;
  targetDurationMinutes: number;
}

export interface SampleCollectionState {
  sampleId: string | null;
  containerId: string | null;
  collected: boolean;
  securedInHabitat: boolean;
}

export interface MissionObjective {
  id: string;
  day: number;
  description: string;
  completed: boolean;
}

export interface EnvironmentalHazards {
  solarRadiationAlertActive: boolean;
  micrometeoriteWarningActive: boolean;
}

export interface MissionConfig {
  oxygenConsumptionPerCrewPerCycle: number;
  co2GenerationPerCrewPerCycle: number;
  waterConsumptionPerCrewPerCycle: number;
  foodConsumptionPerCrewPerCycle: number;
  baseEnergyConsumptionPerCycle: number;
  solarGenerationPerCycle: number;
  co2ScrubberEfficiency: number;
  waterRecyclerEfficiency: number;
  minOxygenForEva: number;
  minEnergyForEva: number;
}

export interface MissionState {
  missionId: string;
  currentCycle: number;
  maxCycles: number;
  crewStatus: CrewStatus;
  resources: ResourcePool;
  equipment: EquipmentItem[];
  hazards: EnvironmentalHazards;
  evaState: EvaState;
  sampleCollectionState: SampleCollectionState;
  objectives: MissionObjective[];
  history: string[];
}

export type MissionActionType =
  | 'ADVANCE_CYCLE'
  | 'DIAGNOSE_EQUIPMENT'
  | 'REPAIR_EQUIPMENT'
  | 'TOGGLE_SHELTER'
  | 'REQUEST_EVA_CLEARANCE'
  | 'START_EVA'
  | 'COLLECT_LUNAR_SAMPLE'
  | 'COMPLETE_EVA_AND_RETURN'
  | 'ABORT_EVA'
  | 'VERIFY_FINAL_MISSION_STATUS';

export interface MissionAction {
  type: MissionActionType;
  payload?: Record<string, unknown>;
}

export interface DispatchResult {
  success: boolean;
  error: string | null;
  state: MissionState | null;
}
