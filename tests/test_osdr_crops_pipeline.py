"""Unit and reference model tests for the NASA OSDR Bio (OSD-269) crops pipeline."""

import pytest
import pandas as pd

from src.ingestion.ingest_osdr_bio import fetch_osd_study_metadata, fetch_osd_study_files
from src.processing.process_osdr_crops import (
    build_crop_parameters_dataframe,
    calculate_crew_crop_demands
)
from src.validation.validate_osdr_crops import validate_crop_dataframe
from src.reference_models.crop_growth_model import simulate_crop_lifecycle


def test_osdr_bio_ingestion():
    meta = fetch_osd_study_metadata(269)
    assert isinstance(meta, dict)
    assert "study" in meta
    studies = meta["study"]["OSD-269"]["studies"]
    assert len(studies) > 0
    assert "VEG03A" in studies[0]["title"] or "lettuce" in studies[0]["title"].lower()

    files = fetch_osd_study_files(269)
    assert isinstance(files, dict)
    study_files = files.get("studies", {}).get("OSD-269", {}).get("study_files", [])
    assert len(study_files) > 0


def test_crop_dataframe_building_and_demands():
    meta = fetch_osd_study_metadata(269)
    df = build_crop_parameters_dataframe(meta)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    assert "lettuce_veg03a" in df["crop_id"].values

    # Test demands calculation for 4 astronauts with 20 m2 crop area
    demands = calculate_crew_crop_demands(df, crew_size=4, allocated_crop_area_m2=20.0)
    lettuce_row = demands[demands["crop_id"] == "lettuce_veg03a"].iloc[0]
    # 2.0 L/m2/d * 20 m2 = 40.0 kg/day
    assert lettuce_row["daily_water_demand_kg"] == 40.0
    assert lettuce_row["full_diet_area_m2_4crew"] == 180.0


def test_crop_validation():
    meta = fetch_osd_study_metadata(269)
    df = build_crop_parameters_dataframe(meta)
    errors = validate_crop_dataframe(df)
    assert len(errors) == 0


def test_crop_reference_model_nominal_vs_failures():
    sample_lettuce = {
        "crop_id": "lettuce_veg03a",
        "first_harvest_days": 33,
        "water_use_rate_l_m2_d": 2.0
    }

    # Nominal: achieves ~90.9% progress by day 30
    nom = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=30)
    assert nom["final_status"] == "growing"
    assert nom["daily_timeline"][-1]["growth_progress_pct"] > 85.0

    # Extended nominal (35 days) should be ready for harvest
    harvest_run = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=35)
    assert harvest_run["final_status"] == "ready_for_harvest"
    assert harvest_run["harvests_achieved"] >= 1

    # Water stress (Scenario 2 cascade)
    stress = simulate_crop_lifecycle(sample_lettuce, allocated_area_m2=10.0, mission_days=30, water_ration_factor=0.3)
    assert stress["final_status"] == "failed_water_stress"

    # Prolonged lighting failure (Scenario 1 cascade: 4 consecutive days without light)
    outage = simulate_crop_lifecycle(
        sample_lettuce,
        allocated_area_m2=10.0,
        mission_days=30,
        lighting_failure_day=10,
        lighting_outage_duration_days=4
    )
    assert outage["final_status"] == "failed_lighting_loss"

