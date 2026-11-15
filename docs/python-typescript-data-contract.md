# Python → TypeScript Data Contract v0.1

**Source:** Notion — [Python → TypeScript Data Contract v0.1](https://app.notion.com/p/4189fd4012aa81e182dff3d2240f922c)  
**Notion status:** Draft · Last reviewed 14 November 2026

> The contract describes the TypeScript configuration structures reported in the source page. The actual configuration loader and a real Python-generated fixture were not verified in that review. Reconcile this mirror against the current source before treating it as a release contract.

## Responsibility boundary

Python prepares data and provenance-aware parameter records. TypeScript validates configuration and owns live simulation state and resource calculations. Python does not run the live gameplay loop or mutate runtime inventories.

## Configuration shape

The documented root configuration uses:
- `schema_version` equal to `"1.1"`;
- `mission.crew_size` as a positive integer;
- a `parameters` array.

Each `SimulationParameter` includes `parameter_id`, `flow_type`, `value`, `unit`, `basis`, `classification`, `data_status`, `source`, `assumptions` and `caveats`. Optional fields include `resource`, `system`, `equipment_id` and `period`.

## Enumerations documented by the contract

**Flow types:** `consumption`, `production`, `generation`, `removal`, `recovery`, `loss`, `capacity`, `requirement`.

**Classifications:** `research_data`, `engineering_inference`, `gameplay_assumption`.

**Data statuses:** `mock`, `pending_review`, `validated`, `TBD`.

**Basis:** `per_person`, `per_equipment`, `per_cycle`, `per_time`, `total`.

For `per_time`, the documented runtime validator/simulator support is limited to `hour`, `day` and `cycle`; do not assume second/minute calculation support merely because a type declaration mentions them.

## Important unit caveat

The source distinguishes the structural unit registry from resource-specific conversion support. A unit accepted by configuration validation is not necessarily executable for every resource. Python must emit units compatible with the target resource's simulator conversions.

## Resource keys

- Oxygen: `oxygenKg`
- Carbon dioxide: `carbonDioxideKg`
- Water: `waterKg`
- Food: `foodKcal`
- Energy: `energyWh`

## Validation versus scientific approval

Structural acceptance does not establish scientific validity. The source page notes that mock parameters may pass scenario-readiness checks, while pending-review and TBD parameters block readiness. Keep assumptions and caveats with every parameter and do not promote a mock value to validated research data.

## Integration checklist

- [ ] Verify schema version and field names against current TypeScript source.
- [ ] Verify the configuration loader accepts the generated file.
- [ ] Add a real Python-generated fixture.
- [ ] Test units against resource-specific simulator conversions.
- [ ] Test missing, duplicate, TBD and pending-review parameters.
- [ ] Confirm equipment-linked flow behavior is implemented and regression-tested before relying on it.
