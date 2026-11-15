"""Mapping module to adapt DONKI space weather events into Simulation Emergency Scenarios.

Produces scenario definitions for Box C (Configuration Layer) and Box E (Event & Emergency Manager).
"""

from typing import Any, Dict, List
import pandas as pd


def map_sep_events_to_scenarios(
    sep_df: pd.DataFrame,
    default_shelter_protection_factor: float = 0.90
) -> List[Dict[str, Any]]:
    """Map cleaned SEP DataFrame records to simulation emergency scenarios."""
    scenarios = []

    for _, row in sep_df.iterrows():
        flare_cls = row.get("associated_flare_class") or "M5.0"
        noaa_scale = row.get("noaa_scale") or "S2"
        flux = float(row.get("estimated_flux_pfu") or 100.0)
        lead_time = float(row.get("warning_lead_time_minutes") or 30.0)
        # Ensure lead time is realistic for gameplay (minimum 15 mins if 0 lead time recorded)
        gameplay_lead_time = max(15.0, lead_time)

        # Realistic duration based on NOAA scale
        duration_map = {
            "S1": 12.0,
            "S2": 18.0,
            "S3": 24.0,
            "S4": 36.0,
            "S5": 48.0,
        }
        duration_hrs = duration_map.get(noaa_scale, 24.0)

        scenario = {
            "scenario_id": f"scenario_spe_{row['message_id']}",
            "title": f"Solar Particle Event ({noaa_scale} - {flare_cls} Flare)",
            "hazard_type": "solar_particle_event",
            "noaa_scale": noaa_scale,
            "associated_flare_class": flare_cls,
            "warning_lead_time_minutes": gameplay_lead_time,
            "peak_flux_pfu": flux,
            "duration_hours": duration_hrs,
            "recommended_action": "seek_radiation_shelter",
            "shelter_protection_factor": default_shelter_protection_factor,
            "affected_systems": [
                "crew_safety",
                "crop_lighting",
                "eva_readiness",
                "radiation_monitoring"
            ],
            "provenance": {
                "source": row.get("source", "NASA CCMC DONKI"),
                "activity_id": row.get("event_id"),
                "classification": row.get("classification", "research reference"),
                "origin_type": row.get("origin_type", "measured"),
                "v1_safe": bool(row.get("v1_safe", True)),
                "caveats": row.get("caveats", "Extrapolated from NASA space weather telemetry")
            }
        }
        scenarios.append(scenario)

    return scenarios


if __name__ == "__main__":
    from src.ingestion.ingest_donki import fetch_donki_notifications
    from src.processing.process_donki import parse_donki_notifications, clean_donki_events, filter_sep_scenarios

    data = fetch_donki_notifications()
    parsed = parse_donki_notifications(data)
    cleaned = clean_donki_events(parsed)
    sep_events = filter_sep_scenarios(cleaned)
    scenarios = map_sep_events_to_scenarios(sep_events)

    print(f"Mapped {len(scenarios)} emergency scenarios from DONKI SEP events.")
    if scenarios:
        print("\nPrimary Scenario Preview:")
        print(scenarios[0])

