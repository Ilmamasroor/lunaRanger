"""Processing module converting parsed research deliverables into standardized schema parameters."""

import re
from typing import Any, Dict, List, Optional
import pandas as pd


def _clean_numeric_value(raw_val: str) -> Optional[float]:
    """Clean markdown table cell value to a float or None if TBD/qualitative."""
    if not isinstance(raw_val, str):
        return None
    val_str = raw_val.strip()

    if re.search(r"\b(to be defined|tbd|none|qualitative|scheme|tier|formula)\b", val_str, re.IGNORECASE) or "×" in val_str or "*" in val_str:
        return None

    # Handle ranges like ~2,500–3,500 or 40–50 or ~93–94
    range_match = re.search(r"([0-9,]+(?:\.[0-9]+)?)\s*[–\-]\s*([0-9,]+(?:\.[0-9]+)?)", val_str)
    if range_match:
        try:
            low = float(range_match.group(1).replace(",", ""))
            high = float(range_match.group(2).replace(",", ""))
            return round((low + high) / 2.0, 3)
        except ValueError:
            pass

    # Handle mean ± uncertainty like 13.2 ± 1 or 57.1 ± 10.6
    plus_minus_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*±", val_str)
    if plus_minus_match:
        try:
            return float(plus_minus_match.group(1))
        except ValueError:
            pass

    # Handle single numbers with tilde or prefixes like ~0.89, >= 40
    num_match = re.search(r"([0-9]+(?:\.[0-9]+)?)", val_str.replace(",", ""))
    if num_match:
        try:
            return float(num_match.group(1))
        except ValueError:
            pass

    return None


def _classify_resource(param_name: str, unit: str) -> str:
    """Identify the system resource category."""
    p_lower = param_name.lower()
    norm_p = p_lower.replace("co₂", "co2").replace("o₂", "o2")
    u_lower = str(unit).lower()

    if "co2" in norm_p or "carbon" in norm_p:
        return "co2"
    if "o2" in norm_p or "oxygen" in norm_p or "air" in norm_p:
        return "oxygen"
    if "water" in norm_p or "urine" in norm_p or "humidity" in norm_p or "potable" in norm_p:
        return "water"
    if any(k in norm_p for k in ["food", "crop", "lettuce", "wheat", "soybean", "microgreens", "fertilizer"]) or (
        "energy" in norm_p and ("kcal" in u_lower or "cal" in u_lower or "food" in norm_p)
    ):
        return "food"
    if any(k in norm_p for k in ["radiation", "dose", "gcr", "spe", "shelter", "shield"]):
        return "radiation"
    if any(k in norm_p for k in ["power", "fission", "solar", "battery", "daytime", "nighttime", "lighting", "energy"]):
        return "power"
    if "crew" in p_lower or "mission" in p_lower:
        return "crew"
    return "general"


def _classify_flow_type(param_name: str, val: Optional[float]) -> str:
    """Identify flow direction: consumption, production, recovery, environment, storage, etc."""
    p_lower = param_name.lower()
    if any(k in p_lower for k in ["consumption", "requirement", "demand", "energy"]):
        return "consumption"
    if any(k in p_lower for k in ["production", "exhaled", "generation"]):
        return "production"
    if "recovery" in p_lower:
        return "recovery"
    if any(k in p_lower for k in ["reserve", "stored", "storage", "capacity"]):
        return "storage"
    if any(k in p_lower for k in ["dose", "gcr", "daytime", "nighttime", "lighting"]):
        return "environment"
    if any(k in p_lower for k in ["growth time", "area", "model"]):
        return "infrastructure"
    return "specification"


def _format_parameter_id(param_name: str) -> str:
    """Generate snake_case parameter identifier with normalized ASCII."""
    normalized = param_name.lower().replace("o₂", "o2").replace("co₂", "co2")
    cleaned = re.sub(r"[^\w\s-]", "", normalized)
    cleaned = re.sub(r"[\s-]+", "_", cleaned).strip("_")
    return cleaned


def transform_research_dataframe_to_parameters(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Transform parsed research DataFrame into standard schema parameter dictionaries."""
    parameters = []

    for _, row in df.iterrows():
        param_name = str(row.get("parameter_name", "")).strip()
        raw_val = str(row.get("raw_value", "")).strip()
        raw_unit = str(row.get("raw_unit", "")).strip()
        source = row.get("source")
        classification = str(row.get("classification", "")).strip().lower()
        desc = str(row.get("description", "")).strip() if pd.notna(row.get("description")) else param_name
        caveats = str(row.get("caveats", "")).strip() if pd.notna(row.get("caveats")) else ""

        numeric_val = _clean_numeric_value(raw_val)
        resource = _classify_resource(param_name, raw_unit)
        flow_type = _classify_flow_type(param_name, numeric_val)
        param_id = _format_parameter_id(param_name)

        # Standardize data status
        if numeric_val is None or "requires research" in classification:
            data_status = "tbd"
        elif "derived" in classification:
            data_status = "derived"
        elif "engineering inference" in classification:
            data_status = "engineering_inference"
        elif "gameplay assumption" in classification:
            data_status = "gameplay_assumption"
        elif "research reference" in classification:
            data_status = "research_reference"
        else:
            data_status = "research_reference"

        # Determine period
        period_unit = "day"
        if "min" in raw_unit:
            period_unit = "minute"
        elif "hour" in raw_unit:
            period_unit = "hour"
        elif "year" in raw_unit:
            period_unit = "year"

        # Compile assumptions list
        assumptions = []
        if data_status == "gameplay_assumption":
            assumptions.append("Design and gameplay assumption agreed by development team")
        if caveats and caveats != "nan":
            assumptions.append(caveats[:150])

        notes_parts = [f"Research value: '{raw_val}'", desc]
        if caveats and caveats != "nan":
            notes_parts.append(f"Caveat: {caveats}")
        full_notes = " | ".join(notes_parts)

        param_dict = {
            "parameter_id": param_id,
            "resource": resource,
            "flow_type": flow_type,
            "value_per_person": numeric_val,
            "raw_value": str(raw_val).strip() if raw_val else None,
            "unit": raw_unit,
            "period": {
                "value": 1,
                "unit": period_unit
            },
            "data_status": data_status,
            "source": str(source) if (source and str(source) != "nan") else None,
            "assumptions": assumptions,
            "notes": full_notes[:250]
        }
        parameters.append(param_dict)

    return parameters


if __name__ == "__main__":
    from src.ingestion.load_research_deliverables import load_research_parameters

    df_raw = load_research_parameters()
    params = transform_research_dataframe_to_parameters(df_raw)
    print(f"Transformed {len(params)} parameters.")
    print("\nSample Transformed Parameter:")
    import json
    print(json.dumps(params[3], indent=2))
