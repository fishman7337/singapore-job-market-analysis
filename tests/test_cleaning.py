import numpy as np
import pandas as pd

from sg_job_market_analysis.cleaning import (
    cap_negative_values,
    deduplicate,
    duplicate_report,
    iqr_bounds,
    missingness_report,
    normalize_column_name,
    replace_blank_with_na,
    standardize_columns,
    trim_string_columns,
)


def test_normalize_column_name_handles_spaces_symbols_and_case():
    assert normalize_column_name(" Gross Monthly Median ($) ") == "gross_monthly_median"
    assert normalize_column_name("Employment Rate FT/Perm") == "employment_rate_ft_perm"


def test_standardize_and_trim_string_columns():
    dataframe = pd.DataFrame({" Degree Name ": ["  AI & Analytics  "], "Value": [1]})

    result = trim_string_columns(standardize_columns(dataframe))

    assert result.columns.tolist() == ["degree_name", "value"]
    assert result.loc[0, "degree_name"] == "AI & Analytics"


def test_replace_blank_with_na_and_missingness_report():
    dataframe = pd.DataFrame({"name": ["Alice", "   "], "score": [1, np.nan]})

    cleaned = replace_blank_with_na(dataframe)
    report = missingness_report(cleaned)

    assert pd.isna(cleaned.loc[1, "name"])
    assert report.loc[0, "missing_count"] == 1
    assert set(report["column"]) == {"name", "score"}


def test_deduplicate_and_duplicate_report():
    dataframe = pd.DataFrame({"year": [2024, 2024, 2025], "degree": ["AI", "AI", "Business"]})

    report = duplicate_report(dataframe, subset=["year", "degree"])
    result = deduplicate(dataframe, subset=["year", "degree"])

    assert report == {"row_count": 3, "duplicate_count": 1, "unique_count": 2}
    assert len(result) == 2


def test_iqr_bounds_and_negative_value_capping():
    dataframe = pd.DataFrame(
        {"salary": [1000, 1100, 1200, 1300, 10000], "rate": [10, -5, 20, -1, 30]}
    )

    lower, upper = iqr_bounds(dataframe["salary"])
    capped = cap_negative_values(dataframe, ["rate"])

    assert lower < 1000
    assert upper < 10000
    assert capped["rate"].tolist() == [10, 0, 20, 0, 30]
