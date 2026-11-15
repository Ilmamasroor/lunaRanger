"""Tests for the initial mock resource pipeline."""

import pytest
import pandas as pd
from src.ingestion.load_resources import load_resource_data
from src.processing.clean_resources import clean_resource_data
from src.validation.validate_resources import validate_resource_data
from src.mapping.map_resources import map_resource_data


def test_load_resource_data():
    df = load_resource_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "resource" in df.columns
    assert "value_per_person" in df.columns


def test_clean_resource_data():
    raw_df = load_resource_data()
    cleaned_df = clean_resource_data(raw_df)
    assert pd.api.types.is_numeric_dtype(cleaned_df["value_per_person"])
    for col in ["resource", "unit", "period", "data_status"]:
        assert cleaned_df[col].str.islower().all()


def test_validate_resource_data_success():
    raw_df = load_resource_data()
    cleaned_df = clean_resource_data(raw_df)
    errors = validate_resource_data(cleaned_df)
    assert len(errors) == 0


def test_validate_resource_data_missing_column():
    df = pd.DataFrame({"resource": ["oxygen"]})
    errors = validate_resource_data(df)
    assert len(errors) > 0
    assert "Missing columns" in errors[0]


def test_map_resource_data():
    raw_df = load_resource_data()
    cleaned_df = clean_resource_data(raw_df)
    config = map_resource_data(cleaned_df, crew_size=4)
    assert config["schema_version"] == "1.1"
    assert config["mission"]["crew_size"] == 4
    assert len(config["parameters"]) == 4

