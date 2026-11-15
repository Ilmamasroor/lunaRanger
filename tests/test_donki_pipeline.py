"""Unit and integration tests for the NASA DONKI pipeline & reference model."""

import json
from pathlib import Path
import pytest
import pandas as pd

from src.ingestion.ingest_donki import fetch_donki_notifications
from src.processing.process_donki import (
    parse_donki_notifications,
    clean_donki_events,
    filter_sep_scenarios
)
from src.validation.validate_donki import validate_donki_dataframe
from src.mapping.map_donki_events import map_sep_events_to_scenarios
from src.reference_models.radiation_model import (
    simulate_reference_radiation_profile,
    calculate_spe_dose_rate_usv_hr
)
from src.testing_scenarios.generate_test_cases import generate_radiation_validation_fixtures


def test_donki_ingestion():
    notifications = fetch_donki_notifications()
    assert isinstance(notifications, list)
    assert len(notifications) > 0
    sample = notifications[0]
    assert "messageType" in sample
    assert "messageBody" in sample


def test_donki_pandas_processing():
    raw_data = fetch_donki_notifications()
    df = parse_donki_notifications(raw_data)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "message_type" in df.columns
    assert "source" in df.columns
    assert (df["source"] == "NASA CCMC DONKI (api.nasa.gov/DONKI)").all()

    cleaned = clean_donki_events(df)
    assert not cleaned.empty

    seps = filter_sep_scenarios(cleaned)
    assert not seps.empty
    assert (seps["message_type"] == "SEP").all()
    assert (seps["warning_lead_time_minutes"] >= 0).all()


def test_donki_validation():
    raw_data = fetch_donki_notifications()
    df = clean_donki_events(parse_donki_notifications(raw_data))
    errors = validate_donki_dataframe(df)
    assert len(errors) == 0


def test_donki_mapping_to_scenarios():
    raw_data = fetch_donki_notifications()
    df = clean_donki_events(parse_donki_notifications(raw_data))
    seps = filter_sep_scenarios(df)
    scenarios = map_sep_events_to_scenarios(seps)

    assert len(scenarios) > 0
    sample = scenarios[0]
    assert sample["hazard_type"] == "solar_particle_event"
    assert sample["shelter_protection_factor"] == 0.90
    assert "provenance" in sample
    assert sample["provenance"]["classification"] == "research reference"


def test_radiation_reference_model():
    sample_scenario = {
        "scenario_id": "test_spe_s3",
        "noaa_scale": "S3",
        "peak_flux_pfu": 1000.0,
        "duration_hours": 24.0,
        "shelter_protection_factor": 0.90
    }

    res_shelter = simulate_reference_radiation_profile(sample_scenario, decision="shelter_immediate")
    res_delayed = simulate_reference_radiation_profile(sample_scenario, decision="shelter_delayed", delay_minutes=60.0)
    res_none = simulate_reference_radiation_profile(sample_scenario, decision="no_shelter")

    # Verify physical sanity: sheltering immediate gives lowest exposure, none gives highest
    assert res_shelter["total_cumulative_dose_usv"] < res_delayed["total_cumulative_dose_usv"]
    assert res_delayed["total_cumulative_dose_usv"] < res_none["total_cumulative_dose_usv"]
    assert len(res_shelter["hourly_timeline"]) == 24


def test_generate_validation_fixtures(tmp_path):
    raw_data = fetch_donki_notifications()
    df = clean_donki_events(parse_donki_notifications(raw_data))
    seps = filter_sep_scenarios(df)

    fixture_file = generate_radiation_validation_fixtures(seps, output_dir=tmp_path)
    assert fixture_file.exists()

    with open(fixture_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) > 0
    assert "expected_calculations" in data[0]

