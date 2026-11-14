"""Validation module for space crop parameters."""

from typing import List
import pandas as pd


REQUIRED_CROP_COLUMNS = [
    "crop_id",
    "common_name",
    "first_harvest_days",
    "water_use_rate_l_m2_d",
    "source",
    "classification",
    "origin_type",
    "v1_safe",
]


def validate_crop_dataframe(df: pd.DataFrame) -> List[str]:
    """Validate processed crop DataFrame against scientific constraints."""
    errors = []

    # 1. Column presence
    missing_cols = [col for col in REQUIRED_CROP_COLUMNS if col not in df.columns]
    if missing_cols:
        return [f"Missing required crop columns: {missing_cols}"]

    # 2. Check empty
    if df.empty:
        return ["Crop DataFrame is empty."]

    # 3. Unique ID
    if df["crop_id"].duplicated().any():
        errors.append("Duplicate crop_id detected.")

    # 4. Numeric validity
    harvest_days = pd.to_numeric(df["first_harvest_days"], errors="coerce")
    if harvest_days.isnull().any() or (harvest_days <= 0).any():
        errors.append("first_harvest_days must be strictly positive integers.")

    water_rates = pd.to_numeric(df["water_use_rate_l_m2_d"], errors="coerce")
    if water_rates.isnull().any() or (water_rates <= 0).any():
        errors.append("water_use_rate_l_m2_d must be strictly positive floats.")

    # 5. Provenance integrity
    if not (df["classification"] == "research reference").all():
        errors.append("All crops must have classification 'research reference'.")

    return errors


if __name__ == "__main__":
    from src.processing.process_osdr_crops import build_crop_parameters_dataframe

    df = build_crop_parameters_dataframe()
    errs = validate_crop_dataframe(df)
    if errs:
        print("Validation errors:")
        for e in errs:
            print("-", e)
    else:
        print("Crop DataFrame validated successfully!")

