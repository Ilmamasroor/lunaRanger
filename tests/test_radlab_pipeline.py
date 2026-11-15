"""Unit tests for the NASA OSDR RadLab radiation telemetry pipeline."""

import pytest
import pandas as pd

from src.ingestion.ingest_radlab import fetch_radlab_telemetry
from src.processing.process_radiation import (
    process_radlab_telemetry,
    save_processed_radiation_parameters
)
from src.validation.validate_radiation import validate_radiation_dataframe


def test_radlab_ingestion():
    records = fetch_radlab_telemetry()
    assert isinstance(records, list)
    assert len(records) > 0
    rec = records[0]
    assert rec["celestial_body"] == "Moon"
    assert rec["trajectory"] == "Surface"
    assert rec["dose_equivalent_rate_usv_hr"] > 0


def test_radlab_processing():
    records = fetch_radlab_telemetry()
    df = process_radlab_telemetry(records)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    row = df.iloc[0]
    # 57.1 * 24 / 1000 = 1.3704 -> round(3) = 1.370
    assert abs(row["daily_gcr_dose_msv"] - 1.370) < 0.01
    assert abs(row["mission_30d_gcr_dose_msv"] - 41.11) < 0.1
    # Sheltered rate should be strictly lower than unsheltered
    assert row["sheltered_daily_gcr_dose_msv"] < row["daily_gcr_dose_msv"]


def test_radlab_validation():
    records = fetch_radlab_telemetry()
    df = process_radlab_telemetry(records)
    errors = validate_radiation_dataframe(df)
    assert len(errors) == 0


def test_save_processed_radiation(tmp_path):
    records = fetch_radlab_telemetry()
    df = process_radlab_telemetry(records)
    out_file = save_processed_radiation_parameters(df, output_path=tmp_path / "rad.csv")
    assert out_file.exists()

