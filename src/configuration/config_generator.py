"""Configuration generator producing validated mission_config.json for the TypeScript Simulation Engine."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import jsonschema


def validate_and_save_mission_config(
    config_data: Dict[str, Any],
    schema_path: Optional[Path] = None,
    output_path: Optional[Path] = None
) -> Path:
    """Validate configuration dictionary against JSON schema and save to outputs/."""
    project_root = Path(__file__).resolve().parents[2]

    if schema_path is None:
        schema_path = project_root / "schemas" / "mission_config_schema.json"
    if output_path is None:
        output_path = project_root / "outputs" / "mission_config.json"

    # 1. Load schema
    if not schema_path.exists():
        raise FileNotFoundError(f"Configuration schema not found at: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # 2. Validate using jsonschema
    jsonschema.validate(instance=config_data, schema=schema)

    # 3. Save validated configuration
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    return output_path

