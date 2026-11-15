import json

import pandas as pd

from src.mapping.map_donki_events import map_sep_events_to_scenarios


def test_missing_flare_class_does_not_become_nan_or_fake_flare():
    sep_df = pd.DataFrame([
        {
            "message_id": "TEST-001",
            "associated_flare_class": float("nan"),
            "noaa_scale": "S2",
            "estimated_flux_pfu": 100.0,
            "warning_lead_time_minutes": 30.0,
        }
    ])

    scenario = map_sep_events_to_scenarios(sep_df)[0]

    assert scenario["associated_flare_class"] is None
    assert "nan" not in scenario["title"].lower()
    assert "M5.0" not in scenario["title"]

    json.dumps(scenario, allow_nan=False)
