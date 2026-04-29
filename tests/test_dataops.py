from pathlib import Path

import pandas as pd

from sg_job_market_analysis.contracts import DatasetContract
from sg_job_market_analysis.dataops import run_quality_checks, validate_dataset_contract


def test_validate_dataset_contract_passes_for_valid_csv(tmp_path: Path):
    data_path = tmp_path / "data" / "raw"
    data_path.mkdir(parents=True)
    file_path = data_path / "graduate.csv"
    pd.DataFrame(
        {
            "Year": [2024, 2025],
            "University": ["SP", "SP"],
            "Degree": ["Applied AI", "Applied AI"],
            "Gross Monthly Median": [3500, 3600],
        }
    ).to_csv(file_path, index=False)
    contract = DatasetContract(
        name="graduate",
        relative_path=Path("data/raw/graduate.csv"),
        description="Synthetic graduate data.",
        file_type="csv",
        required_columns=("year", "university", "degree"),
        non_negative_columns=("gross_monthly_median",),
        year_columns=("year",),
    )

    issues = validate_dataset_contract(contract, repo_root=tmp_path)

    assert issues == []


def test_validate_dataset_contract_flags_missing_and_invalid_values(tmp_path: Path):
    data_path = tmp_path / "data" / "raw"
    data_path.mkdir(parents=True)
    file_path = data_path / "salary.csv"
    pd.DataFrame({"Year": [1800], "Salary": [-1]}).to_csv(file_path, index=False)
    contract = DatasetContract(
        name="salary",
        relative_path=Path("data/raw/salary.csv"),
        description="Synthetic salary data.",
        file_type="csv",
        required_columns=("year", "industry"),
        non_negative_columns=("salary",),
        year_columns=("year",),
    )

    issues = validate_dataset_contract(contract, repo_root=tmp_path)

    assert {issue.check for issue in issues} == {"required_columns", "non_negative", "year_range"}


def test_run_quality_checks_can_downgrade_missing_data_to_warning(tmp_path: Path):
    contract = DatasetContract(
        name="missing",
        relative_path=Path("data/raw/missing.csv"),
        description="Missing data test.",
        file_type="csv",
    )

    issues = run_quality_checks([contract], repo_root=tmp_path, allow_missing=True)

    assert len(issues) == 1
    assert issues[0].severity == "warning"
