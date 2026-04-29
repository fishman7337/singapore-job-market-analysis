# Data Dictionary

This project uses seven source files. Raw files should be placed in `data/raw/`.

| Dataset | Expected File | Purpose | Key Checks |
| --- | --- | --- | --- |
| Graduate employment survey | `graduate employment survey modified.csv` | Graduate employment and salary outcomes by university, school, degree, and year | Required year, university, school, degree; non-negative salary and employment-rate fields |
| Overall resident labour force | `labour_force_1_overall_resident.csv` | Resident labour force size over time | Valid year values |
| Labour force by education and sex | `res_labour_force_1_edu_sex.csv` | Labour force distribution by education level and sex | Valid year values |
| Labour force by age and sex | `res_labour_force_2_age_sex.csv` | Labour force distribution by age band and sex | Valid year values |
| Labour force participation rate | `res_LFPR_1_sex_agg_age.csv` | Resident LFPR trends by sex and age aggregate | Valid year values |
| Median salary by industry | `Median Salary Per Industry.xlsx` | Median salary trends across industries | Valid year values |
| Population | `Population.csv` | Population context for labour market competitiveness | File presence and non-empty checks |

## Recommended Canonical Fields

Where possible, downstream code should use snake_case names:

- `year`
- `university`
- `school`
- `degree`
- `employment_rate_overall`
- `employment_rate_ft_perm`
- `basic_monthly_mean`
- `basic_monthly_median`
- `gross_monthly_mean`
- `gross_monthly_median`
- `gross_mthly_25_percentile`
- `gross_mthly_75_percentile`
- `field_of_study`
- `uni_short`

Use `sg_job_market_analysis.cleaning.standardize_columns` to convert raw column labels into canonical names.
