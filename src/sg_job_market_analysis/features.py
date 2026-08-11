"""Feature engineering helpers for graduate employment analysis."""

from __future__ import annotations

import re
from collections.abc import Mapping

import pandas as pd

FIELD_KEYWORDS: Mapping[str, tuple[str, ...]] = {
    "Artificial Intelligence & Computing": (
        "ai",
        "artificial intelligence",
        "analytics",
        "computer",
        "computing",
        "data",
        "information systems",
        "software",
    ),
    "Business & Economics": (
        "account",
        "business",
        "economics",
        "finance",
        "management",
        "marketing",
    ),
    "Engineering": (
        "aerospace",
        "bioengineering",
        "chemical engineering",
        "civil engineering",
        "electrical",
        "engineering",
        "mechanical",
    ),
    "Health Sciences": (
        "dental",
        "medicine",
        "nursing",
        "pharmacy",
        "physiotherapy",
    ),
    "Law": ("law",),
    "Built Environment": (
        "architecture",
        "built environment",
        "estate",
        "real estate",
        "urban",
    ),
    "Science": (
        "biology",
        "chemistry",
        "mathematics",
        "physics",
        "science",
        "statistics",
    ),
    "Arts, Design & Social Sciences": (
        "arts",
        "communication",
        "design",
        "education",
        "humanities",
        "psychology",
        "social sciences",
    ),
}


def normalize_text(value: object) -> str:
    """Normalise text for deterministic matching."""
    text = "" if pd.isna(value) else str(value)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def classify_field_of_study(degree: object) -> str:
    """Classify a degree name into a broad field of study."""
    text = normalize_text(degree)
    if not text:
        return "Unknown"

    for field, keywords in FIELD_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return field

    return "Other"


def add_field_of_study(
    dataframe: pd.DataFrame,
    *,
    degree_column: str = "degree",
    output_column: str = "field_of_study",
) -> pd.DataFrame:
    """Add a broad field-of-study column based on degree text."""
    if degree_column not in dataframe.columns:
        raise KeyError(f"Column not found: {degree_column}")

    result = dataframe.copy()
    result[output_column] = result[degree_column].map(classify_field_of_study)
    return result


def add_salary_spread(
    dataframe: pd.DataFrame,
    *,
    lower_column: str = "gross_mthly_25_percentile",
    upper_column: str = "gross_mthly_75_percentile",
    output_column: str = "gross_salary_iqr",
) -> pd.DataFrame:
    """Add the interquartile salary spread where percentile columns exist."""
    missing = {lower_column, upper_column}.difference(dataframe.columns)
    if missing:
        raise KeyError(f"Missing salary percentile column(s): {sorted(missing)}")

    result = dataframe.copy()
    result[output_column] = pd.to_numeric(result[upper_column], errors="coerce") - pd.to_numeric(
        result[lower_column], errors="coerce"
    )
    return result


def add_employment_rate_gap(
    dataframe: pd.DataFrame,
    *,
    overall_column: str = "employment_rate_overall",
    full_time_column: str = "employment_rate_ft_perm",
    output_column: str = "employment_rate_gap",
) -> pd.DataFrame:
    """Add the gap between overall and full-time permanent employment rates."""
    missing = {overall_column, full_time_column}.difference(dataframe.columns)
    if missing:
        raise KeyError(f"Missing employment-rate column(s): {sorted(missing)}")

    result = dataframe.copy()
    result[output_column] = pd.to_numeric(result[overall_column], errors="coerce") - pd.to_numeric(
        result[full_time_column], errors="coerce"
    )
    return result
