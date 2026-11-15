"""Python-side TypeScript contract compatibility tests.

STATUS: PENDING TYPESCRIPT RUNTIME VERIFICATION
========================================================
The TypeScript simulation engine source code, its runtime validator, and its
configuration loader are not available in this repository.

What these tests DO:
  - Enforce the documented SimulationParameter contract structure (field names,
    types, enum values) as described in README_FOR_TYPESCRIPT_DEV.md and
    TYPESCRIPT_COMPAT_STATUS.md.
  - Confirm that every parameter in mission_config.json conforms to that
    documented contract before it is handed to the TypeScript developer.
  - Validate the config against the Python-side JSON Schema (schemas/mission_config_schema.json),
    which mirrors the documented TypeScript interface.

What these tests do NOT do:
  - Execute or import any TypeScript code.
  - Run the TypeScript runtime validator.
  - Guarantee that the TypeScript engine will accept the generated config.
  - Substitute for confirmation from the TypeScript developer.

Required action before claiming full TypeScript compatibility:
  The TypeScript developer must either:
    (a) Confirm that the SimulationParameter interface matches what is documented
        in README_FOR_TYPESCRIPT_DEV.md and TYPESCRIPT_COMPAT_STATUS.md, OR
    (b) Provide the actual TypeScript interface/validator so a live integration
        test can be added here.

See TYPESCRIPT_COMPAT_STATUS.md at the project root for the full status.
"""

import json
import math
from pathlib import Path
import pytest
import jsonschema

# ---------------------------------------------------------------------------
# TypeScript contract field definitions
# (Mirrored from the documented SimulationParameter interface.
#  These values must be confirmed by the TypeScript developer before
#  claiming full runtime compatibility.)
# ---------------------------------------------------------------------------

TS_FLOW_TYPES = frozenset({
    "consumption", "production", "generation",
    "removal", "recovery", "loss", "capacity", "requirement"
})

TS_CLASSIFICATIONS = frozenset({
    "research_data", "engineering_inference", "gameplay_assumption"
})

TS_DATA_STATUSES = frozenset({
    "validated", "pending_review", "mock", "TBD"
})

TS_RESOURCES = frozenset({
    "oxygen", "co2", "water", "food", "radiation", "power", "crew", "general"
})

TS_PERIOD_UNITS = frozenset({"second", "minute", "hour", "day", "cycle"})

TS_PER_TIME_PERIOD_UNITS = frozenset({"hour", "day", "cycle"})

TS_BASIS_VALUES = frozenset({
    "per_person", "per_equipment", "per_cycle", "per_time", "total"
})

TS_REGISTRY_UNITS = frozenset({
    "kg", "g", "L", "mL", "kcal", "Wh", "kWh", "W", "kW",
    "kg/day", "kg/cycle", "L/day", "Wh/cycle", "kWh/cycle",
    "kg/m3", "ppm", "percent"
})

TS_REQUIRED_FIELDS = frozenset({
    "parameter_id", "flow_type",
    "value", "basis", "unit",
    "classification", "data_status", "source",
    "assumptions", "caveats"
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_generated_config() -> dict:
    """Load the most recent generated mission_config.json."""
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "outputs" / "mission_config.json"
    if not config_path.exists():
        pytest.skip("mission_config.json not found — run the pipeline first (python main.py)")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_schema() -> dict:
    project_root = Path(__file__).resolve().parents[1]
    schema_path = project_root / "schemas" / "mission_config_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_params() -> list:
    return _load_generated_config()["parameters"]


# ---------------------------------------------------------------------------
# Schema-level tests
# ---------------------------------------------------------------------------

class TestSchemaStructure:
    """Validate the top-level mission_config.json structure."""

    def test_schema_version(self):
        config = _load_generated_config()
        assert config["schema_version"] == "1.1"

    def test_mission_crew_size(self):
        config = _load_generated_config()
        assert isinstance(config["mission"]["crew_size"], int)
        assert config["mission"]["crew_size"] >= 1

    def test_parameters_is_list(self):
        config = _load_generated_config()
        assert isinstance(config["parameters"], list)
        assert len(config["parameters"]) == 28

    def test_jsonschema_validation_passes(self):
        """The generated config must pass the Python-side JSON Schema."""
        config = _load_generated_config()
        schema = _load_schema()
        jsonschema.validate(instance=config, schema=schema)


# ---------------------------------------------------------------------------
# Parameter-level contract tests
# ---------------------------------------------------------------------------

class TestRequiredFields:
    """Every parameter must have all TypeScript contract required fields."""

    def test_all_required_fields_present(self):
        params = _load_params()
        for p in params:
            pid = p.get("parameter_id", "<unknown>")
            missing = TS_REQUIRED_FIELDS - set(p.keys())
            assert not missing, (
                f"Parameter '{pid}' missing required TypeScript fields: {missing}"
            )

    def test_parameter_id_is_nonempty_string(self):
        params = _load_params()
        for p in params:
            assert isinstance(p["parameter_id"], str) and p["parameter_id"].strip(), (
                f"parameter_id must be a non-empty string, got: {p['parameter_id']!r}"
            )


class TestEnumValues:
    """Enum fields must only use values supported by the TypeScript contract."""

    def test_flow_type_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["flow_type"] in TS_FLOW_TYPES, (
                f"Parameter '{pid}': flow_type '{p['flow_type']}' not in TS contract enum. "
                f"Unsupported values: environment, infrastructure, storage, specification"
            )

    def test_classification_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["classification"] in TS_CLASSIFICATIONS, (
                f"Parameter '{pid}': classification '{p['classification']}' not in TS contract enum"
            )

    def test_data_status_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["data_status"] in TS_DATA_STATUSES, (
                f"Parameter '{pid}': data_status '{p['data_status']}' not in TS contract enum. "
                f"'research_reference', 'derived', 'tbd' are not valid — use 'pending_review'/'TBD'"
            )

    def test_resource_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["resource"] in TS_RESOURCES, (
                f"Parameter '{pid}': resource '{p['resource']}' not in TS contract enum"
            )

    def test_period_unit_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            if p.get("basis") == "per_time":
                assert "period" in p and isinstance(p["period"], dict), (
                    f"Parameter '{pid}': basis 'per_time' requires a 'period' object"
                )
                assert p["period"]["unit"] in TS_PER_TIME_PERIOD_UNITS, (
                    f"Parameter '{pid}': period.unit for per_time must be in {TS_PER_TIME_PERIOD_UNITS}, got '{p['period']['unit']}'"
                )
            elif "period" in p and p["period"] is not None:
                pu = p["period"]["unit"]
                assert pu in TS_PERIOD_UNITS, (
                    f"Parameter '{pid}': period.unit '{pu}' not in TS contract enum"
                )

    def test_unit_registry_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["unit"] in TS_REGISTRY_UNITS, (
                f"Parameter '{pid}': unit '{p['unit']}' not in 17-unit TS registry"
            )

    def test_basis_enum(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["basis"] in TS_BASIS_VALUES, (
                f"Parameter '{pid}': basis '{p['basis']}' not in allowed values"
            )


class TestDataTypes:
    """Field types must match the TypeScript interface."""

    def test_value_is_finite_non_negative_number(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            v = p["value"]
            assert isinstance(v, (int, float)) and not isinstance(v, bool), (
                f"Parameter '{pid}': value must be a number, got {type(v).__name__}"
            )
            assert v >= 0, f"Parameter '{pid}': value must be non-negative, got {v}"

    def test_value_not_nan(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            v = p["value"]
            if isinstance(v, float):
                assert not math.isnan(v), f"Parameter '{pid}': value is NaN"

    def test_value_not_infinity(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            v = p["value"]
            if isinstance(v, float):
                assert not math.isinf(v), f"Parameter '{pid}': value is Infinity"

    def test_assumptions_is_list_of_strings(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert isinstance(p["assumptions"], list), (
                f"Parameter '{pid}': assumptions must be list"
            )
            for item in p["assumptions"]:
                assert isinstance(item, str), (
                    f"Parameter '{pid}': each assumption must be a string, got {type(item)}"
                )

    def test_caveats_is_list_of_strings(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert isinstance(p["caveats"], list), (
                f"Parameter '{pid}': caveats must be list"
            )
            for item in p["caveats"]:
                assert isinstance(item, str), (
                    f"Parameter '{pid}': each caveat must be a string, got {type(item)}"
                )

    def test_period_has_positive_value(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            if "period" in p and p["period"] is not None:
                assert p["period"]["value"] > 0, (
                    f"Parameter '{pid}': period.value must be positive"
                )

    def test_unit_is_nonempty_string(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert isinstance(p["unit"], str) and p["unit"].strip(), (
                f"Parameter '{pid}': unit must be a non-empty string"
            )


class TestSourceStructure:
    """Source must be a structured object or null — not a plain string."""

    def test_source_is_dict_or_null(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            src = p["source"]
            assert src is None or isinstance(src, dict), (
                f"Parameter '{pid}': source must be a structured dict or null, "
                f"got {type(src).__name__} = {src!r}. Plain strings are not accepted."
            )

    def test_source_dict_has_title(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            src = p["source"]
            if isinstance(src, dict):
                assert "title" in src and src["title"], (
                    f"Parameter '{pid}': source dict must have a non-empty 'title'"
                )

    def test_source_dict_no_extra_keys(self):
        allowed_source_keys = {"title", "url", "identifier", "location"}
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            src = p["source"]
            if isinstance(src, dict):
                extra = set(src.keys()) - allowed_source_keys
                assert not extra, (
                    f"Parameter '{pid}': source dict has unexpected keys: {extra}"
                )

    def test_source_url_is_string_or_null(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            src = p["source"]
            if isinstance(src, dict) and "url" in src:
                assert src["url"] is None or isinstance(src["url"], str), (
                    f"Parameter '{pid}': source.url must be string or null"
                )


class TestNegativeValues:
    """Resources that cannot be negative must not have negative values."""

    _CANNOT_BE_NEGATIVE = {
        "oxygen", "water", "food", "power"
    }

    def test_non_negative_resources(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            v = p["value"]
            if v is not None and p["resource"] in self._CANNOT_BE_NEGATIVE:
                assert v >= 0, (
                    f"Parameter '{pid}': resource '{p['resource']}' value must not be negative, got {v}"
                )


class TestTBDValues:
    """TBD parameters with unresolved values are omitted from mission_config.json,
    and all parameters in mission_config.json have valid non-null numbers.
    """

    def test_no_null_values_in_config(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["value"] is not None, (
                f"Parameter '{pid}': value must not be null in mission_config.json"
            )

    def test_null_value_has_appropriate_status(self):
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            if p["value"] is None:
                assert p["data_status"] in {"TBD", "pending_review"}, (
                    f"Parameter '{pid}': null value must have data_status 'TBD' or 'pending_review', "
                    f"got '{p['data_status']}'"
                )


class TestProvenance:
    """Scientific provenance must be preserved — no silently removed caveats."""

    def test_radiation_gcr_has_caveats(self):
        """GCR measurements must carry caveats about not being human effective dose."""
        params = _load_params()
        params_by_id = {p["parameter_id"]: p for p in params}
        if "lunar_surface_gcr_dose_equivalent" in params_by_id:
            p = params_by_id["lunar_surface_gcr_dose_equivalent"]
            assert len(p["caveats"]) > 0, (
                "lunar_surface_gcr_dose_equivalent must carry caveats explaining "
                "it is an environmental reference, not a human effective dose"
            )

    def test_spe_proton_flux_has_caveats(self):
        """SPE peak proton flux must carry caveats about not being directly convertible to dose."""
        params = _load_params()
        params_by_id = {p["parameter_id"]: p for p in params}
        if "spe_peak_proton_flux" in params_by_id:
            p = params_by_id["spe_peak_proton_flux"]
            assert len(p["caveats"]) > 0, (
                "spe_peak_proton_flux must carry caveats about pfu-to-dose conversion requirements"
            )

    def test_no_parameter_missing_source_when_known(self):
        """Parameters derived from known NASA sources must not have null source."""
        params = _load_params()
        # These parameter IDs are known to have traceable NASA sources
        known_sourced = {
            "daily_o2_requirement_per_astronaut",
            "daily_co2_production_per_astronaut",
            "daily_water_requirement_per_astronaut",
            "packaged_food_per_astronaut",
            "lunar_surface_gcr_dose_equivalent",
            "spe_solar_particle_warning_time",
            "crop_growth_time_lettuce_veg03a",
        }
        params_by_id = {p["parameter_id"]: p for p in params}
        for pid in known_sourced:
            if pid in params_by_id:
                assert params_by_id[pid]["source"] is not None, (
                    f"Parameter '{pid}' has a known NASA source but source is null"
                )

    def test_research_data_not_marked_gameplay(self):
        """NASA-measured values must not be classified as gameplay_assumption."""
        params = _load_params()
        # These are physical measurements that must remain research_data
        strictly_research = {
            "lunar_surface_gcr_dose_equivalent",
            "spe_peak_proton_flux",
            "daily_o2_requirement_per_astronaut",
            "daily_co2_production_per_astronaut",
        }
        params_by_id = {p["parameter_id"]: p for p in params}
        for pid in strictly_research:
            if pid in params_by_id:
                p = params_by_id[pid]
                assert p["classification"] != "gameplay_assumption", (
                    f"Parameter '{pid}' is a research measurement and must not be "
                    f"classified as 'gameplay_assumption'"
                )


class TestFlowTypeSemantic:
    """Key parameters must have semantically correct flow types."""

    def test_o2_consumption_flow(self):
        params_by_id = {p["parameter_id"]: p for p in _load_params()}
        if "daily_o2_requirement_per_astronaut" in params_by_id:
            # "requirement" is semantically correct for the daily O2 requirement parameter.
            # The per-minute consumption rates (sleeping_o2_consumption, etc.) correctly use "consumption".
            assert params_by_id["daily_o2_requirement_per_astronaut"]["flow_type"] in {
                "consumption", "requirement"
            }, "daily_o2_requirement_per_astronaut must be 'consumption' or 'requirement'"

    def test_co2_production_flow(self):
        params_by_id = {p["parameter_id"]: p for p in _load_params()}
        if "daily_co2_production_per_astronaut" in params_by_id:
            assert params_by_id["daily_co2_production_per_astronaut"]["flow_type"] == "production"

    def test_gcr_dose_loss_flow(self):
        """GCR radiation represents a continuous loss (cumulative energy deposition)."""
        params_by_id = {p["parameter_id"]: p for p in _load_params()}
        if "lunar_surface_gcr_dose_equivalent" in params_by_id:
            assert params_by_id["lunar_surface_gcr_dose_equivalent"]["flow_type"] == "loss", (
                "GCR dose is an environmental loss, not 'environment' (not a valid TS enum)"
            )

    def test_no_invalid_flow_types(self):
        """Legacy flow types that are not in the TypeScript enum must not appear."""
        invalid_legacy_types = {"environment", "infrastructure", "storage", "specification"}
        params = _load_params()
        for p in params:
            pid = p["parameter_id"]
            assert p["flow_type"] not in invalid_legacy_types, (
                f"Parameter '{pid}': flow_type '{p['flow_type']}' is a legacy value "
                f"not supported by the TypeScript runtime validator"
            )


# ---------------------------------------------------------------------------
# PENDING: TypeScript runtime integration test
# ---------------------------------------------------------------------------
# TypeScript runtime verification is NOT complete.
# The TypeScript simulation engine source code and its runtime validator
# are not available in this repository.
#
# When the TypeScript developer provides the engine or confirms the contract,
# add a live integration test here. Example shape:
#
#   def test_typescript_runtime_validation():
#       """Validate the generated config using the actual TypeScript runtime validator.
#
#       PREREQUISITE: TypeScript developer must confirm validator CLI entrypoint.
#       """
#       import subprocess
#       result = subprocess.run(
#           ["npx", "ts-node", "src/validateConfig.ts", "outputs/mission_config.json"],
#           cwd=Path(__file__).resolve().parents[1] / "lunaRanger",
#           capture_output=True, text=True
#       )
#       assert result.returncode == 0, (
#           f"TypeScript validator rejected config:\n{result.stdout}\n{result.stderr}"
#       )
#
# Until that test is added and passes, TypeScript runtime compatibility is
# PENDING VERIFICATION. See TYPESCRIPT_COMPAT_STATUS.md for the checklist.
# ---------------------------------------------------------------------------
