"""Validation primitives for raw and processed data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

from sg_job_market_analysis.cleaning import normalize_column_name

Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class ValidationIssue:
    """A single validation issue emitted by a data quality check."""

    severity: Severity
    dataset: str
    check: str
    message: str


def _normalised_columns(dataframe: pd.DataFrame) -> dict[str, str]:
    return {normalize_column_name(column): str(column) for column in dataframe.columns}


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: tuple[str, ...],
    *,
    dataset: str,
) -> list[ValidationIssue]:
    """Validate that required columns are present after column normalisation."""
    available = _normalised_columns(dataframe)
    issues: list[ValidationIssue] = []
    for column in required_columns:
        normalized = normalize_column_name(column)
        if normalized not in available:
            issues.append(
                ValidationIssue(
                    severity="error",
                    dataset=dataset,
                    check="required_columns",
                    message=f"Missing required column: {column}",
                )
            )
    return issues


def validate_non_negative(
    dataframe: pd.DataFrame,
    columns: tuple[str, ...],
    *,
    dataset: str,
) -> list[ValidationIssue]:
    """Validate that selected columns do not contain negative numeric values."""
    available = _normalised_columns(dataframe)
    issues: list[ValidationIssue] = []
    for column in columns:
        normalized = normalize_column_name(column)
        if normalized not in available:
            continue

        source_column = available[normalized]
        numeric = pd.to_numeric(dataframe[source_column], errors="coerce")
        negative_count = int((numeric < 0).sum())
        if negative_count:
            issues.append(
                ValidationIssue(
                    severity="error",
                    dataset=dataset,
                    check="non_negative",
                    message=f"{source_column} contains {negative_count} negative value(s).",
                )
            )
    return issues


def validate_year_columns(
    dataframe: pd.DataFrame,
    columns: tuple[str, ...],
    *,
    dataset: str,
    min_year: int = 1900,
    max_year: int = 2100,
) -> list[ValidationIssue]:
    """Validate year columns are numeric and in a reasonable range."""
    available = _normalised_columns(dataframe)
    issues: list[ValidationIssue] = []
    for column in columns:
        normalized = normalize_column_name(column)
        if normalized not in available:
            continue

        source_column = available[normalized]
        numeric = pd.to_numeric(dataframe[source_column], errors="coerce")
        invalid = numeric.isna() | ~numeric.between(min_year, max_year)
        invalid_count = int(invalid.sum())
        if invalid_count:
            issues.append(
                ValidationIssue(
                    severity="error",
                    dataset=dataset,
                    check="year_range",
                    message=f"{source_column} contains {invalid_count} invalid year value(s).",
                )
            )
    return issues


def validate_no_duplicate_keys(
    dataframe: pd.DataFrame,
    key_columns: tuple[str, ...],
    *,
    dataset: str,
) -> list[ValidationIssue]:
    """Validate that a composite key has no duplicate records."""
    if not key_columns:
        return []

    available = _normalised_columns(dataframe)
    source_columns = [available.get(normalize_column_name(column)) for column in key_columns]
    if any(column is None for column in source_columns):
        return []

    duplicate_count = int(dataframe.duplicated(subset=source_columns).sum())
    if not duplicate_count:
        return []

    return [
        ValidationIssue(
            severity="error",
            dataset=dataset,
            check="duplicate_key",
            message=f"Composite key {key_columns} contains {duplicate_count} duplicate record(s).",
        )
    ]
