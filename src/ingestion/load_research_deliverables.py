"""Ingestion module to parse Markdown research deliverables into Pandas DataFrames.

Parses:
- simulation-parameter-sheet.md (§3 Master Parameter Table + §4 Per-Parameter Detail)
- resource-dependency-matrix.md (§4 Dependency Edges)
"""

from pathlib import Path
import re
from typing import Dict, List, Optional
import pandas as pd


def _parse_single_markdown_table(lines: List[str]) -> pd.DataFrame:
    """Parse a list of pipe-delimited Markdown table lines into a DataFrame."""
    header = [c.strip() for c in lines[0].split("|")[1:-1]]
    rows = []
    for line in lines[2:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cols = [c.strip() for c in stripped.split("|")[1:-1]]
        if len(cols) == len(header):
            rows.append(cols)
        elif len(cols) > len(header):
            rows.append(cols[:len(header)])
        else:
            rows.append(cols + [""] * (len(header) - len(cols)))
    return pd.DataFrame(rows, columns=header)


def extract_markdown_tables(file_path: Path) -> List[pd.DataFrame]:
    """Extract all Markdown tables in a file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    table_blocks = []
    current_block = []

    for line in text.splitlines():
        if line.strip().startswith("|"):
            current_block.append(line)
        else:
            if len(current_block) >= 3:
                table_blocks.append(current_block)
            current_block = []
    if len(current_block) >= 3:
        table_blocks.append(current_block)

    return [_parse_single_markdown_table(block) for block in table_blocks]


def load_research_parameters(deliverables_dir: Optional[Path] = None) -> pd.DataFrame:
    """Parse simulation-parameter-sheet.md master and detail tables into a single DataFrame."""
    if deliverables_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        deliverables_dir = project_root / "research-deliverables"

    sheet_path = deliverables_dir / "simulation-parameter-sheet.md"
    tables = extract_markdown_tables(sheet_path)

    master_tables = []
    detail_tables = []

    for df in tables:
        cols = [c.lower() for c in df.columns]
        if "parameter" in cols and "value" in cols and "unit" in cols:
            master_tables.append(df)
        elif "parameter" in cols and "what it represents" in cols and "origin" in cols:
            detail_tables.append(df)

    if not master_tables:
        raise ValueError(f"No master parameter tables found in {sheet_path}")

    df_master = pd.concat(master_tables, ignore_index=True)

    col_map = {
        "Parameter": "parameter_name",
        "Value": "raw_value",
        "Unit": "raw_unit",
        "Source / Qualification": "source",
        "Classification": "classification"
    }
    df_master = df_master.rename(columns=col_map)
    df_master = df_master.drop_duplicates(subset=["parameter_name"]).reset_index(drop=True)

    if detail_tables:
        df_detail = pd.concat(detail_tables, ignore_index=True)
        detail_map = {
            "Parameter": "detail_param",
            "What it represents": "description",
            "Origin": "origin_type",
            "v1 Safe?": "v1_safe",
            "Caveat / Next step": "caveats"
        }
        df_detail = df_detail.rename(columns=detail_map)
        df_detail = df_detail.drop_duplicates(subset=["detail_param"]).reset_index(drop=True)

        df_detail["match_key"] = df_detail["detail_param"].apply(
            lambda x: re.split(r"\s*[-—]\s*", str(x))[0].strip().lower()
        )
        df_master["match_key"] = df_master["parameter_name"].apply(
            lambda x: re.split(r"\s*[-—]\s*", str(x))[0].strip().lower()
        )

        # Merge on match_key, keeping first detail match
        detail_dedup = df_detail.drop_duplicates(subset=["match_key"])
        merged = pd.merge(df_master, detail_dedup[["match_key", "description", "origin_type", "v1_safe", "caveats"]],
                          on="match_key", how="left")
        merged = merged.drop(columns=["match_key"])
        return merged

    return df_master


def load_dependency_matrix_edges(deliverables_dir: Optional[Path] = None) -> pd.DataFrame:
    """Parse resource-dependency-matrix.md edges table into a DataFrame."""
    if deliverables_dir is None:
        project_root = Path(__file__).resolve().parents[2]
        deliverables_dir = project_root / "research-deliverables"

    matrix_path = deliverables_dir / "resource-dependency-matrix.md"
    tables = extract_markdown_tables(matrix_path)

    edges_tables = []
    for df in tables:
        cols = [c.lower() for c in df.columns]
        if "edge" in cols and "what flows" in cols:
            edges_tables.append(df)

    if not edges_tables:
        raise ValueError(f"No edges table found in {matrix_path}")

    df_edges = pd.concat(edges_tables, ignore_index=True)
    return df_edges


if __name__ == "__main__":
    params_df = load_research_parameters()
    edges_df = load_dependency_matrix_edges()
    print(f"Loaded {len(params_df)} unique research parameters.")
    print(f"Loaded {len(edges_df)} dependency edges.")
    print(params_df[["parameter_name", "raw_value", "raw_unit", "classification"]].head(8))
