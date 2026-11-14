"""Validation module for space radiation parameters."""

from typing import List
import pandas as pd


REQUIRED_RAD_COLUMNS = [
    "record_id",
    "celestial_body",
    "dose_equivalent_rate_usv_hr",
    "daily_gcr_dose_msv",
    "source",
    "classification",
    "origin_type",
    "v1_safe"
]


def validate_radiation_dataframe(df: pd.DataFrame) -> List[str]:
    """Validate radiation DataFrame against scientific ranges."""
    errors = []

    # 1. Column presence
    missing_cols = [col for col in REQUIRED_RAD_COLUMNS if col not in df.columns]
    if missing_cols:
        return [f"Missing required radiation columns: {missing_cols}"]

    if df.empty:
        return ["Radiation DataFrame is empty."]

    # 2. Celestial body check
    if not (df["celestial_body"] == "Moon").all():
        errors.append("Dataset contains non-lunar records.")

    # 3. Astrophysical sanity ranges for lunar surface GCR
    rates = pd.to_numeric(df["dose_equivalent_rate_usv_hr"], errors="coerce")
    if rates.isnull().any():
        errors.append("dose_equivalent_rate_usv_hr must be numeric.")
    elif (rates < 10.0).any() or (rates > 200.0).any():
        errors.append("dose_equivalent_rate_usv_hr out of expected lunar surface range (10-200 µSv/hr).")

    # 4. Provenance
    if not (df["classification"] == "research reference").all():
        errors.append("Radiation parameters must have classification 'research reference'.")

    return errors


if __name__ == "__main__":
    from src.ingestion.ingest_radlab import fetch_radlab_telemetry
    from src.processing.process_radiation import process_radlab_telemetry

    recs = fetch_radlab_telemetry()
    df = process_radlab_telemetry(recs)
    errs = validate_radiation_dataframe(df)
    if errs:
        print("Validation errors:")
        for e in errs:
            print("-", e)
    else:
        print("Radiation telemetry DataFrame passed all validation checks!")

