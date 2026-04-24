"""
Data structure derived from the 2020 SVI data dictionary CSV.

This module keeps the Python metadata dictionary aligned with
tu3svi2_0av4_SVIdatadictionary_2026-04-23_only2020.csv.
"""

from __future__ import annotations

import csv
import pandas as pd
import numpy as np
from pathlib import Path


CSV_FILENAME = "tu3svi2_0av4_SVIdatadictionary_2026-04-23_only2020.csv"

DTYPE_TO_PYTYPE = {
    "str": str,
    "int64": int,
    "float": float,
}

DEFAULT_DF_VARIABLE_METADATA: dict[str, dict[str, object]] = {
    "BG2020": {"label": "Block Group ID", "DataType": 'String', "pyType": str, "source": ""},
    "FIPSCNTY": {"label": "County FIPS Code", "DataType": 'String', "pyType": str, "source": ""},
    "SETX": {"label": "Southeast Texas", "DataType": 'Int', "pyType": int, "source": ""},
    "TRACT2020": {"label": "Census Tract ID", "DataType": 'String', "pyType": str, "source": ""},
    "airsite_bg": {"label": "Air Site Block Group", "DataType": 'String', "pyType": str, "source": ""},
    "airsite_tract": {"label": "Air Site Census Tract", "DataType": 'String', "pyType": str, "source": ""},
    "airsite_name": {"label": "Air Site Name", "DataType": 'String', "pyType": str, "source": ""},
}


def _resolve_csv_path() -> Path:
    csv_path = Path(__file__).with_name(CSV_FILENAME)
    if csv_path.exists():
        return csv_path

    matches = sorted(Path(__file__).parent.glob("tu3svi2_0av4_SVIdatadictionary_*_only2020.csv"))
    if not matches:
        raise FileNotFoundError(f"Could not find SVI data dictionary CSV next to {__file__}.")

    return matches[-1]


def _data_type_label(dtype: str) -> str:
    return {
        "str": "String",
        "int64": "Int",
        "float": "Float",
    }.get(dtype, dtype)


def _analysis_unit(row: dict[str, str]) -> str:
    geocode = row["comcat"]
    if geocode == "TRACT2020":
        return "Census tract"
    if geocode == "BG2020":
        return "Census block group"
    return "Census tract or block group"


def _measure_unit(row: dict[str, str]) -> str:
    label = row["label"]
    if row["percent"] == "1":
        return "Percent"
    if row["proportion"] == "1":
        return "Proportion"
    if "Percentile Rank" in label:
        return "Percentile rank"
    if "Quartile" in label:
        return "Quartile"
    if "Match" in label:
        return "Indicator"
    if row["gencat"] == "Denominator" or row["dtype"] == "int64":
        return "Count"
    return "Value"


def _categorical(row: dict[str, str]) -> bool:
    return row["dtype"] == "str"


def _categorical_type(row: dict[str, str]) -> str | None:
    if not _categorical(row):
        return None
    if "Quartile" in row["label"]:
        return "ordinal"
    return "nominal"


def _notes(row: dict[str, str]) -> str:
    details = [
        f"1. Source SVI framework: {row['SVI']}.",
        f"2. Year: {row['year']}.",
        f"3. General category: {row['gencat']} ({row['gencatcode']}).",
        f"4. Comparison category: {row['comcat']} ({row['comcatcode']}).",
        f"5. SVI theme: {row['theme']}.",
        f"6. SVI category: {row['SVIcat']}.",
        f"7. Original source variable: {row['oldvarname']}.",
        f"8. ACS table references: v2={row['ACStable1v2']}, v1={row['ACStable1v1']}.",
        f"9. Inverted for index construction: {row['inverted'] == '1'}.",
        f"10. Stored as proportion: {row['proportion'] == '1'}; stored as percent: {row['percent'] == '1'}."
    ]
    return "\n\n".join(details)


def _build_data_structure() -> dict[str, dict[str, object]]:
    csv_path = _resolve_csv_path()
    data_structure: dict[str, dict[str, object]] = {}

    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            dtype = row["dtype"]
            entry: dict[str, object] = {
                "label": row["label"],
                "DataType": _data_type_label(dtype),
                "pyType": DTYPE_TO_PYTYPE.get(dtype, str),
                "AnalysisUnit": _analysis_unit(row),
                "MeasureUnit": _measure_unit(row),
                "notes": _notes(row)
            }

            if _categorical(row):
                entry["categorical"] = True
                entry["categorical_type"] = _categorical_type(row)

            data_structure[row["newvarname"]] = entry

    return data_structure


def compare_data_structure_with_df(
    datastructure: dict[str, dict[str, object]],
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Build a comparison table between metadata keys and dataframe columns."""
    ds_vars = pd.Index(datastructure.keys(), name="variable")
    df_vars = pd.Index(df.columns, name="variable")
    all_vars = ds_vars.union(df_vars)

    compare_df = pd.DataFrame({"variable": all_vars})
    compare_df["in_datastructure"] = compare_df["variable"].isin(ds_vars)
    compare_df["in_df"] = compare_df["variable"].isin(df_vars)

    compare_df["match_status"] = np.select(
        [
            compare_df["in_datastructure"] & compare_df["in_df"],
            compare_df["in_datastructure"] & ~compare_df["in_df"],
            ~compare_df["in_datastructure"] & compare_df["in_df"],
        ],
        [
            "in both",
            "only in datastructure",
            "only in df",
        ],
        default="not in either",
    )

    # Pull selected metadata from datastructure where available.
    def _metadata_lookup(variable: object, field: str) -> str:
        if not isinstance(variable, str):
            return ""
        value = datastructure.get(variable, {}).get(field, "")
        return value if isinstance(value, str) else str(value)

    compare_df["label"] = compare_df["variable"].map(lambda v: _metadata_lookup(v, "label"))
    compare_df["DataType"] = compare_df["variable"].map(lambda v: _metadata_lookup(v, "DataType"))

    return compare_df.sort_values(["match_status", "variable"]).reset_index(drop=True)


def match_data_structure_to_df(
    datastructure: dict[str, dict[str, object]],
    df: pd.DataFrame,
) -> tuple[dict[str, dict[str, object]], pd.DataFrame]:
    """Align datastructure keys to dataframe columns and return comparison output."""
    compare_df = compare_data_structure_with_df(datastructure=datastructure, df=df)

    # Remove variables not present in dataframe.
    condition = compare_df["match_status"] == "only in datastructure"
    variables_to_remove = compare_df.loc[condition, "variable"].tolist()
    for var in variables_to_remove:
        datastructure.pop(var, None)

    # Add variables present in dataframe but missing from datastructure.
    condition = compare_df["match_status"] == "only in df"
    variables_to_add = compare_df.loc[condition, "variable"].tolist()
    for var in variables_to_add:
        default_metadata = DEFAULT_DF_VARIABLE_METADATA.get(var, {})
        data_type = default_metadata.get("DataType", str)
        datastructure[var] = {
            "label": default_metadata.get("label", ""),
            "DataType": data_type,
            "source": default_metadata.get("source", ""),
            "pyType": data_type if isinstance(data_type, type) else str,
            "AnalysisUnit": "",
            "MeasureUnit": "",
            "notes": "Added during dataframe-to-datastructure alignment.",
        }

    # sort the datastructure to match the order of the dataframe columns
    sorted_datastructure = {var: datastructure[var] for var in 
                            df.columns if var in datastructure}

    updated_compare_df = compare_data_structure_with_df(datastructure=sorted_datastructure, df=df)
    return sorted_datastructure, updated_compare_df

DATA_STRUCTURE = _build_data_structure()

# Alias retained for codebook workflows that expect a lowercase name.
datastructure = DATA_STRUCTURE