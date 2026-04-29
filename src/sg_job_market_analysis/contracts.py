"""Dataset contracts for the analysis inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DatasetContract:
    """Expected shape and quality rules for one raw dataset."""

    name: str
    relative_path: Path
    description: str
    file_type: str
    required_columns: tuple[str, ...] = field(default_factory=tuple)
    non_negative_columns: tuple[str, ...] = field(default_factory=tuple)
    year_columns: tuple[str, ...] = field(default_factory=tuple)
    primary_key: tuple[str, ...] = field(default_factory=tuple)


def get_dataset_contracts() -> tuple[DatasetContract, ...]:
    """Return the raw datasets expected by the original CA2 notebook."""

    return (
        DatasetContract(
            name="graduate_employment_survey",
            relative_path=Path("data/raw/graduate employment survey modified.csv"),
            description="Graduate employment outcomes by university, school, degree, and year.",
            file_type="csv",
            required_columns=("year", "university", "school", "degree"),
            non_negative_columns=(
                "employment_rate_overall",
                "employment_rate_ft_perm",
                "basic_monthly_mean",
                "basic_monthly_median",
                "gross_monthly_mean",
                "gross_monthly_median",
                "gross_mthly_25_percentile",
                "gross_mthly_75_percentile",
            ),
            year_columns=("year",),
        ),
        DatasetContract(
            name="overall_resident_labour_force",
            relative_path=Path("data/raw/labour_force_1_overall_resident.csv"),
            description="Resident labour force totals over time.",
            file_type="csv",
            required_columns=("year",),
            year_columns=("year",),
        ),
        DatasetContract(
            name="resident_labour_force_by_education_and_sex",
            relative_path=Path("data/raw/res_labour_force_1_edu_sex.csv"),
            description="Resident labour force distribution by education level and sex.",
            file_type="csv",
            required_columns=("year",),
            year_columns=("year",),
        ),
        DatasetContract(
            name="resident_labour_force_by_age_and_sex",
            relative_path=Path("data/raw/res_labour_force_2_age_sex.csv"),
            description="Resident labour force distribution by age band and sex.",
            file_type="csv",
            required_columns=("year",),
            year_columns=("year",),
        ),
        DatasetContract(
            name="resident_labour_force_participation_rate",
            relative_path=Path("data/raw/res_LFPR_1_sex_agg_age.csv"),
            description="Resident labour force participation rate by sex and age aggregate.",
            file_type="csv",
            required_columns=("year",),
            year_columns=("year",),
        ),
        DatasetContract(
            name="median_salary_by_industry",
            relative_path=Path("data/raw/Median Salary Per Industry.xlsx"),
            description="Median monthly salary by Singapore industry over time.",
            file_type="xlsx",
            required_columns=("year",),
            year_columns=("year",),
        ),
        DatasetContract(
            name="population",
            relative_path=Path("data/raw/Population.csv"),
            description="Population trend dataset used to contextualise workforce competition.",
            file_type="csv",
        ),
    )
