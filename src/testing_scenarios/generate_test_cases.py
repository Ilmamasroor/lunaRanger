"""Generates validation test cases and expected calculation fixtures.

Corresponds to 'Validation Test Cases' in Diagram 1 and Box H in Diagram 2.
Produces expected calculation benchmarks that verify the TypeScript simulation engine.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd

from src.mapping.map_donki_events import map_sep_events_to_scenarios
from src.reference_models.radiation_model import simulate_reference_radiation_profile


def generate_radiation_validation_fixtures(
    sep_df: pd.DataFrame,
    output_dir: Optional[Path] = None
) -> Path:
    """Generate expected calculation test fixtures from DONKI SEP scenarios."""
    if output_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "tests" / "fixtures"
    output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = map_sep_events_to_scenarios(sep_df)
    test_cases = []

    for sc in scenarios[:5]:  # Generate benchmarks for top 5 scenarios
        sc_id = sc["scenario_id"]
        # Generate expected outcomes for all three commander decision branches
        out_immediate = simulate_reference_radiation_profile(sc, decision="shelter_immediate")
        out_delayed = simulate_reference_radiation_profile(sc, decision="shelter_delayed", delay_minutes=45.0)
        out_none = simulate_reference_radiation_profile(sc, decision="no_shelter")

        test_cases.append({
            "test_case_id": f"tc_radiation_{sc_id}",
            "scenario": sc,
            "expected_calculations": {
                "shelter_immediate": {
                    "total_dose_msv": out_immediate["total_cumulative_dose_msv"],
                    "total_dose_usv": out_immediate["total_cumulative_dose_usv"]
                },
                "shelter_delayed_45min": {
                    "total_dose_msv": out_delayed["total_cumulative_dose_msv"],
                    "total_dose_usv": out_delayed["total_cumulative_dose_usv"]
                },
                "no_shelter": {
                    "total_dose_msv": out_none["total_cumulative_dose_msv"],
                    "total_dose_usv": out_none["total_cumulative_dose_usv"]
                }
            }
        })

    fixture_path = output_dir / "expected_radiation_calculations.json"
    with open(fixture_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2)

    return fixture_path


if __name__ == "__main__":
    from src.ingestion.ingest_donki import fetch_donki_notifications
    from src.processing.process_donki import parse_donki_notifications, clean_donki_events, filter_sep_scenarios

    data = fetch_donki_notifications()
    parsed = parse_donki_notifications(data)
    cleaned = clean_donki_events(parsed)
    seps = filter_sep_scenarios(cleaned)

    path = generate_radiation_validation_fixtures(seps)
    print(f"Generated validation test fixtures at: {path}")

