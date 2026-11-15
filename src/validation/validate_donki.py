"""Validation module for processed NASA DONKI space weather events."""

from typing import List
import pandas as pd


REQUIRED_DONKI_COLUMNS = [
    "message_id",
    "message_type",
    "source",
    "classification",
    "origin_type",
    "v1_safe",
]


def validate_donki_dataframe(df: pd.DataFrame) -> List[str]:
    """Validate processed DONKI DataFrame against data and scientific rules."""
    errors = []

    # 1. Column presence
    missing_cols = [col for col in REQUIRED_DONKI_COLUMNS if col not in df.columns]
    if missing_cols:
        return [f"Missing required columns: {missing_cols}"]

    # 2. Emptiness check
    if df.empty:
        errors.append("DONKI DataFrame is empty.")
        return errors

    # 3. Message ID uniqueness / null check
    if df["message_id"].isnull().any():
        errors.append("Found null message_id values in DONKI dataset.")
    if df["message_id"].duplicated().any():
        errors.append("Duplicate message_id records found in DONKI dataset.")

    # 4. Message types check
    valid_types = {"SEP", "FLR", "CME", "GST", "IPS", "MPC", "RBE", "HSS", "REPORT"}
    invalid_types = set(df["message_type"].dropna().unique()) - valid_types
    if invalid_types:
        errors.append(f"Unexpected message types encountered: {invalid_types}")

    # 5. Numeric boundary checks
    if "warning_lead_time_minutes" in df.columns:
        lead_times = pd.to_numeric(df["warning_lead_time_minutes"].dropna(), errors="coerce")
        if (lead_times < 0).any():
            errors.append("warning_lead_time_minutes cannot be negative.")

    if "estimated_flux_pfu" in df.columns:
        flux = pd.to_numeric(df["estimated_flux_pfu"].dropna(), errors="coerce")
        if (flux <= 0).any():
            errors.append("estimated_flux_pfu must be strictly positive when present.")

    # 6. Provenance & Scientific rules: no invented science
    if not (df["source"] == "NASA CCMC DONKI (api.nasa.gov/DONKI)").all():
        errors.append("Invalid source attribution; must be NASA CCMC DONKI.")

    if not (df["classification"] == "research reference").all():
        errors.append("Invalid classification; must be 'research reference'.")

    return errors


if __name__ == "__main__":
    from src.ingestion.ingest_donki import fetch_donki_notifications
    from src.processing.process_donki import parse_donki_notifications, clean_donki_events

    data = fetch_donki_notifications()
    parsed = parse_donki_notifications(data)
    cleaned = clean_donki_events(parsed)

    errs = validate_donki_dataframe(cleaned)
    if errs:
        print("Validation failed:")
        for e in errs:
            print("-", e)
    else:
        print("DONKI DataFrame passed all validation checks!")

