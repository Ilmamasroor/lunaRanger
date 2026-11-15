"""Unit tests for the research deliverables ingestion and processing pipeline."""

import pytest
import pandas as pd

from src.ingestion.load_research_deliverables import (
    load_research_parameters,
    load_dependency_matrix_edges
)
from src.processing.process_research_parameters import (
    transform_research_dataframe_to_parameters,
    _clean_numeric_value,
    get_unresolved_parameters_report,
    get_unsupported_unit_parameters_report
)


def test_load_research_parameters():
    df = load_research_parameters()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) >= 35
    assert "parameter_name" in df.columns
    assert "raw_value" in df.columns
    assert "classification" in df.columns


def test_load_dependency_matrix_edges():
    edges = load_dependency_matrix_edges()
    assert isinstance(edges, pd.DataFrame)
    assert len(edges) == 16  # All 16 documented dependency edges


def test_clean_numeric_value():
    assert _clean_numeric_value("~0.89") == 0.89
    assert _clean_numeric_value("13.2 ± 1") == 13.2
    assert _clean_numeric_value("~2,500–3,500") == 3000.0
    assert _clean_numeric_value("To be defined") is None
    assert _clean_numeric_value("qualitative") is None


def test_transform_research_dataframe_to_parameters():
    df = load_research_parameters()
    params = transform_research_dataframe_to_parameters(df)
    assert isinstance(params, list)
    # 23 parameters have valid numbers and registry units; 22 are unresolved, 21 have unsupported units
    assert len(params) == 23

    unresolved = get_unresolved_parameters_report()
    unsupported = get_unsupported_unit_parameters_report()
    assert len(unresolved) == 22
    assert len(unsupported) == 21
    assert len(params) + len(unresolved) + len(unsupported) == len(df)

    # Check schema compliance of every parameter — TypeScript contract fields
    required_keys = {
        "parameter_id",
        "resource",
        "flow_type",
        "value",
        "basis",
        "unit",
        "classification",
        "data_status",
        "source",
        "assumptions",
        "caveats"
    }
    for p in params:
        assert required_keys.issubset(p.keys())
        if p["basis"] == "per_time":
            assert "period" in p and isinstance(p["period"], dict)
            assert "value" in p["period"] and "unit" in p["period"]
        assert isinstance(p["assumptions"], list)
        assert isinstance(p["caveats"], list)
        assert p["value"] >= 0

