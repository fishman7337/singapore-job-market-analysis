# Methodology

## Analytical Workflow

1. Define the research question and boundaries.
2. Load seven source datasets covering graduate employment, resident labour force, labour force participation, median salary, and population context.
3. Inspect each dataset for shape, missingness, duplicates, abnormal categories, and invalid numeric values.
4. Clean and standardise datasets before analysis.
5. Engineer features such as field of study, university short names, salary spread, and employment-rate gaps.
6. Explore trends using static and interactive visualisations.
7. Use machine learning experiments, including Random Forest regression, to support missing-value imputation and salary prediction analysis.
8. Summarise insights and limitations.

## Cleaning Strategy

- Standardise column names and categorical labels where needed.
- Remove duplicated records where they are confirmed to be duplicated observations rather than repeated valid measurements.
- Treat missing values based on variable meaning, distribution, and modelling suitability.
- Use IQR and z-score approaches for outlier review.
- Validate that count, salary, and rate fields do not contain impossible negative values.

## Modelling Strategy

The notebook uses Random Forest regression to support prediction of missing salary-related values. This is suitable for exploratory tabular modelling because it can capture non-linear relationships and interactions without heavy assumptions about feature distributions.

## Interpretation Principles

- Correlation does not prove causation.
- Salary and employment outcomes can be affected by macroeconomic conditions, cohort size, industry cycles, survey design, and institutional effects.
- Gender and labour force comparisons should be interpreted carefully because aggregate trends may hide occupation, seniority, and participation differences.
- Model performance should be reviewed alongside data quality, sample coverage, and feature leakage risks.
