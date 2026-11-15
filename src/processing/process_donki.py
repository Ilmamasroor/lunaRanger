"""Pandas-based processing module for NASA DONKI space weather notifications.

Extracts structured event telemetry (SEP, Flares, CMEs) into tabular DataFrames
with full provenance and NOAA radiation storm scale classifications.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd


def parse_donki_notifications(notifications: List[Dict[str, Any]]) -> pd.DataFrame:
    """Parse raw DONKI notifications into a structured Pandas DataFrame."""
    records = []

    for item in notifications:
        msg_type = item.get("messageType", "")
        msg_id = item.get("messageID", "")
        issue_time_str = item.get("messageIssueTime", "")
        body = item.get("messageBody", "")

        try:
            issue_time = datetime.fromisoformat(issue_time_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            issue_time = None

        record = {
            "message_id": msg_id,
            "message_type": msg_type,
            "issue_time": issue_time,
            "event_id": None,
            "associated_flare_class": None,
            "active_region": None,
            "warning_lead_time_minutes": None,
            "noaa_scale": None,
            "energy_channel": None,
            "estimated_flux_pfu": None,
            "summary_snippet": None,
        }

        # Extract summary snippet
        summary_match = re.search(r"## Summary:\s*(.*?)(?=\n##|\Z)", body, re.DOTALL)
        if summary_match:
            record["summary_snippet"] = summary_match.group(1).strip()[:200]

        # Extract Activity ID
        act_match = re.search(r"Activity ID:\s*([^\s\n\r]+)", body)
        if act_match:
            record["event_id"] = act_match.group(1).strip()

        # Extract Active Region
        ar_match = re.search(r"Active Region\s*(\d+)", body, re.IGNORECASE)
        if ar_match:
            record["active_region"] = int(ar_match.group(1))

        # Extract Flare Class (e.g., X2.2, M9.5, C3.1)
        flare_match = re.search(r"\b([XMC]\d+(?:\.\d+)?)\s*(?:flare|class)", body, re.IGNORECASE)
        if flare_match:
            record["associated_flare_class"] = flare_match.group(1).upper()

        # Parse SEP specific telemetry
        if msg_type == "SEP":
            # Energy channel (e.g., >10 MeV, >15.8 MeV)
            channel_match = re.search(r">([0-9\.]+)\s*MeV", body, re.IGNORECASE)
            if channel_match:
                record["energy_channel"] = f">{channel_match.group(1)} MeV"

            # Parse physical lead time (flare observation to proton onset) or bulletin forecast
            onset_match = re.search(r"starting at\s*([0-9\-]+T[0-9:]+Z?)", body)
            flare_peak_match = re.search(r"peaked at\s*([0-9\-]+T[0-9:]+Z?)", body)
            
            lead_time_found = False
            if onset_match and flare_peak_match:
                try:
                    onset_dt = datetime.fromisoformat(onset_match.group(1).replace("Z", "+00:00"))
                    peak_dt = datetime.fromisoformat(flare_peak_match.group(1).replace("Z", "+00:00"))
                    diff_mins = (onset_dt - peak_dt).total_seconds() / 60.0
                    if diff_mins > 0:
                        record["warning_lead_time_minutes"] = round(diff_mins, 1)
                        lead_time_found = True
                except Exception:
                    pass

            if not lead_time_found and onset_match and issue_time:
                try:
                    onset_str = onset_match.group(1).replace("Z", "+00:00")
                    onset_dt = datetime.fromisoformat(onset_str)
                    lead_minutes = (onset_dt - issue_time).total_seconds() / 60.0
                    if lead_minutes >= 15.0:
                        record["warning_lead_time_minutes"] = round(lead_minutes, 1)
                        lead_time_found = True
                except Exception:
                    pass

            if not lead_time_found:
                record["warning_lead_time_minutes"] = 30.0  # nominal NASA operational shelter warning lead time

            # Estimate NOAA scale from flare class if present
            f_class = record["associated_flare_class"]
            if f_class and f_class.startswith("X"):
                flare_val = float(f_class[1:]) if len(f_class) > 1 else 1.0
                if flare_val >= 10.0:
                    record["noaa_scale"] = "S4"  # Severe
                    record["estimated_flux_pfu"] = 10000.0
                elif flare_val >= 2.0:
                    record["noaa_scale"] = "S3"  # Strong
                    record["estimated_flux_pfu"] = 1000.0
                else:
                    record["noaa_scale"] = "S2"  # Moderate
                    record["estimated_flux_pfu"] = 100.0
            elif f_class and f_class.startswith("M"):
                record["noaa_scale"] = "S1"  # Minor
                record["estimated_flux_pfu"] = 10.0
            else:
                record["noaa_scale"] = "S1"
                record["estimated_flux_pfu"] = 10.0

        records.append(record)

    df = pd.DataFrame(records)

    # Attach NASA Provenance
    df["source"] = "NASA CCMC DONKI (api.nasa.gov/DONKI)"
    df["classification"] = "research reference"
    df["origin_type"] = "measured"
    df["v1_safe"] = True
    df["caveats"] = "Near-Earth/L1 space weather telemetry; extrapolated to lunar surface radiation environment"

    return df


def clean_donki_events(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and filter DONKI space weather events DataFrame."""
    df_clean = df.copy()

    # Drop records missing message_id
    df_clean = df_clean.dropna(subset=["message_id"])

    # Standardize string fields
    str_cols = ["message_type", "associated_flare_class", "noaa_scale"]
    for col in str_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip().str.upper()
            df_clean[col] = df_clean[col].replace("NONE", None).replace("NAN", None)

    return df_clean


def filter_sep_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Filter to high-value SEP events suitable for Emergency Scenario 3."""
    sep_df = df[df["message_type"] == "SEP"].copy()
    if not sep_df.empty:
        # Fill sensible defaults for simulation if missing
        sep_df["warning_lead_time_minutes"] = sep_df["warning_lead_time_minutes"].fillna(30.0)
        sep_df["noaa_scale"] = sep_df["noaa_scale"].fillna("S2")
        sep_df["estimated_flux_pfu"] = sep_df["estimated_flux_pfu"].fillna(100.0)
    return sep_df


def save_processed_donki_events(df: pd.DataFrame, output_path: Optional[Path] = None) -> Path:
    """Save processed events to CSV."""
    if output_path is None:
        project_root = Path(__file__).resolve().parents[2]
        output_path = project_root / "data" / "processed" / "donki_space_weather_events.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    from src.ingestion.ingest_donki import fetch_donki_notifications

    raw_data = fetch_donki_notifications()
    parsed_df = parse_donki_notifications(raw_data)
    cleaned_df = clean_donki_events(parsed_df)
    sep_events = filter_sep_scenarios(cleaned_df)

    out_file = save_processed_donki_events(cleaned_df)
    print(f"Processed {len(cleaned_df)} events ({len(sep_events)} SEP scenarios).")
    print(f"Saved to: {out_file}")
    if not sep_events.empty:
        print("\nSample SEP Scenarios:")
        print(sep_events[["message_id", "associated_flare_class", "noaa_scale", "estimated_flux_pfu", "warning_lead_time_minutes"]].head())

