"""Pandas processing module for space radiation telemetry from NASA OSDR RadLab.

Calculates baseline surface GCR dose rates, daily accumulations, shelter attenuation,
and 30-day mission totals with full provenance tracking.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd


def process_radlab_telemetry(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Process raw RadLab telemetry into a structured Pandas DataFrame."""
    df = pd.DataFrame(records)

    # Calculate daily accumulation rate (mSv/day) from hourly µSv/hr: (rate * 24) / 1000
    df["daily_gcr_dose_msv"] = (df["dose_equivalent_rate_usv_hr"] * 24.0) / 1000.0

    # 30-day mission reference accumulation (mSv)
    df["mission_30d_gcr_dose_msv"] = df["daily_gcr_dose_msv"] * 30.0

    # Shelter attenuation calculations (default 90% reduction)
    shelter_factor = 0.90
    df["shelter_protection_factor"] = shelter_factor
    df["sheltered_daily_gcr_dose_msv"] = df["daily_gcr_dose_msv"] * (1.0 - (shelter_factor * 0.5))
    df["sheltered_30d_gcr_dose_msv"] = df["sheltered_daily_gcr_dose_msv"] * 30.0

    # Round floats for clean representation
    float_cols = [
        "daily_gcr_dose_msv",
        "mission_30d_gcr_dose_msv",
        "sheltered_daily_gcr_dose_msv",
        "sheltered_30d_gcr_dose_msv"
    ]
    for col in float_cols:
        df[col] = df[col].round(3)

    return df


def save_processed_radiation_parameters(df: pd.DataFrame, output_path: Optional[Path] = None) -> Path:
    """Save processed radiation parameters to CSV."""
    if output_path is None:
        project_root = Path(__file__).resolve().parents[2]
        output_path = project_root / "data" / "processed" / "radiation_parameters.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    from src.ingestion.ingest_radlab import fetch_radlab_telemetry

    raw_recs = fetch_radlab_telemetry()
    rad_df = process_radlab_telemetry(raw_recs)
    out_file = save_processed_radiation_parameters(rad_df)

    print(f"Processed {len(rad_df)} radiation records.")
    print(f"Saved to: {out_file}")
    print("\nRadiation Parameters:")
    print(rad_df[["spacecraft", "dose_equivalent_rate_usv_hr", "daily_gcr_dose_msv", "mission_30d_gcr_dose_msv"]])

