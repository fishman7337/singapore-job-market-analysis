"""Command-line data quality checks for the project."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from sg_job_market_analysis.contracts import DatasetContract, get_dataset_contracts
from sg_job_market_analysis.paths import REPO_ROOT
from sg_job_market_analysis.validation import (
    ValidationIssue,
    validate_no_duplicate_keys,
    validate_non_negative,
    validate_required_columns,
    validate_year_columns,
)


def load_dataset(path: Path, file_type: str) -> pd.DataFrame:
    """Load a supported raw dataset format."""
    if file_type == "csv":
        return pd.read_csv(path)
    if file_type in {"xls", "xlsx"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {file_type}")


def validate_dataset_contract(
    contract: DatasetContract,
    *,
    repo_root: Path = REPO_ROOT,
    allow_missing: bool = False,
) -> list[ValidationIssue]:
    """Validate one dataset contract against files on disk."""
    path = repo_root / contract.relative_path
    if not path.exists():
        return [
            ValidationIssue(
                severity="warning" if allow_missing else "error",
                dataset=contract.name,
                check="file_exists",
                message=f"Expected file is missing: {contract.relative_path.as_posix()}",
            )
        ]

    dataframe = load_dataset(path, contract.file_type)
    issues: list[ValidationIssue] = []
    if dataframe.empty:
        issues.append(
            ValidationIssue(
                severity="error",
                dataset=contract.name,
                check="not_empty",
                message="Dataset is empty.",
            )
        )

    issues.extend(
        validate_required_columns(dataframe, contract.required_columns, dataset=contract.name)
    )
    issues.extend(
        validate_non_negative(dataframe, contract.non_negative_columns, dataset=contract.name)
    )
    issues.extend(validate_year_columns(dataframe, contract.year_columns, dataset=contract.name))
    issues.extend(
        validate_no_duplicate_keys(dataframe, contract.primary_key, dataset=contract.name)
    )
    return issues


def run_quality_checks(
    contracts: Iterable[DatasetContract] | None = None,
    *,
    repo_root: Path = REPO_ROOT,
    allow_missing: bool = False,
) -> list[ValidationIssue]:
    """Run all configured data quality checks."""
    selected_contracts = tuple(contracts or get_dataset_contracts())
    issues: list[ValidationIssue] = []
    for contract in selected_contracts:
        issues.extend(
            validate_dataset_contract(contract, repo_root=repo_root, allow_missing=allow_missing)
        )
    return issues


def _format_text(issues: list[ValidationIssue]) -> str:
    if not issues:
        return "Data quality checks passed."

    lines = ["Data quality checks found issues:"]
    for issue in issues:
        lines.append(f"[{issue.severity.upper()}] {issue.dataset}::{issue.check} - {issue.message}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Run project data quality checks.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root containing the data directory.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Downgrade missing raw data files to warnings for CI smoke checks.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = build_parser().parse_args(argv)
    issues = run_quality_checks(repo_root=args.repo_root, allow_missing=args.allow_missing)

    if args.format == "json":
        print(json.dumps([asdict(issue) for issue in issues], indent=2))
    else:
        print(_format_text(issues))

    has_error = any(issue.severity == "error" for issue in issues)
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
