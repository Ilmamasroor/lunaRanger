"""Configuration generator producing validated mission_config.json for the TypeScript Simulation Engine."""

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
import jsonschema

REGISTRY_UNITS = frozenset({
    "kg", "g", "L", "mL", "kcal", "Wh", "kWh", "W", "kW",
    "kg/day", "kg/cycle", "L/day", "Wh/cycle", "kWh/cycle",
    "kg/m3", "ppm", "percent"
})

RESOURCE_SUPPORTED_UNITS = {
    "oxygen": frozenset({"kg", "kg/day", "kg/cycle", "g", "percent", "ppm"}),
    "co2": frozenset({"kg", "kg/day", "kg/cycle", "g", "percent", "ppm"}),
    "water": frozenset({"kg", "kg/day", "kg/cycle", "L", "L/day", "g", "mL", "percent", "ppm"}),
    "food": frozenset({"kcal", "kg", "kg/day", "percent"}),
    "power": frozenset({"Wh", "Wh/cycle", "kWh", "kWh/cycle", "W", "kW", "percent"}),
}

VALID_FLOW_TYPES = frozenset({
    "consumption", "production", "generation",
    "removal", "recovery", "loss", "capacity", "requirement"
})

VALID_CLASSIFICATIONS = frozenset({
    "research_data", "engineering_inference", "gameplay_assumption"
})

VALID_DATA_STATUSES = frozenset({
    "mock", "pending_review", "validated", "TBD"
})

VALID_BASES = frozenset({
    "per_person", "per_equipment", "per_cycle", "per_time", "total"
})

PER_TIME_PERIOD_UNITS = frozenset({
    "hour", "day", "cycle"
})


def validate_mission_config_contract(config_data: Dict[str, Any]) -> List[str]:
    """Validate configuration against the documented TypeScript SimulationParameter contract.

    Returns a list of validation error messages (empty if valid).
    """
    errors: List[str] = []

    # 1. Root structure
    if config_data.get("schema_version") != "1.1":
        errors.append(f"schema_version must be '1.1', got: {config_data.get('schema_version')!r}")

    mission = config_data.get("mission")
    if not isinstance(mission, dict):
        errors.append("mission must be an object")
    else:
        crew_size = mission.get("crew_size")
        if not isinstance(crew_size, int) or crew_size < 1:
            errors.append(f"mission.crew_size must be a positive integer, got: {crew_size!r}")

    parameters = config_data.get("parameters")
    if not isinstance(parameters, list):
        errors.append("parameters must be an array")
        return errors

    if len(parameters) == 0:
        errors.append("parameters array must not be empty")

    seen_ids = set()

    for idx, p in enumerate(parameters):
        if not isinstance(p, dict):
            errors.append(f"Parameter [{idx}] must be an object")
            continue

        pid = p.get("parameter_id")
        if not isinstance(pid, str) or not pid.strip():
            errors.append(f"Parameter [{idx}] missing or empty parameter_id")
            continue

        if pid in seen_ids:
            errors.append(f"Duplicate parameter_id: '{pid}'")
        seen_ids.add(pid)

        # Value: finite, non-negative number
        val = p.get("value")
        if val is None:
            errors.append(f"Parameter '{pid}': value must be a number (got None/null). TBD null is not permitted.")
        elif not isinstance(val, (int, float)):
            errors.append(f"Parameter '{pid}': value must be numeric, got {type(val).__name__}")
        else:
            if not math.isfinite(val):
                errors.append(f"Parameter '{pid}': value must be finite (got NaN or Inf)")
            if val < 0:
                errors.append(f"Parameter '{pid}': value must be non-negative (got {val})")

        # Flow type
        ft = p.get("flow_type")
        if ft not in VALID_FLOW_TYPES:
            errors.append(f"Parameter '{pid}': invalid flow_type '{ft}'. Must be one of {sorted(VALID_FLOW_TYPES)}")

        # Unit
        u = p.get("unit")
        if u not in REGISTRY_UNITS:
            errors.append(f"Parameter '{pid}': unsupported unit '{u}'. Must be in TypeScript unit registry: {sorted(REGISTRY_UNITS)}")

        # Resource-specific unit compatibility
        res = p.get("resource")
        if res and res in RESOURCE_SUPPORTED_UNITS:
            allowed = RESOURCE_SUPPORTED_UNITS[res]
            if u not in allowed:
                errors.append(f"Parameter '{pid}': unit '{u}' is incompatible with resource '{res}'. Allowed: {sorted(allowed)}")

        # Basis
        basis = p.get("basis")
        if basis not in VALID_BASES:
            errors.append(f"Parameter '{pid}': invalid basis '{basis}'. Must be one of {sorted(VALID_BASES)}")

        # Period for per_time
        period = p.get("period")
        if basis == "per_time":
            if not isinstance(period, dict):
                errors.append(f"Parameter '{pid}': basis 'per_time' requires a 'period' object")
            else:
                p_unit = period.get("unit")
                if p_unit not in PER_TIME_PERIOD_UNITS:
                    errors.append(f"Parameter '{pid}': basis 'per_time' requires period.unit in {sorted(PER_TIME_PERIOD_UNITS)}, got '{p_unit}'")
                p_val = period.get("value")
                if not isinstance(p_val, (int, float)) or p_val <= 0:
                    errors.append(f"Parameter '{pid}': period.value must be positive, got {p_val!r}")

        # Classification
        cls_val = p.get("classification")
        if cls_val not in VALID_CLASSIFICATIONS:
            errors.append(f"Parameter '{pid}': invalid classification '{cls_val}'. Must be one of {sorted(VALID_CLASSIFICATIONS)}")

        # Data Status
        ds = p.get("data_status")
        if ds not in VALID_DATA_STATUSES:
            errors.append(f"Parameter '{pid}': invalid data_status '{ds}'. Must be one of {sorted(VALID_DATA_STATUSES)}")

        # Source
        src = p.get("source")
        if src is not None:
            if not isinstance(src, dict):
                errors.append(f"Parameter '{pid}': source must be an object or null, got {type(src).__name__}")
            else:
                title = src.get("title")
                if not isinstance(title, str) or not title.strip():
                    errors.append(f"Parameter '{pid}': non-null source must contain a non-empty 'title'")

        # Assumptions and Caveats
        if not isinstance(p.get("assumptions"), list):
            errors.append(f"Parameter '{pid}': assumptions must be an array of strings")
        if not isinstance(p.get("caveats"), list):
            errors.append(f"Parameter '{pid}': caveats must be an array of strings")

    return errors


def validate_and_save_mission_config(
    config_data: Dict[str, Any],
    schema_path: Optional[Path] = None,
    output_path: Optional[Path] = None
) -> Path:
    """Validate configuration dictionary against JSON schema and contract rules, then save to outputs/."""
    project_root = Path(__file__).resolve().parents[2]

    if schema_path is None:
        schema_path = project_root / "schemas" / "mission_config_schema.json"
    if output_path is None:
        output_path = project_root / "outputs" / "mission_config.json"

    # 1. Check schema file exists
    if not schema_path.exists():
        raise FileNotFoundError(f"Configuration schema not found at: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # 2. Validate using jsonschema
    jsonschema.validate(instance=config_data, schema=schema)

    # 3. Contract-specific validation (unique IDs, finite non-negative numbers, resource units, per_time periods)
    contract_errors = validate_mission_config_contract(config_data)
    if contract_errors:
        raise ValueError(f"Configuration contract validation failed ({len(contract_errors)} errors):\n" + "\n".join(f"- {e}" for e in contract_errors))

    # 4. Save validated configuration
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    return output_path
