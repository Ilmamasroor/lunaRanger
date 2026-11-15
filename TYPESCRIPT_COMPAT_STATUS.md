# TypeScript Runtime Compatibility Status

**Status: PENDING TYPESCRIPT RUNTIME VERIFICATION**

---

## What This Document Tracks

The Python science pipeline generates `outputs/mission_config.json` for the TypeScript simulation engine. This document tracks whether the generated configuration has been accepted by the actual TypeScript runtime validator and loaded by the TypeScript configuration loader.

---

## Current State

| Check | Status | Notes |
|---|---|---|
| Python-side JSON Schema validation | ✅ Pass | `schemas/mission_config_schema.json` enforces contract structure |
| Python contract field tests | ✅ Pass | `tests/test_ts_compatibility.py` — 35 tests, all pass |
| Generated `mission_config.json` matches documented contract | ✅ Pass | 28 parameters, all fields and units verified |
| TypeScript source code available | ❌ Not available | TS engine not provided to Python team |
| TypeScript `SimulationParameter` interface confirmed | ⏳ Pending | Awaiting TypeScript developer confirmation |
| TypeScript runtime validator executed against config | ⏳ Pending | No validator CLI available |
| TypeScript configuration loader executed | ⏳ Pending | No loader available |

---

## Documented Contract

The Python pipeline implements the following `SimulationParameter` structure, documented in `README_FOR_TYPESCRIPT_DEV.md`:

```typescript
interface SimulationParameter {
  parameter_id: string;
  resource?: string;
  system?: string;
  equipment_id?: string;
  flow_type: "consumption" | "production" | "generation" | "removal" | "recovery" | "loss" | "capacity" | "requirement";
  value: number; // Finite non-negative number; null is never used in mission_config.json
  basis: "per_person" | "per_equipment" | "per_cycle" | "per_time" | "total";
  unit: string;  // Strictly from the 17-unit registry
  period?: { value: number; unit: "hour" | "day" | "cycle" | "minute" | "second" };
  classification: "research_data" | "engineering_inference" | "gameplay_assumption";
  data_status: "mock" | "pending_review" | "validated" | "TBD";
  source: { title: string; url: string | null; identifier: string | null; location: string | null } | null;
  assumptions: string[];
  caveats: string[];
}
```

This contract was derived from the PR review comments describing the TypeScript `SimulationParameter` interface and runtime validator. It has **not been confirmed against the actual TypeScript source**.

This contract was derived from the PR review comments describing the TypeScript `SimulationParameter` interface and runtime validator. It has **not been confirmed against the actual TypeScript source**.

> **Legacy fields** (`value_per_person`, `raw_value`, `notes`) may appear in the generated JSON as optional backward-compatibility fields. The Python-side schema permits them via `additionalProperties: true`. The TypeScript developer should confirm whether these fields interfere with their parser.

---

## What the Python-Side Tests Cover

`tests/test_ts_compatibility.py` enforces:

- All required fields are present on every parameter
- `flow_type` only uses contract enum values (no `"environment"`, `"infrastructure"`, `"storage"`, `"specification"`)
- `classification` only uses `research_data` / `engineering_inference` / `gameplay_assumption`
- `data_status` only uses `validated` / `pending_review` / `mock` / `TBD` (no `"research_reference"`, `"derived"`, `"tbd"`)
- `source` is a structured object `{title, url, identifier, location}` or `null` — never a plain string
- `value` is a number or `null` — never NaN, Infinity, or a string
- `assumptions` and `caveats` are lists of strings — never silently dropped
- Scientifically meaningful caveats are present on radiation parameters
- NASA-measured values are not classified as `gameplay_assumption`
- No negative values for resources that cannot be negative (oxygen, water, food, power)
- Null values carry `data_status: "TBD"` or `"pending_review"`
- Known parameters have traceable structured sources

## What These Tests Cannot Cover

- Whether the TypeScript runtime parser accepts the JSON without error
- Whether the TypeScript `SimulationParameter` interface uses these exact property names
- Whether the TypeScript validator applies additional constraints (branded types, runtime parsers, discriminated unions)
- Whether the TypeScript configuration loader maps `basis`, `caveats`, or `classification` to its own internal types

---

## Required Actions Before Claiming Full Compatibility

1. **TypeScript developer must review `README_FOR_TYPESCRIPT_DEV.md`** and confirm or correct:
   - The `SimulationParameter` field names match their actual interface
   - The enum values for `flow_type`, `classification`, `data_status`, `basis`, `resource` are correct
   - The `source` object structure `{title, url, identifier, location}` is what their loader expects
   - The `period.unit` enum (`"minute"`, `"hour"`, `"day"`, `"year"`) is complete

2. **TypeScript developer must run the generated `mission_config.json` through their validator** and report any rejection errors.

3. **On confirmation or correction**, update:
   - `schemas/mission_config_schema.json` (adjust any mismatched enums)
   - `src/processing/process_research_parameters.py` (adjust any field mappings)
   - `src/mapping/dataset_adapter.py` (adjust any field mappings)
   - `tests/test_ts_compatibility.py` (add live `ts-node` integration test)
   - This file (mark checks as ✅)

---

## How to Add a Live TypeScript Integration Test

Once the TypeScript validator CLI entrypoint is known:

```python
# In tests/test_ts_compatibility.py:
def test_typescript_runtime_validation():
    """Live integration test against the actual TypeScript runtime validator."""
    import subprocess
    from pathlib import Path
    result = subprocess.run(
        ["npx", "ts-node", "src/validateConfig.ts",
         "../../outputs/mission_config.json"],
        cwd=Path(__file__).resolve().parents[1] / "lunaRanger",
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, (
        f"TypeScript validator rejected config:\n{result.stdout}\n{result.stderr}"
    )
```

The exact CLI command and working directory must be confirmed with the TypeScript developer.

---

## Contact

> To complete this verification, the TypeScript developer should review the
> contract in `README_FOR_TYPESCRIPT_DEV.md` and either confirm it matches their
> `SimulationParameter` interface, or provide the corrections needed.
