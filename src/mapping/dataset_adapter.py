"""Dataset Adapter mapping research deliverables and NASA API datasets to the TypeScript
SimulationParameter contract (Schema 1.1).

Every parameter produced here conforms to the shared TypeScript interface:
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

from typing import Any, Dict, List, Optional
import pandas as pd

from src.ingestion.load_research_deliverables import load_research_parameters
from src.processing.process_research_parameters import transform_research_dataframe_to_parameters


def build_unified_parameters_list(
    research_df: Optional[pd.DataFrame] = None,
    donki_sep_df: Optional[pd.DataFrame] = None,
    crops_df: Optional[pd.DataFrame] = None,
    radiation_df: Optional[pd.DataFrame] = None
) -> List[Dict[str, Any]]:
    """Assemble all parameters conforming to the TypeScript SimulationParameter contract into a unified list.

    Note on NASA API Datasets (RadLab, DONKI, OSDR Bio):
      - RadLab lunar dosimetry is measured in mSv/day and µSv/hour.
      - DONKI particle flux is measured in pfu, and warning lead time in minutes.
      - OSDR crop growth time is measured in days.
      Since none of these units ('mSv/day', 'pfu', 'minute', 'day') exist in the
      17-unit TypeScript unit registry, and converting them to abstract scores or
      invented radiation damage units is scientifically unjustified, these parameters
      are NOT emitted into mission_config.json. Instead:
      - DONKI space weather events are mapped to outputs/emergency_scenarios.json.
      - RadLab dosimetry is saved to data/processed/radiation_parameters.csv and tests/fixtures/.
      - OSDR crops are saved to data/processed/crop_growth_parameters.csv.
      - Their unsupported status is documented in TYPESCRIPT_COMPAT_STATUS.md.
    """
    if research_df is None:
        research_df = load_research_parameters()

    # 1. Transform research deliverables (filters to valid TS contract parameters)
    base_parameters = transform_research_dataframe_to_parameters(research_df)

    # 2. Canonical aliases for simulation engine ease-of-use
    canonical_aliases: List[Dict[str, Any]] = [
        {
            "parameter_id": "crew_oxygen_consumption",
            "resource": "oxygen",
            "flow_type": "consumption",
            "value": 0.89,
            "unit": "kg",
            "basis": "per_person",
            "period": {"value": 1, "unit": "day"},
            "classification": "research_data",
            "data_status": "pending_review",
            "source": {
                "title": "Astronaut Mass Balance for Long Duration Missions",
                "url": "https://ntrs.nasa.gov/citations/20190027563",
                "identifier": "NASA NTRS 20190027563 / BVAD Table 4-53",
                "location": "82 kg reference astronaut model incl. 90 min exercise"
            },
            "assumptions": [],
            "caveats": ["Canonical alias for daily_o2_requirement_per_astronaut (simulation-parameter-sheet.md §3.1)"]
        },
        {
            "parameter_id": "crew_co2_production",
            "resource": "co2",
            "flow_type": "production",
            "value": 1.08,
            "unit": "kg",
            "basis": "per_person",
            "period": {"value": 1, "unit": "day"},
            "classification": "research_data",
            "data_status": "pending_review",
            "source": {
                "title": "Astronaut Mass Balance for Long Duration Missions",
                "url": "https://ntrs.nasa.gov/citations/20190027563",
                "identifier": "NASA NTRS 20190027563 / BVAD Table 4-53",
                "location": "82 kg reference astronaut CO₂ production rate"
            },
            "assumptions": [],
            "caveats": ["Canonical alias for daily_co2_production_per_astronaut (simulation-parameter-sheet.md §3.1)"]
        },
        {
            "parameter_id": "crew_water_requirement",
            "resource": "water",
            "flow_type": "requirement",
            "value": 5.03,
            "unit": "kg",
            "basis": "per_person",
            "period": {"value": 1, "unit": "day"},
            "classification": "research_data",
            "data_status": "pending_review",
            "source": {
                "title": "Astronaut Mass Balance for Long Duration Missions",
                "url": "https://ntrs.nasa.gov/citations/20190027563",
                "identifier": "NASA NTRS 20190027563",
                "location": "Total daily water requirement per astronaut (drinking + food preparation + hygiene)"
            },
            "assumptions": [],
            "caveats": [
                "Canonical alias for daily_water_requirement_per_astronaut (simulation-parameter-sheet.md §3.2)",
                "Value includes potable water, food rehydration, and hygiene water"
            ]
        },
        {
            "parameter_id": "crew_food_energy",
            "resource": "food",
            "flow_type": "consumption",
            "value": 3000.0,
            "unit": "kcal",
            "basis": "per_person",
            "period": {"value": 1, "unit": "day"},
            "classification": "research_data",
            "data_status": "pending_review",
            "source": {
                "title": "NASA STEMonstration: Nutrition & ISS Food Systems",
                "url": "https://www.nasa.gov/stem-content/stemonstrations-nutrition",
                "identifier": "NASA STEM Education / Science Friday 2022",
                "location": "Astronaut Caloric Requirements Guidelines"
            },
            "assumptions": [],
            "caveats": [
                "Canonical alias for energy_requirement_per_astronaut (simulation-parameter-sheet.md §3.6)",
                "Mid-point of 2,500–3,500 kcal/day range; actual requirement varies with activity level"
            ]
        },
        {
            "parameter_id": "crew_food_mass",
            "resource": "food",
            "flow_type": "consumption",
            "value": 2.39,
            "unit": "kg",
            "basis": "per_person",
            "period": {"value": 1, "unit": "day"},
            "classification": "research_data",
            "data_status": "pending_review",
            "source": {
                "title": "Astronaut Mass Balance for Long Duration Missions",
                "url": "https://ntrs.nasa.gov/citations/20190027563",
                "identifier": "NASA NTRS 20190027563 / BVAD Table 4-53",
                "location": "Packaged food mass per astronaut per day"
            },
            "assumptions": [],
            "caveats": ["Canonical alias for packaged_food_per_astronaut (simulation-parameter-sheet.md §3.6)"]
        }
    ]

    # Combine: base parameters first, then aliases (if not already present)
    all_params_dict: Dict[str, Dict[str, Any]] = {}
    for p in base_parameters:
        all_params_dict[p["parameter_id"]] = p
    for p in canonical_aliases:
        if p["parameter_id"] not in all_params_dict:
            all_params_dict[p["parameter_id"]] = p

    return list(all_params_dict.values())


def build_schema_1_1_configuration(
    crew_size: int = 4,
    research_df: Optional[pd.DataFrame] = None,
    donki_sep_df: Optional[pd.DataFrame] = None,
    crops_df: Optional[pd.DataFrame] = None,
    radiation_df: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """Build the complete Schema 1.1 configuration dictionary."""
    parameters = build_unified_parameters_list(
        research_df=research_df,
        donki_sep_df=donki_sep_df,
        crops_df=crops_df,
        radiation_df=radiation_df
    )

    config = {
        "schema_version": "1.1",
        "mission": {
            "crew_size": crew_size
        },
        "parameters": parameters
    }

    return config
