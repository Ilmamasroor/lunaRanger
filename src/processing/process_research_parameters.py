"""Processing module converting parsed research deliverables into standardized TypeScript SimulationParameters.

Conforms strictly to the documented TypeScript SimulationParameter contract:
{
  "parameter_id": str,
  "resource": str (optional for non-resource flows),
  "system": str (optional),
  "equipment_id": str (optional),
  "flow_type": "consumption" | "production" | "generation" | "removal" | "recovery" | "loss" | "capacity" | "requirement",
  "value": number (finite, non-negative),
  "unit": string (one of the 17 units in the TypeScript registry),
  "basis": "per_person" | "per_equipment" | "per_cycle" | "per_time" | "total",
  "period": {"value": number, "unit": "second" | "minute" | "hour" | "day" | "cycle"} (required for per_time),
  "classification": "research_data" | "engineering_inference" | "gameplay_assumption",
  "data_status": "mock" | "pending_review" | "validated" | "TBD",
  "source": {"title": str, "url": str|null, "identifier": str|null, "location": str|null} | null,
  "assumptions": [str, ...],
  "caveats": [str, ...]
}
"""

import math
import re
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd


# Documented TypeScript Unit Registry (exactly 17 units)
REGISTRY_UNITS = frozenset({
    "kg",
    "g",
    "L",
    "mL",
    "kcal",
    "Wh",
    "kWh",
    "W",
    "kW",
    "kg/day",
    "kg/cycle",
    "L/day",
    "Wh/cycle",
    "kWh/cycle",
    "kg/m3",
    "ppm",
    "percent"
})

# Resource-specific supported units
RESOURCE_SUPPORTED_UNITS = {
    "oxygen": frozenset({"kg", "kg/day", "kg/cycle", "g"}),
    "co2": frozenset({"kg", "kg/day", "kg/cycle", "g"}),
    "water": frozenset({"kg", "kg/day", "kg/cycle", "L", "L/day", "g", "mL"}),
    "food": frozenset({"kcal", "kg", "kg/day"}),
    "power": frozenset({"Wh", "Wh/cycle", "kWh", "kWh/cycle", "W", "kW"}),
}

VALID_FLOW_TYPES = frozenset({
    "consumption", "production", "generation",
    "removal", "recovery", "loss", "capacity", "requirement"
})

VALID_CLASSIFICATIONS = frozenset({
    "research_data", "engineering_inference", "gameplay_assumption"
})

VALID_DATA_STATUSES = frozenset({
    "mock", "pending_review", "validated", "TBD"
})

VALID_BASES = frozenset({
    "per_person", "per_equipment", "per_cycle", "per_time", "total"
})

VALID_PERIOD_UNITS = frozenset({
    "second", "minute", "hour", "day", "cycle"
})

PER_TIME_PERIOD_UNITS = frozenset({
    "hour", "day", "cycle"
})


# Storage for tracking parameters that cannot be emitted as valid SimulationParameters
# without fabricating values or units, preserving complete scientific traceability.
UNRESOLVED_RESEARCH_PARAMETERS: List[Dict[str, Any]] = []
UNSUPPORTED_UNIT_PARAMETERS: List[Dict[str, Any]] = []


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
    """Identify flow direction strictly matching the TypeScript runtime validator enum:
    ['consumption', 'production', 'generation', 'removal', 'recovery', 'loss', 'capacity', 'requirement']
    """
    p_lower = param_name.lower()

    # Recovery streams
    if any(k in p_lower for k in ["recovery", "recycled", "fallback"]):
        return "recovery"

    # Active Generation
    if any(k in p_lower for k in ["generation capacity", "fission surface-power", "fission daily energy", "electrolysis"]):
        return "generation"

    # Capacity / Storage
    if any(k in p_lower for k in ["reserve", "stored", "storage", "capacity", "battery", "shelf life", "shelf_life", "target for beyond-leo"]):
        return "capacity"

    # Removal
    if any(k in p_lower for k in ["scrubber", "removal", "co2 removal"]):
        return "removal"

    # Loss / Environmental degradation / Hazard
    if any(k in p_lower for k in ["absorbed dose", "dose-equivalent", "gcr", "dose", "spe", "hazard", "leak"]):
        return "loss"

    # Production
    if any(k in p_lower for k in ["production", "exhaled"]):
        return "production"

    # Requirements (target constraints, planning standards, growth times)
    if any(k in p_lower for k in ["requirement", "demand", "target", "design goal", "growth time", "fertilizer required", "schedule", "duration"]):
        return "requirement"

    # Consumption
    if any(k in p_lower for k in ["consumption", "water use", "packaged food", "energy requirement"]):
        return "consumption"

    return "requirement"


def _normalize_unit_and_basis(param_name: str, raw_unit: str) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    """Map raw physical unit and measurement context to the documented TypeScript Unit Registry and Basis enum.

    Returns:
        (canonical_unit, basis, period_dict) or (None, None, None) if unsupported.
    """
    p_lower = param_name.lower()
    u_lower = raw_unit.lower().strip()

    # Percentages
    if "%" in u_lower:
        if any(k in p_lower for k in ["bpa", "brine", "urine", "humidity"]):
            return "percent", "per_equipment", None
        return "percent", "total", None

    # Power & Energy (kW, W, kWh)
    if "continuous" in u_lower or u_lower == "kw":
        return "kW", "per_equipment", None
    if "kwh/day" in u_lower:
        return "kWh", "per_time", {"value": 1, "unit": "day"}
    if "kwh" in u_lower:
        return "kWh", "total", None
    if u_lower == "w" or "watt" in u_lower:
        return "W", "per_equipment", None

    # Food Calories (kcal)
    if "kcal" in u_lower:
        if "/person" in u_lower or "per astronaut" in p_lower:
            return "kcal", "per_person", {"value": 1, "unit": "day"}
        return "kcal", "per_time", {"value": 1, "unit": "day"}

    # Mass (kg, g)
    if "year" in u_lower or "years" in u_lower:
        # Annual rates cannot be represented without year in Period (only second/minute/hour/day/cycle supported)
        return None, None, None
    if "kg/person/day" in u_lower:
        return "kg", "per_person", {"value": 1, "unit": "day"}
    if "kg/day" in u_lower:
        return "kg/day", "per_time", {"value": 1, "unit": "day"}
    if "g/min/person" in u_lower or ("g/min" in u_lower and "person" in p_lower):
        return "g", "per_person", {"value": 1, "unit": "minute"}
    if "kg" in u_lower:
        # Mission total mass parameters (e.g. 30-day requirements)
        return "kg", "total", None

    # Volume (L, L/day, mL)
    if "l/day" in u_lower:
        return "L/day", "per_time", {"value": 1, "unit": "day"}
    if u_lower in ["l", "liter", "liters"]:
        return "L", "total", None

    # Unsupported units in TypeScript registry
    # (e.g. μGy/hour, μSv/hour, mSv/day, pfu, Earth days, days, years, m², L/m²/d, astronauts, ratio, qualitative)
    return None, None, None


def _determine_classification_and_status(classification_raw: str, numeric_val: Optional[float]) -> Tuple[str, str]:
    """Map to TypeScript enums:
    classification: ['research_data', 'engineering_inference', 'gameplay_assumption']
    data_status: ['mock', 'pending_review', 'validated', 'TBD']
    """
    c_lower = classification_raw.lower()

    if numeric_val is None or "requires research" in c_lower or "to be defined" in c_lower:
        if "modelling decision" in c_lower or "gameplay" in c_lower:
            return "gameplay_assumption", "TBD"
        return "research_data", "TBD"

    # Derived calculations & engineering inferences: pending_review (not auto-validated)
    if "derived" in c_lower or "engineering inference" in c_lower:
        return "engineering_inference", "pending_review"

    if "gameplay assumption" in c_lower or "modelling decision" in c_lower:
        return "gameplay_assumption", "pending_review"

    # Research references and measured data: pending_review until explicitly validated for sim use
    if "research reference" in c_lower or "measured" in c_lower or "modelled" in c_lower:
        return "research_data", "pending_review"

    return "research_data", "pending_review"


def _build_structured_source(source_raw: Any, param_name: str) -> Optional[Dict[str, Optional[str]]]:
    """Parse raw source string into structured object expected by TypeScript contract:
    { "title": str, "url": str | null, "identifier": str | null, "location": str | null }
    """
    if not source_raw or pd.isna(source_raw) or str(source_raw).lower() in ["none", "nan", "tbd", "to be defined"]:
        return None

    s_str = str(source_raw).strip()
    p_lower = param_name.lower()

    if "ewert" in s_str.lower() or "2019 mass-balance" in s_str.lower() or "bvad" in s_str.lower() or "reference astronaut" in s_str.lower():
        return {
            "title": "Astronaut Mass Balance for Long Duration Missions",
            "url": "https://ntrs.nasa.gov/citations/20190027563",
            "identifier": "NASA NTRS 20190027563 / BVAD Table 4-53",
            "location": "Table 4-53 & Section 3.1"
        }
    if "chang'e-4" in s_str.lower() or "science advances" in s_str.lower() or "silicon" in p_lower:
        return {
            "title": "First Measurements of the Low-Energy Cosmic Radiation on the Lunar Surface",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7518862/",
            "identifier": "DOI: 10.1126/sciadv.aaz2574",
            "location": "Chang'e-4 LND Instrument Telemetry"
        }
    if "iss" in s_str.lower() and ("milestone" in s_str.lower() or "bpa" in s_str.lower() or "recovery" in s_str.lower()):
        return {
            "title": "NASA Achieves Water Recovery Milestone on International Space Station",
            "url": "https://www.nasa.gov/missions/station/iss-research/nasa-achieves-water-recovery-milestone-on-international-space-station/",
            "identifier": "NASA ISS ECLSS Milestone 2023",
            "location": "Brine Processor Assembly (BPA) Telemetry Report"
        }
    if "tm-2020-5008832" in s_str.lower() or ("wheeler 2020" in s_str.lower() and "table 2" in s_str.lower()):
        return {
            "title": "NASA's Contributions to Vertical Farming",
            "url": "https://ntrs.nasa.gov/api/citations/20205008832/downloads/NASA%20TM-2020-5008832%20NASA's%20Contributions%20to%20Vertical%20Farming.pdf",
            "identifier": "NASA TM-2020-5008832",
            "location": "Page 9, Table 2"
        }
    if "wheeler 1996" in s_str.lower() or "bpc" in s_str.lower():
        return {
            "title": "Gas Exchange and Growth of Plants in a Large Controlled Environment",
            "url": "https://www.sciencedirect.com/science/article/pii/027311779500880N",
            "identifier": "Advances in Space Research Vol 18",
            "location": "Biomass Production Chamber Results"
        }
    if "20200002230" in s_str.lower() or ("fertilizer" in p_lower and "wheeler" in s_str.lower()):
        return {
            "title": "Nutrient and Fertilizer Requirements for Controlled Environment Agriculture",
            "url": "https://ntrs.nasa.gov/api/citations/20200002230/downloads/20200002230.pdf",
            "identifier": "NASA NTRS 20200002230",
            "location": "Section 4 (Fertilizer Demands)"
        }
    if "cooper" in s_str.lower() or "shelf life" in p_lower or "5466603" in s_str.lower():
        return {
            "title": "Nutrient Stability of Space Foods for Long-Duration Space Missions",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5466603/",
            "identifier": "NPJ Microgravity (2017) 3:17",
            "location": "Table 2 (Vitamin Degradation Kinetics)"
        }
    if "stemonstration" in s_str.lower() or "science friday" in s_str.lower() or "energy requirement" in p_lower:
        return {
            "title": "NASA STEMonstration: Nutrition & ISS Food Systems",
            "url": "https://www.nasa.gov/stem-content/stemonstrations-nutrition",
            "identifier": "NASA STEM Education / Science Friday 2022",
            "location": "Astronaut Caloric Requirements Guidelines"
        }
    if "moon fact sheet" in s_str.lower() or "nssdc" in s_str.lower() or "synodic" in s_str.lower():
        return {
            "title": "NASA Planetary Science Moon Fact Sheet",
            "url": "https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html",
            "identifier": "NASA NSSDCA Fact Sheet",
            "location": "Lunar Synodic Orbital Period Telemetry"
        }
    if "donki" in s_str.lower() or "ccmc" in s_str.lower():
        return {
            "title": "CCMC Database Of Notifications, Knowledge, Information (DONKI)",
            "url": "https://ccmc.gsfc.nasa.gov/tools/DONKI/",
            "identifier": "NASA CCMC DONKI",
            "location": "api.nasa.gov/DONKI/notifications"
        }
    if "osdr" in s_str.lower() or "osd-269" in s_str.lower() or "veg-03" in s_str.lower():
        return {
            "title": "VEG-03A: Plant Growth in Space (Red Romaine Lettuce)",
            "url": "https://osdr.nasa.gov/bio/repo/data/studies/OSD-269",
            "identifier": "NASA OSDR OSD-269",
            "location": "Payload Telemetry & Harvest Yields"
        }
    if "fission" in s_str.lower() or "fission" in p_lower:
        return {
            "title": "NASA Fission Surface Power Project",
            "url": "https://www.nasa.gov/exploration-systems-development-mission-directorate/fission-surface-power/",
            "identifier": "NASA STMD Technology Goal",
            "location": "40 kW Continuous Power Target"
        }

    return {
        "title": s_str,
        "url": None,
        "identifier": None,
        "location": None
    }


def _format_parameter_id(param_name: str) -> str:
    """Generate snake_case parameter identifier with normalized ASCII."""
    normalized = param_name.lower().replace("o₂", "o2").replace("co₂", "co2")
    cleaned = re.sub(r"[^\w\s-]", "", normalized)
    cleaned = re.sub(r"[\s-]+", "_", cleaned).strip("_")
    return cleaned


def transform_research_dataframe_to_parameters(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Transform parsed research DataFrame into standard TypeScript SimulationParameter dictionaries.

    Only parameters with a defensible, finite, non-negative numeric value AND a unit supported
    by the documented TypeScript Unit Registry are emitted into mission_config.json.
    Unresolved (TBD) parameters and parameters with unsupported units are tracked separately
    to avoid fabricating values or emitting invalid units.
    """
    global UNRESOLVED_RESEARCH_PARAMETERS, UNSUPPORTED_UNIT_PARAMETERS
    UNRESOLVED_RESEARCH_PARAMETERS = []
    UNSUPPORTED_UNIT_PARAMETERS = []

    parameters = []

    for _, row in df.iterrows():
        param_name = str(row.get("parameter_name", "")).strip()
        raw_val = str(row.get("raw_value", "")).strip()
        raw_unit = str(row.get("raw_unit", "")).strip()
        source = row.get("source")
        classification_raw = str(row.get("classification", "")).strip()
        desc = str(row.get("description", "")).strip() if pd.notna(row.get("description")) else param_name
        caveats = str(row.get("caveats", "")).strip() if pd.notna(row.get("caveats")) else ""

        numeric_val = _clean_numeric_value(raw_val)

        # 1. Unresolved / TBD values: Do NOT emit with null or zero.
        if numeric_val is None or not math.isfinite(numeric_val) or numeric_val < 0:
            UNRESOLVED_RESEARCH_PARAMETERS.append({
                "parameter_name": param_name,
                "raw_value": raw_val,
                "raw_unit": raw_unit,
                "reason": "Unresolved scientific value (TBD/qualitative/formula); cannot assign number without inventing data"
            })
            continue

        # 2. Unit and basis normalization
        norm_unit, basis, period = _normalize_unit_and_basis(param_name, raw_unit)
        if norm_unit is None or norm_unit not in REGISTRY_UNITS:
            UNSUPPORTED_UNIT_PARAMETERS.append({
                "parameter_name": param_name,
                "numeric_value": numeric_val,
                "raw_unit": raw_unit,
                "reason": f"Unit '{raw_unit}' is not in the documented TypeScript unit registry and cannot be converted without inventing science"
            })
            continue

        resource = _classify_resource(param_name, raw_unit)
        flow_type = _classify_flow_type(param_name, numeric_val)
        classification_ts, data_status_ts = _determine_classification_and_status(classification_raw, numeric_val)
        structured_source = _build_structured_source(source, param_name)
        param_id = _format_parameter_id(param_name)

        # Assumptions and caveats
        assumptions = []
        if classification_ts == "gameplay_assumption":
            assumptions.append("Design and gameplay assumption agreed by development team")
        if "exercise" in param_name.lower():
            assumptions.append("Applies only to scheduled exercise windows; MUST NOT be used as an EVA rate")

        caveats_list = []
        if caveats and caveats != "nan" and caveats.strip():
            caveats_list.append(caveats.strip())

        param_dict: Dict[str, Any] = {
            "parameter_id": param_id,
            "resource": resource,
            "flow_type": flow_type,
            "value": numeric_val,
            "unit": norm_unit,
            "basis": basis,
            "classification": classification_ts,
            "data_status": data_status_ts,
            "source": structured_source,
            "assumptions": assumptions,
            "caveats": caveats_list
        }

        if period is not None:
            param_dict["period"] = period

        parameters.append(param_dict)

    return parameters


def get_unresolved_parameters_report() -> List[Dict[str, Any]]:
    """Return the list of parameters that could not be mapped due to unresolved scientific values."""
    if not UNRESOLVED_RESEARCH_PARAMETERS:
        from src.ingestion.load_research_deliverables import load_research_parameters
        transform_research_dataframe_to_parameters(load_research_parameters())
    return list(UNRESOLVED_RESEARCH_PARAMETERS)


def get_unsupported_unit_parameters_report() -> List[Dict[str, Any]]:
    """Return the list of parameters omitted due to unsupported units in the TypeScript registry."""
    if not UNSUPPORTED_UNIT_PARAMETERS:
        from src.ingestion.load_research_deliverables import load_research_parameters
        transform_research_dataframe_to_parameters(load_research_parameters())
    return list(UNSUPPORTED_UNIT_PARAMETERS)
