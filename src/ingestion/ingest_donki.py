"""Ingestion client for NASA CCMC DONKI Space Weather notifications and events.

Provides fetching with automated raw data caching for offline reproducibility.
"""

import json
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


DONKI_NOTIFICATIONS_URL = "https://api.nasa.gov/DONKI/notifications"


def fetch_donki_notifications(
    start_date: str = "2024-05-01",
    end_date: str = "2024-05-15",
    event_type: str = "all",
    api_key: str = "DEMO_KEY",
    timeout: int = 20,
    raw_cache_dir: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Fetch space weather notifications from NASA DONKI.

    Falls back to cached JSON if network is unreachable.
    """
    if raw_cache_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        raw_cache_dir = project_root / "data" / "raw" / "donki"
    raw_cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = raw_cache_dir / f"donki_notifications_{start_date}_{end_date}_{event_type}.json"

    # Try live fetch
    url = f"{DONKI_NOTIFICATIONS_URL}?startDate={start_date}&endDate={end_date}&type={event_type}&api_key={api_key}"
    req = urllib.request.Request(url, headers={"User-Agent": "JuniorAstronautMissionTrainer/1.0"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                # Save raw payload for reproducibility & offline use
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                return data
    except Exception as exc:
        # Fallback to cache if available
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        raise RuntimeError(f"Failed to fetch DONKI data and no cache found at {cache_file}: {exc}") from exc

    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


if __name__ == "__main__":
    records = fetch_donki_notifications()
    print(f"Retrieved {len(records)} DONKI notifications.")

