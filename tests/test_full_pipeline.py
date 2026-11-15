"""End-to-end integration tests for the full Python Data & Science Layer pipeline (Schema 1.1).

These tests verify that:
1. The pipeline runs end-to-end without error.
2. The generated mission_config.json conforms to the TypeScript SimulationParameter contract.
3. Required scientific parameters are present with correct values.
4. The Python-side JSON Schema accepts the generated configuration.
"""

import json
import math
from pathlib import Path
import pytest
import jsonschema

from main import run_pipeline


def test_full_pipeline_execution():
    config_path = run_pipeline(crew_size=4)
    assert config_path.exists()

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 1. Top-level structure (Schema 1.1)
    assert config["schema_version"] == "1.1"
    assert config["mission"]["crew_size"] == 4
    assert "parameters" in config
    assert isinstance(config["parameters"], list)
    assert len(config["parameters"]) == 28

    # Index parameters by parameter_id
    params_by_id = {p["parameter_id"]: p for p in config["parameters"]}

    # 2. Required TypeScript contract fields present on every parameter
    required_ts_fields = {
        "parameter_id", "flow_type",
        "value", "basis", "unit",
        "classification", "data_status", "source",
        "assumptions", "caveats"
    }
    valid_flow_types = {
        "consumption", "production", "generation",
        "removal", "recovery", "loss", "capacity", "requirement"
    }
    valid_bases = {
        "per_person", "per_equipment", "per_cycle", "per_time", "total"
    }
    valid_classifications = {"research_data", "engineering_inference", "gameplay_assumption"}
    valid_data_statuses = {"validated", "pending_review", "mock", "TBD"}

    for p in config["parameters"]:
        pid = p.get("parameter_id", "<unknown>")
        # All required fields present
        for field in required_ts_fields:
            assert field in p, f"Parameter '{pid}' missing required field '{field}'"

        # flow_type enum
        assert p["flow_type"] in valid_flow_types, (
            f"Parameter '{pid}' has invalid flow_type '{p['flow_type']}'"
        )

        # basis enum
        assert p["basis"] in valid_bases, (
            f"Parameter '{pid}' has invalid basis '{p['basis']}'"
        )

        # classification enum
        assert p["classification"] in valid_classifications, (
            f"Parameter '{pid}' has invalid classification '{p['classification']}'"
        )

        # data_status enum
        assert p["data_status"] in valid_data_statuses, (
            f"Parameter '{pid}' has invalid data_status '{p['data_status']}'"
        )

        # value must be a finite, non-negative number; no null, NaN, or Infinity
        v = p["value"]
        assert isinstance(v, (int, float)) and not isinstance(v, bool), (
            f"Parameter '{pid}' value is not a number: {v!r}"
        )
        assert not math.isnan(v), f"Parameter '{pid}' value is NaN"
        assert not math.isinf(v), f"Parameter '{pid}' value is Infinity"
        assert v >= 0, f"Parameter '{pid}' value is negative: {v}"

        # source must be a dict with 'title' or null
        src = p["source"]
        assert src is None or isinstance(src, dict), (
            f"Parameter '{pid}' source must be dict or null, got {type(src)}"
        )
        if isinstance(src, dict):
            assert "title" in src and src["title"], (
                f"Parameter '{pid}' source dict missing 'title'"
            )

        # assumptions and caveats must be lists
        assert isinstance(p["assumptions"], list), f"Parameter '{pid}' assumptions must be list"
        assert isinstance(p["caveats"], list), f"Parameter '{pid}' caveats must be list"

        # period: if basis is per_time, period is mandatory with value and unit
        if p["basis"] == "per_time":
            assert "period" in p and p["period"] is not None, (
                f"Parameter '{pid}' with basis 'per_time' missing period"
            )
            assert isinstance(p["period"], dict), f"Parameter '{pid}' period must be dict"
            assert "value" in p["period"] and "unit" in p["period"], (
                f"Parameter '{pid}' period missing value or unit"
            )
            assert p["period"]["unit"] in {"hour", "day", "cycle"}
            assert p["period"]["value"] > 0
        elif "period" in p and p["period"] is not None:
            assert isinstance(p["period"], dict), f"Parameter '{pid}' period must be dict"
            assert "value" in p["period"] and "unit" in p["period"]
            assert p["period"]["value"] > 0

    # 3. Life-support research parameters from simulation-parameter-sheet.md
    assert "daily_o2_requirement_per_astronaut" in params_by_id
    o2_p = params_by_id["daily_o2_requirement_per_astronaut"]
    assert o2_p["resource"] == "oxygen"
    # "requirement" is correct: this is a planned daily requirement, not a real-time consumption rate
    assert o2_p["flow_type"] in {"consumption", "requirement"}
    assert o2_p["value"] == 0.89
    assert o2_p["classification"] in valid_classifications
    assert o2_p["data_status"] in valid_data_statuses

    assert "daily_co2_production_per_astronaut" in params_by_id
    co2_p = params_by_id["daily_co2_production_per_astronaut"]
    assert co2_p["resource"] == "co2"
    assert co2_p["value"] == 1.08

    assert "daily_water_requirement_per_astronaut" in params_by_id
    water_p = params_by_id["daily_water_requirement_per_astronaut"]
    assert water_p["resource"] == "water"
    assert water_p["value"] == 5.03

    assert "packaged_food_per_astronaut" in params_by_id
    food_p = params_by_id["packaged_food_per_astronaut"]
    assert food_p["resource"] == "food"
    assert food_p["value"] == 2.39

    # 4. Canonical simulation aliases and critical systems
    assert "overall_iss_water_recovery_milestone" in params_by_id
    rec_p = params_by_id["overall_iss_water_recovery_milestone"]
    assert rec_p["resource"] == "water"
    assert rec_p["flow_type"] == "recovery"
    assert rec_p["value"] == 98.0
    assert rec_p["unit"] == "percent"

    assert "fission_surface_power_target" in params_by_id
    fsp_p = params_by_id["fission_surface_power_target"]
    assert fsp_p["resource"] == "power"
    assert fsp_p["flow_type"] == "generation"
    assert fsp_p["value"] == 40.0
    assert fsp_p["unit"] == "kW"

    # Canonical simulation aliases
    assert "crew_oxygen_consumption" in params_by_id
    assert params_by_id["crew_oxygen_consumption"]["value"] == 0.89
    assert "crew_co2_production" in params_by_id
    assert params_by_id["crew_co2_production"]["value"] == 1.08
    assert "crew_water_requirement" in params_by_id
    assert params_by_id["crew_water_requirement"]["value"] == 5.03
    assert "crew_food_energy" in params_by_id
    assert params_by_id["crew_food_energy"]["value"] == 3000.0
    assert "crew_food_mass" in params_by_id
    assert params_by_id["crew_food_mass"]["value"] == 2.39

    # Unresolved / unsupported unit parameters must NOT be emitted in mission_config.json
    assert "lunar_surface_gcr_dose_equivalent" not in params_by_id
    assert "spe_solar_particle_warning_time" not in params_by_id
    assert "crop_growth_time_lettuce_veg03a" not in params_by_id

    # Emergency scenarios file must be generated with 16 scenarios
    project_root = Path(__file__).resolve().parents[1]
    scenarios_path = project_root / "outputs" / "emergency_scenarios.json"
    assert scenarios_path.exists()
    with open(scenarios_path, "r", encoding="utf-8") as f:
        scenarios_data = json.load(f)
    assert "scenarios" in scenarios_data
    assert len(scenarios_data["scenarios"]) == 16

    # 5. JSON Schema validation against mission_config_schema.json
    schema_file = project_root / "schemas" / "mission_config_schema.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(instance=config, schema=schema)


def test_validation_fixtures_presence():
    project_root = Path(__file__).resolve().parents[1]
    fixtures_dir = project_root / "tests" / "fixtures"

    rad_fixture = fixtures_dir / "expected_radiation_calculations.json"
    assert rad_fixture.exists()
    with open(rad_fixture, "r", encoding="utf-8") as f:
        rad_data = json.load(f)
    assert len(rad_data) > 0

    ls_fixture = fixtures_dir / "expected_life_support_calculations.json"
    assert ls_fixture.exists()
    with open(ls_fixture, "r", encoding="utf-8") as f:
        ls_data = json.load(f)
    assert "benchmark_crew_size_4" in ls_data
