import pandas as pd
import pytest

from sg_job_market_analysis.features import (
    add_employment_rate_gap,
    add_field_of_study,
    add_salary_spread,
    classify_field_of_study,
)


@pytest.mark.parametrize(
    ("degree", "expected"),
    [
        ("Bachelor of Science in Artificial Intelligence", "Artificial Intelligence & Computing"),
        ("Bachelor of Business Management", "Business & Economics"),
        ("Bachelor of Laws", "Law"),
        ("", "Unknown"),
    ],
)
def test_classify_field_of_study(degree, expected):
    assert classify_field_of_study(degree) == expected


def test_add_field_of_study_returns_copy_with_new_column():
    dataframe = pd.DataFrame({"degree": ["Computer Science", "Mechanical Engineering"]})

    result = add_field_of_study(dataframe)

    assert "field_of_study" in result.columns
    assert result["field_of_study"].tolist() == [
        "Artificial Intelligence & Computing",
        "Engineering",
    ]
    assert "field_of_study" not in dataframe.columns


def test_add_salary_spread_and_employment_rate_gap():
    dataframe = pd.DataFrame(
        {
            "gross_mthly_25_percentile": [3000],
            "gross_mthly_75_percentile": [4500],
            "employment_rate_overall": [92.5],
            "employment_rate_ft_perm": [88.0],
        }
    )

    result = add_employment_rate_gap(add_salary_spread(dataframe))

    assert result.loc[0, "gross_salary_iqr"] == 1500
    assert result.loc[0, "employment_rate_gap"] == pytest.approx(4.5)
