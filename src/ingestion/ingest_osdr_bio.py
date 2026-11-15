"""Ingestion module for NASA Open Science Data Repository (OSDR) Bio studies.

Fetches and caches metadata and study file manifests for space biology investigations
(primary target: study OSD-269 / VEG-03A lettuce).
"""

import json
import ssl
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional


OSDR_META_URL = "https://osdr.nasa.gov/osdr/data/osd/meta"
OSDR_FILES_URL = "https://osdr.nasa.gov/osdr/data/osd/files"


def fetch_osd_study_metadata(
    study_id: int = 269,
    timeout: int = 15,
    raw_cache_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Fetch study metadata from OSDR with local disk caching."""
    if raw_cache_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        raw_cache_dir = project_root / "data" / "raw" / "osdr" / f"OSD-{study_id}"
    raw_cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = raw_cache_dir / f"OSD_{study_id}_metadata.json"

    url = f"{OSDR_META_URL}/{study_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "JuniorAstronautMissionTrainer/1.0"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return data
    except Exception as exc:
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        raise RuntimeError(f"Failed to fetch OSDR metadata and no cache found at {cache_file}: {exc}") from exc


def fetch_osd_study_files(
    study_id: int = 269,
    timeout: int = 15,
    raw_cache_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """Fetch study files manifest from OSDR with local disk caching."""
    if raw_cache_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        raw_cache_dir = project_root / "data" / "raw" / "osdr" / f"OSD-{study_id}"
    raw_cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = raw_cache_dir / f"OSD_{study_id}_files.json"

    url = f"{OSDR_FILES_URL}/{study_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "JuniorAstronautMissionTrainer/1.0"})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return data
    except Exception as exc:
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        raise RuntimeError(f"Failed to fetch OSDR files and no cache found at {cache_file}: {exc}") from exc


if __name__ == "__main__":
    meta = fetch_osd_study_metadata(269)
    files = fetch_osd_study_files(269)
    print("OSD-269 Metadata retrieved:", meta.get("study", {}).get("OSD-269", {}).get("studies", [{}])[0].get("title"))
    print("OSD-269 Files count:", len(files.get("studies", {}).get("OSD-269", {}).get("study_files", [])))

