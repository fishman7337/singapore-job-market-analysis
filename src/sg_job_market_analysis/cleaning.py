"""Reusable cleaning helpers used by the project and tests."""

from __future__ import annotations

import re
from collections.abc import Iterable

import numpy as np
import pandas as pd


def normalize_column_name(name: object) -> str:
    """Convert a raw column label into a stable snake_case name."""
    normalized = str(name).strip().lower()
    normalized = re.sub(r"[%/()]+", " ", normalized)
    normalized = re.sub(r"[^0-9a-zA-Z]+", "_", normalized)
    return normalized.strip("_")


def standardize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``dataframe`` with snake_case column names."""
    result = dataframe.copy()
    result.columns = [normalize_column_name(column) for column in result.columns]
    return result


def trim_string_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Strip leading and trailing whitespace from object/string columns."""
    result = dataframe.copy()
    string_columns = result.select_dtypes(include=["object", "string"]).columns
    for column in string_columns:
        result[column] = result[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    return result


def replace_blank_with_na(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Replace empty or whitespace-only strings with ``pd.NA``."""
    result = dataframe.copy()
    return result.replace(r"^\s*$", pd.NA, regex=True)


def drop_empty_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where every value is missing."""
    return dataframe.dropna(how="all").copy()


def deduplicate(dataframe: pd.DataFrame, subset: Iterable[str] | None = None) -> pd.DataFrame:
    """Drop duplicate rows while preserving first occurrence order."""
    return dataframe.drop_duplicates(subset=list(subset) if subset else None, keep="first").copy()


def coerce_numeric(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
    *,
    errors: str = "coerce",
) -> pd.DataFrame:
    """Coerce selected columns to numeric dtype."""
    result = dataframe.copy()
    for column in columns:
        result[column] = pd.to_numeric(result[column], errors=errors)
    return result


def missingness_report(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for each column."""
    missing_count = dataframe.isna().sum()
    report = pd.DataFrame(
        {
            "column": missing_count.index,
            "missing_count": missing_count.values,
            "missing_percent": (
                missing_count.values / len(dataframe) * 100 if len(dataframe) else 0
            ),
        }
    )
    return report.sort_values(["missing_count", "column"], ascending=[False, True]).reset_index(
        drop=True
    )


def duplicate_report(
    dataframe: pd.DataFrame, subset: Iterable[str] | None = None
) -> dict[str, int]:
    """Return a compact duplicate-row summary."""
    duplicate_count = int(dataframe.duplicated(subset=list(subset) if subset else None).sum())
    return {
        "row_count": int(len(dataframe)),
        "duplicate_count": duplicate_count,
        "unique_count": int(len(dataframe) - duplicate_count),
    }


def iqr_bounds(series: pd.Series, multiplier: float = 1.5) -> tuple[float, float]:
    """Return lower and upper Tukey IQR bounds for a numeric series."""
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return (np.nan, np.nan)

    q1 = float(numeric.quantile(0.25))
    q3 = float(numeric.quantile(0.75))
    iqr = q3 - q1
    return (q1 - multiplier * iqr, q3 + multiplier * iqr)


def remove_iqr_outliers(
    dataframe: pd.DataFrame,
    column: str,
    *,
    multiplier: float = 1.5,
) -> pd.DataFrame:
    """Remove rows outside the IQR bounds for a selected numeric column."""
    lower, upper = iqr_bounds(dataframe[column], multiplier=multiplier)
    if np.isnan(lower) or np.isnan(upper):
        return dataframe.copy()

    numeric = pd.to_numeric(dataframe[column], errors="coerce")
    return dataframe.loc[numeric.between(lower, upper) | numeric.isna()].copy()


def cap_negative_values(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
    *,
    floor: int | float = 0,
) -> pd.DataFrame:
    """Replace negative numeric values in selected columns with ``floor``."""
    result = dataframe.copy()
    for column in columns:
        numeric = pd.to_numeric(result[column], errors="coerce")
        result[column] = numeric.mask(numeric < floor, floor)
    return result
