"""Pandas processing module for space crops data combining NASA OSDR OSD-269 with BPC research.

Extracts tabular crop growth cycles, daily water demands, lighting conditions,
and life-support system scaling with full provenance.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd


def build_crop_parameters_dataframe(osd_269_meta: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Build a structured Pandas DataFrame of mission candidate crops."""
    # Base parameters verified against NASA OSDR OSD-269, Wheeler 1996, and Wheeler 2020
    crops_data = [
        {
            "crop_id": "lettuce_veg03a",
            "common_name": "Lettuce (VEG-03A)",
            "scientific_name": "Lactuca sativa",
            "first_harvest_days": 33,
            "harvest_cycle_type": "cut-and-come-again (3 weekly harvests)",
            "water_use_rate_l_m2_d": 2.0,
            "photoperiod_hours_light": 16.0,
            "optimal_temp_c": 23.0,
            "recommended_ppfd_umol_m2_s": 300.0,
            "primary_role": "Fresh micronutrients & vitamins (B1/C supplement)",
            "source": "NASA OSDR OSD-269 & Wheeler 2020 (TM-2020-5008832)",
            "classification": "research reference",
            "origin_type": "measured",
            "v1_safe": True,
            "caveats": "Gross BPC water-use; transpiration is recycled via humidity recovery"
        },
        {
            "crop_id": "dwarf_wheat",
            "common_name": "Dwarf Wheat",
            "scientific_name": "Triticum aestivum",
            "first_harvest_days": 35,
            "harvest_cycle_type": "single harvest (~35d dwarf, 64-86d full)",
            "water_use_rate_l_m2_d": 5.0,
            "photoperiod_hours_light": 20.0,
            "optimal_temp_c": 20.0,
            "recommended_ppfd_umol_m2_s": 800.0,
            "primary_role": "Calorie staple & carbohydrate bulk",
            "source": "NASA BPC (Wheeler 1996) & Wheeler 2020 Table 2",
            "classification": "research reference",
            "origin_type": "measured",
            "v1_safe": True,
            "caveats": "High lighting power requirement; requires closed-loop humidity capture"
        },
        {
            "crop_id": "soybean",
            "common_name": "Soybean",
            "scientific_name": "Glycine max",
            "first_harvest_days": 90,
            "harvest_cycle_type": "single harvest (90-97 days)",
            "water_use_rate_l_m2_d": 5.0,
            "photoperiod_hours_light": 12.0,
            "optimal_temp_c": 23.0,
            "recommended_ppfd_umol_m2_s": 600.0,
            "primary_role": "Protein & essential lipid supplement",
            "source": "NASA BPC (Wheeler 1996) & Wheeler 2020 Table 2",
            "classification": "research reference",
            "origin_type": "measured",
            "v1_safe": True,
            "caveats": "Long growth cycle; sensitive to lighting failure"
        },
        {
            "crop_id": "microgreens",
            "common_name": "Microgreens / Sprouts",
            "scientific_name": "Mixed cultivars",
            "first_harvest_days": 10,
            "harvest_cycle_type": "rapid rotation (7-14 days)",
            "water_use_rate_l_m2_d": 1.5,
            "photoperiod_hours_light": 14.0,
            "optimal_temp_c": 22.0,
            "recommended_ppfd_umol_m2_s": 150.0,
            "primary_role": "Rapid morale boost & early vitamin availability",
            "source": "NASA Horticultural candidate & Wheeler research",
            "classification": "research reference",
            "origin_type": "modelled",
            "v1_safe": True,
            "caveats": "Low calorie yield; acts strictly as fresh supplement"
        }
    ]

    df = pd.DataFrame(crops_data)

    # If OSDR metadata was supplied, verify study accession consistency
    if osd_269_meta:
        study_info = osd_269_meta.get("study", {}).get("OSD-269", {}).get("studies", [{}])[0]
        if study_info.get("identifier") == "OSD-269":
            # Add corroboration flag
            df["osdr_verified"] = True

    return df


def calculate_crew_crop_demands(
    crop_df: pd.DataFrame,
    crew_size: int = 4,
    allocated_crop_area_m2: float = 20.0
) -> pd.DataFrame:
    """Calculate daily water demands and area metrics for the mission crew."""
    df_calc = crop_df.copy()

    # Total daily water use (L/day = kg/day) = rate * area
    df_calc["allocated_area_m2"] = allocated_crop_area_m2
    df_calc["daily_water_demand_kg"] = df_calc["water_use_rate_l_m2_d"] * allocated_crop_area_m2
    df_calc["crew_size"] = crew_size

    # Vegetative area reference from Wheeler (40-50 m2/person for 100% vegetarian diet)
    df_calc["full_diet_area_m2_4crew"] = 45.0 * crew_size
    df_calc["food_supplement_fraction"] = round(allocated_crop_area_m2 / (45.0 * crew_size), 3)

    return df_calc


def save_processed_crop_parameters(df: pd.DataFrame, output_path: Optional[Path] = None) -> Path:
    """Save processed crop parameters to CSV."""
    if output_path is None:
        project_root = Path(__file__).resolve().parents[2]
        output_path = project_root / "data" / "processed" / "crop_growth_parameters.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    from src.ingestion.ingest_osdr_bio import fetch_osd_study_metadata

    meta = fetch_osd_study_metadata(269)
    df = build_crop_parameters_dataframe(meta)
    df_demands = calculate_crew_crop_demands(df, crew_size=4, allocated_crop_area_m2=20.0)
    out_file = save_processed_crop_parameters(df_demands)

    print(f"Processed {len(df_demands)} crop varieties.")
    print(f"Saved to: {out_file}")
    print("\nCrop Parameters Table:")
    print(df_demands[["crop_id", "first_harvest_days", "water_use_rate_l_m2_d", "daily_water_demand_kg", "food_supplement_fraction"]])

