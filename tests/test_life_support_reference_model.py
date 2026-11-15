"""Unit tests for the Life-Support stoichiometric reference model & scenarios."""

import json
from pathlib import Path
import pytest

from src.reference_models.life_support_model import (
    calculate_daily_crew_mass_balance,
    simulate_life_support_emergency_cascade,
    O2_CONSUMPTION_KG_PERSON_DAY,
    CO2_PRODUCTION_KG_PERSON_DAY,
    WATER_REQUIREMENT_KG_PERSON_DAY
)
from src.testing_scenarios.life_support_scenarios import generate_life_support_validation_fixtures


def test_crew_mass_balance_stoichiometry():
    bal = calculate_daily_crew_mass_balance(crew_size=4)
    # Check scaling against NASA 2019 reference values
    assert bal["daily_o2_demand_kg"] == 3.56
    assert bal["daily_co2_production_kg"] == 4.32
    assert bal["daily_water_requirement_kg"] == 20.12
    assert bal["daily_packaged_food_kg"] == 9.56
    # Theoretical electrolysis feed: ~4.01 kg/day
    assert abs(bal["daily_electrolysis_feed_min_kg"] - 4.01) < 0.05
    assert bal["mission_30d_o2_demand_kg"] == 106.8
    assert bal["mission_30d_co2_production_kg"] == 129.6


def test_scenario_1_unpowered_scrubbers_cascade():
    # Power failure halts CO2 scrubbers
    res = simulate_life_support_emergency_cascade(
        "power_failure",
        crew_size=4,
        mission_days=10,
        co2_scrubber_powered=False,
        electrolysis_powered=True
    )
    assert res["final_cabin_co2_kg"] > 40.0
    assert res["cascade_triggered"] == "air_quality_emergency_high_co2"


def test_scenario_2_degraded_water_recycling():
    # Pre-BPA historical rate (93%) vs nominal (98%)
    nom = simulate_life_support_emergency_cascade("nominal", water_recycler_efficiency=0.98, mission_days=10)
    deg = simulate_life_support_emergency_cascade("degraded", water_recycler_efficiency=0.93, mission_days=10)

    # Degraded recycling must lose more stored water than nominal
    assert deg["final_stored_water_kg"] < nom["final_stored_water_kg"]


def test_generate_life_support_fixtures(tmp_path):
    out_file = generate_life_support_validation_fixtures(output_dir=tmp_path)
    assert out_file.exists()
    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "benchmark_crew_size_4" in data
    assert data["benchmark_crew_size_4"]["daily_o2_demand_kg"] == 3.56

