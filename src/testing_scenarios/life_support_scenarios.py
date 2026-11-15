"""Generates expected calculation fixtures for life-support mass balances & emergency cascades."""

import json
from pathlib import Path
from typing import Optional

from src.reference_models.life_support_model import (
    calculate_daily_crew_mass_balance,
    simulate_life_support_emergency_cascade
)


def generate_life_support_validation_fixtures(output_dir: Optional[Path] = None) -> Path:
    """Generate expected calculations fixture for life-support models."""
    if output_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "tests" / "fixtures"
    output_dir.mkdir(parents=True, exist_ok=True)

    nominal_balance = calculate_daily_crew_mass_balance(crew_size=4)
    cascade_water_fail = simulate_life_support_emergency_cascade(
        "scenario_2_water_failure",
        crew_size=4,
        water_recycler_efficiency=0.93  # Pre-BPA historical fallback rate
    )
    cascade_power_fail = simulate_life_support_emergency_cascade(
        "scenario_1_power_loss",
        crew_size=4,
        co2_scrubber_powered=False,
        electrolysis_powered=False
    )

    fixture_data = {
        "benchmark_crew_size_4": nominal_balance,
        "scenarios": {
            "scenario_1_solar_power_loss": {
                "description": "CO2 scrubbers and electrolysis unpowered; CO2 accumulates, O2 reserves deplete",
                "final_stored_o2_kg": cascade_power_fail["final_stored_o2_kg"],
                "final_cabin_co2_kg": cascade_power_fail["final_cabin_co2_kg"],
                "cascade_triggered": cascade_power_fail["cascade_triggered"]
            },
            "scenario_2_water_recycling_failure": {
                "description": "Recycling efficiency degrades to 93% pre-BPA rate",
                "final_stored_water_kg": cascade_water_fail["final_stored_water_kg"],
                "cascade_triggered": cascade_water_fail["cascade_triggered"]
            }
        }
    }

    out_file = output_dir / "expected_life_support_calculations.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(fixture_data, f, indent=2)

    return out_file


if __name__ == "__main__":
    path = generate_life_support_validation_fixtures()
    print("Generated life support validation fixtures at:", path)

