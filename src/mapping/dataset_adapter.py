"""Dataset Adapter mapping research deliverables and NASA API datasets to Schema 1.1.

Produces the exact format required by the simulation engine:
{
  "schema_version": "1.1",
  "mission": {
    "crew_size": 4
  },
  "parameters": [...]
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
    """Assemble all parameters from research deliverables and NASA APIs into a unified list."""
    if research_df is None:
        research_df = load_research_parameters()

    # 1. Transform research deliverables
    base_parameters = transform_research_dataframe_to_parameters(research_df)

    # 2. Add high-value live NASA API telemetry parameters
    api_parameters = []

    # RadLab GCR dosimetry
    if radiation_df is not None and not radiation_df.empty:
        rad_row = radiation_df.iloc[0]
        api_parameters.append({
            "parameter_id": "lunar_surface_gcr_dose_equivalent",
            "resource": "radiation",
            "flow_type": "environment",
            "value_per_person": float(rad_row.get("daily_gcr_dose_msv", 1.37)),
            "raw_value": "1.37",
            "unit": "mSv/day",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": str(rad_row.get("source", "NASA OSDR RadLab & Chang'e-4")),
            "assumptions": ["Surface detector telemetry; biological tissue dose requires model weighting"],
            "notes": "Chang'e-4 derived GCR dose-equivalent rate on lunar surface"
        })

    # DONKI Solar Particle Event parameters
    if donki_sep_df is not None and not donki_sep_df.empty:
        sep_row = donki_sep_df.iloc[0]
        spe_lead_time = float(sep_row.get("warning_lead_time_minutes") or 30.0)
        if spe_lead_time < 15.0:
            spe_lead_time = 30.0
        api_parameters.append({
            "parameter_id": "spe_solar_particle_warning_time",
            "resource": "radiation",
            "flow_type": "environment",
            "value_per_person": spe_lead_time,
            "raw_value": str(spe_lead_time),
            "unit": "minute",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA CCMC DONKI (api.nasa.gov/DONKI)",
            "assumptions": ["Lead time from flare observation to energetic proton arrival at near-Earth/Moon"],
            "notes": f"DONKI historical SPE warning lead time (Associated flare: {sep_row.get('associated_flare_class', 'X-class')})"
        })
        api_parameters.append({
            "parameter_id": "spe_peak_proton_flux",
            "resource": "radiation",
            "flow_type": "environment",
            "value_per_person": float(sep_row.get("estimated_flux_pfu", 1000.0)),
            "raw_value": str(sep_row.get("estimated_flux_pfu", 1000.0)),
            "unit": "pfu",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA CCMC DONKI",
            "assumptions": [">10 MeV solar proton flux exceeding threshold"],
            "notes": f"Historical solar proton event flux ({sep_row.get('noaa_scale', 'S3')} scale)"
        })

    # OSDR Crop Parameters
    if crops_df is not None and not crops_df.empty:
        for _, crop in crops_df.iterrows():
            cid = crop["crop_id"]
            pid = f"crop_growth_time_{cid}" if cid == "lettuce_veg03a" else f"flight_crop_growth_time_{cid}"
            api_parameters.append({
                "parameter_id": pid,
                "resource": "food",
                "flow_type": "infrastructure",
                "value_per_person": float(crop["first_harvest_days"]),
                "raw_value": str(crop["first_harvest_days"]),
                "unit": "day",
                "period": {"value": 1, "unit": "day"},
                "data_status": str(crop.get("classification", "research reference")).lower().replace(" ", "_"),
                "source": str(crop.get("source")),
                "assumptions": [str(crop.get("caveats", ""))[:150]],
                "notes": f"{crop['common_name']} first harvest cycle ({crop['harvest_cycle_type']})"
            })

    # Canonical aliases mapping directly to research deliverables values
    canonical_aliases = [
        {
            "parameter_id": "crew_oxygen_consumption",
            "resource": "oxygen",
            "flow_type": "consumption",
            "value_per_person": 0.89,
            "raw_value": "~0.89",
            "unit": "kg/person/day",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA reference astronaut model (82 kg astronaut, incl. 90 min exercise)",
            "assumptions": [],
            "notes": "Core alias for daily_o2_requirement_per_astronaut from simulation-parameter-sheet.md §3.1"
        },
        {
            "parameter_id": "crew_co2_production",
            "resource": "co2",
            "flow_type": "production",
            "value_per_person": 1.08,
            "raw_value": "~1.08",
            "unit": "kg/person/day",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA reference astronaut model",
            "assumptions": [],
            "notes": "Core alias for daily_co2_production_per_astronaut from simulation-parameter-sheet.md §3.1"
        },
        {
            "parameter_id": "crew_water_requirement",
            "resource": "water",
            "flow_type": "consumption",
            "value_per_person": 5.03,
            "raw_value": "~5.03",
            "unit": "kg/person/day (≈ L/person/day)",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA 2019 mass-balance study",
            "assumptions": [],
            "notes": "Core alias for daily_water_requirement_per_astronaut from simulation-parameter-sheet.md §3.2"
        },
        {
            "parameter_id": "crew_food_energy",
            "resource": "food",
            "flow_type": "consumption",
            "value_per_person": 3000.0,
            "raw_value": "~2,500–3,500",
            "unit": "kcal/person/day",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "NASA STEMonstration: Nutrition (2018); Science Friday (2022)",
            "assumptions": [],
            "notes": "Core alias for energy_requirement_per_astronaut from simulation-parameter-sheet.md §3.6"
        },
        {
            "parameter_id": "crew_food_mass",
            "resource": "food",
            "flow_type": "consumption",
            "value_per_person": 2.39,
            "raw_value": "2.39",
            "unit": "kg/person/day",
            "period": {"value": 1, "unit": "day"},
            "data_status": "research_reference",
            "source": "Ewert 2019 (NASA, NTRS 20190027563) citing NASA BVAD Table 4-53",
            "assumptions": [],
            "notes": "Core alias for packaged_food_per_astronaut from simulation-parameter-sheet.md §3.6"
        }
    ]

    # Combine: base research parameters take precedence, then API parameters, then canonical aliases
    all_params_dict = {}
    for p in base_parameters:
        all_params_dict[p["parameter_id"]] = p
    for p in api_parameters:
        all_params_dict[p["parameter_id"]] = p
    for p in canonical_aliases:
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
