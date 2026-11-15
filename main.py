"""Junior Astronaut Mission Trainer — Python Data & Science Layer Pipeline.

Executes end-to-end:
1. Ingests research deliverables (simulation-parameter-sheet.md, resource-dependency-matrix.md)
   along with NASA DONKI, NASA OSDR Bio (OSD-269), and NASA OSDR RadLab telemetry
2. Cleans & transforms data using Pandas
3. Validates fields, types, units, and physical/astrophysical constraints
4. Maps datasets to Schema 1.1 format
5. Generates the authoritative mission_config.json for the TypeScript simulation engine
6. Runs scientific reference models and outputs expected calculation fixtures
"""

import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion.load_research_deliverables import load_research_parameters, load_dependency_matrix_edges
from src.ingestion.ingest_donki import fetch_donki_notifications
from src.ingestion.ingest_osdr_bio import fetch_osd_study_metadata
from src.ingestion.ingest_radlab import fetch_radlab_telemetry

from src.processing.process_donki import (
    parse_donki_notifications,
    clean_donki_events,
    filter_sep_scenarios,
    save_processed_donki_events
)
from src.processing.process_osdr_crops import (
    build_crop_parameters_dataframe,
    calculate_crew_crop_demands,
    save_processed_crop_parameters
)
from src.processing.process_radiation import (
    process_radlab_telemetry,
    save_processed_radiation_parameters
)

from src.validation.validate_donki import validate_donki_dataframe
from src.validation.validate_osdr_crops import validate_crop_dataframe
from src.validation.validate_radiation import validate_radiation_dataframe

from src.mapping.dataset_adapter import build_schema_1_1_configuration
from src.mapping.map_donki_events import map_sep_events_to_scenarios
from src.configuration.config_generator import validate_and_save_mission_config

from src.testing_scenarios.generate_test_cases import generate_radiation_validation_fixtures
from src.testing_scenarios.life_support_scenarios import generate_life_support_validation_fixtures


def run_pipeline(crew_size: int = 4) -> Path:
    """Execute the full data pipeline producing Schema 1.1 mission_config.json."""
    print("=" * 70)
    print("  JUNIOR ASTRONAUT MISSION TRAINER — PYTHON DATA & SCIENCE LAYER")
    print("=" * 70)

    # 1. Ingestion
    print("\n[1/5] Ingesting Research Deliverables & NASA Datasets...")
    research_df = load_research_parameters()
    edges_df = load_dependency_matrix_edges()
    print(f"  ✓ Research parameter sheet parsed: {len(research_df)} parameters")
    print(f"  ✓ Resource dependency matrix parsed: {len(edges_df)} dependency edges")

    donki_raw = fetch_donki_notifications()
    print(f"  ✓ NASA DONKI notifications retrieved: {len(donki_raw)} records")

    osdr_meta = fetch_osd_study_metadata(269)
    print("  ✓ NASA OSDR Bio (OSD-269) metadata retrieved")

    radlab_raw = fetch_radlab_telemetry()
    print(f"  ✓ NASA OSDR RadLab telemetry retrieved: {len(radlab_raw)} records")

    # 2. Pandas Processing
    print("\n[2/5] Cleaning & Transforming Data (Pandas)...")
    donki_df = clean_donki_events(parse_donki_notifications(donki_raw))
    donki_seps = filter_sep_scenarios(donki_df)
    save_processed_donki_events(donki_df)
    print(f"  ✓ Processed {len(donki_df)} space weather events ({len(donki_seps)} SEP emergency scenarios)")

    crops_df = build_crop_parameters_dataframe(osdr_meta)
    crops_df = calculate_crew_crop_demands(crops_df, crew_size=crew_size, allocated_crop_area_m2=20.0)
    save_processed_crop_parameters(crops_df)
    print(f"  ✓ Processed {len(crops_df)} space crop candidates (20m² allocated area)")

    rad_df = process_radlab_telemetry(radlab_raw)
    save_processed_radiation_parameters(rad_df)
    print(f"  ✓ Processed lunar radiation parameters (GCR rate: {rad_df.iloc[0]['daily_gcr_dose_msv']} mSv/day)")

    # 3. Scientific Validation
    print("\n[3/5] Validating Data Integrity & Scientific Constraints...")
    donki_errs = validate_donki_dataframe(donki_df)
    if donki_errs:
        raise ValueError(f"DONKI validation failed: {donki_errs}")
    print("  ✓ DONKI space weather dataset passed validation")

    crop_errs = validate_crop_dataframe(crops_df)
    if crop_errs:
        raise ValueError(f"Crop validation failed: {crop_errs}")
    print("  ✓ Space crop parameters passed validation")

    rad_errs = validate_radiation_dataframe(rad_df)
    if rad_errs:
        raise ValueError(f"Radiation validation failed: {rad_errs}")
    print("  ✓ Radiation dosimetry passed validation")

    # 4. Schema Mapping & Configuration Generation (Schema 1.1)
    print("\n[4/5] Mapping to Schema 1.1 & Emitting mission_config.json...")
    config_data = build_schema_1_1_configuration(
        crew_size=crew_size,
        research_df=research_df,
        donki_sep_df=donki_seps,
        crops_df=crops_df,
        radiation_df=rad_df
    )
    config_file = validate_and_save_mission_config(config_data)
    print(f"  ✓ Validated mission_config.json generated (Schema 1.1): {config_file}")
    print(f"  ✓ Total parameters in configuration: {len(config_data['parameters'])}")

    # Save mapped emergency scenarios for simulation engine
    scenarios = map_sep_events_to_scenarios(donki_seps)
    scenarios_path = PROJECT_ROOT / "outputs" / "emergency_scenarios.json"
    with open(scenarios_path, "w", encoding="utf-8") as f:
        json.dump({"scenarios": scenarios}, f, indent=2, allow_nan=False)
    print(f"  ✓ Emergency scenarios generated ({len(scenarios)} events): {scenarios_path}")

    # 5. Scientific Reference Models & Validation Test Cases
    print("\n[5/5] Generating Expected Calculations & Test Fixtures...")
    rad_fixtures = generate_radiation_validation_fixtures(donki_seps)
    print(f"  ✓ Radiation expected calculation fixtures: {rad_fixtures}")

    ls_fixtures = generate_life_support_validation_fixtures()
    print(f"  ✓ Life support expected calculation fixtures: {ls_fixtures}")

    print("\n" + "=" * 70)
    print("  PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return config_file


if __name__ == "__main__":
    run_pipeline()
