"""End-to-end integration tests for the full Python Data & Science Layer pipeline (Schema 1.1)."""

import json
from pathlib import Path
import pytest
import jsonschema

from main import run_pipeline


def test_full_pipeline_execution():
    config_path = run_pipeline(crew_size=4)
    assert config_path.exists()

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 1. Structure verification (Schema 1.1)
    assert config["schema_version"] == "1.1"
    assert config["mission"]["crew_size"] == 4
    assert "parameters" in config
    assert isinstance(config["parameters"], list)
    assert len(config["parameters"]) >= 30

    # Index parameters by parameter_id
    params_by_id = {p["parameter_id"]: p for p in config["parameters"]}

    # 2. Check life-support research parameters from simulation-parameter-sheet.md
    assert "daily_o2_requirement_per_astronaut" in params_by_id
    o2_p = params_by_id["daily_o2_requirement_per_astronaut"]
    assert o2_p["resource"] == "oxygen"
    assert o2_p["flow_type"] == "consumption"
    assert o2_p["value_per_person"] == 0.89
    assert o2_p["data_status"] == "research_reference"

    assert "daily_co2_production_per_astronaut" in params_by_id
    co2_p = params_by_id["daily_co2_production_per_astronaut"]
    assert co2_p["resource"] == "co2"
    assert co2_p["value_per_person"] == 1.08

    assert "daily_water_requirement_per_astronaut" in params_by_id
    water_p = params_by_id["daily_water_requirement_per_astronaut"]
    assert water_p["resource"] == "water"
    assert water_p["value_per_person"] == 5.03

    assert "packaged_food_per_astronaut" in params_by_id
    food_p = params_by_id["packaged_food_per_astronaut"]
    assert food_p["resource"] == "food"
    assert food_p["value_per_person"] == 2.39

    # 3. Check NASA API integrated parameters
    assert "lunar_surface_gcr_dose_equivalent" in params_by_id
    rad_p = params_by_id["lunar_surface_gcr_dose_equivalent"]
    assert rad_p["resource"] == "radiation"
    assert rad_p["value_per_person"] == 1.37

    assert "spe_solar_particle_warning_time" in params_by_id
    spe_p = params_by_id["spe_solar_particle_warning_time"]
    assert spe_p["resource"] == "radiation"
    assert spe_p["value_per_person"] >= 15.0

    assert "crop_growth_time_lettuce_veg03a" in params_by_id
    crop_p = params_by_id["crop_growth_time_lettuce_veg03a"]
    assert crop_p["resource"] == "food"
    assert crop_p["value_per_person"] == 33.0

    # 4. JSON Schema Validation against mission_config_schema.json
    project_root = Path(__file__).resolve().parents[1]
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
