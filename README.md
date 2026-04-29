# Singapore Graduate Employment & Labour Market Analytics

[![CI](https://github.com/fishman7337/singapore-job-market-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/fishman7337/singapore-job-market-analysis/actions/workflows/ci.yml)

This repository contains an academic data analytics project on Singapore graduate employment, salaries, labour force participation, and workforce competitiveness. It preserves the original ST1510 CA2 notebook and slide deck, while adding a maintainable Python package, tests, CI, and DataOps documentation around the analysis.

## Academic Context

- Institution: Singapore Polytechnic, School of Computing
- Diploma: Diploma in Applied AI & Analytics
- Module: ST1510 Programming for Data Analytics
- Assessment: CA2
- Academic year: AY2024/2025, Year 1 Semester 2
- Student: Goh Kun Ming
- Lecturer: Senior Lecturer Goh Chia Ming

## Research Question

How do factors such as degree specialisation, industry, gender, and labour market competitiveness affect employment outcomes and salary in Singapore?

## What This Project Covers

- Graduate employment outcomes by university, school, degree, and year
- Labour force trends by age, gender, and educational qualification
- Median salary trends across Singapore industries
- Population and labour market competition context
- Data cleaning, missing-value handling, duplicate checks, anomaly checks, outlier treatment, and feature engineering
- Static and interactive visualisations using Matplotlib, Seaborn, and Plotly
- Random Forest modelling for salary imputation and prediction experiments

## Repository Layout

```text
.
|-- .github/workflows/        # CI for linting, tests, compile checks, and DataOps smoke checks
|-- configs/                  # Dataset registry and project configuration
|-- data/                     # Local-only raw/interim/processed data folders
|-- docs/                     # Methodology, DataOps, reproducibility, and project notes
|-- notebooks/                # Original CA2 notebook plus sequential split notebooks
|-- reports/                  # Slides, figures, and presentation artefacts
|-- scripts/                  # Command-line helper scripts
|-- src/sg_job_market_analysis/
|   |-- cleaning.py           # Reusable data cleaning helpers
|   |-- contracts.py          # Dataset contracts
|   |-- dataops.py            # Data quality CLI
|   |-- features.py           # Feature engineering helpers
|   `-- validation.py         # Validation primitives
`-- tests/                    # Pytest suite
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

## Data Setup

Raw datasets are not committed to Git. Place the original source files in `data/raw/` using the filenames below:

- `graduate employment survey modified.csv`
- `labour_force_1_overall_resident.csv`
- `res_labour_force_1_edu_sex.csv`
- `res_labour_force_2_age_sex.csv`
- `res_LFPR_1_sex_agg_age.csv`
- `Median Salary Per Industry.xlsx`
- `Population.csv`

Run the DataOps checks after adding the data:

```bash
python -m sg_job_market_analysis.dataops
```

For CI or a fresh clone without private/local data:

```bash
python -m sg_job_market_analysis.dataops --allow-missing
```

## Reproducing The Notebook

Open `notebooks/01_student_submission.ipynb` after installing the dependencies and placing datasets in `data/raw/`. The notebook paths are set relative to the `notebooks/` folder.

The original notebook is retained as the full submission artefact. For easier review, the same notebook has also been split into sequential notebooks `02_` through `07_`; together, those split notebooks reconstruct every original cell in order. Regenerate or verify the split with:

```bash
python scripts/split_notebook.py
python scripts/split_notebook.py --verify
```

## Quality Gates

The GitHub Actions workflow runs:

- Ruff linting
- Python compilation checks
- Pytest with coverage output
- Notebook split verification
- DataOps smoke checks that confirm the validation CLI works without requiring raw data in Git

## Documentation

- [Project context](docs/PROJECT_CONTEXT.md)
- [Methodology](docs/METHODOLOGY.md)
- [DataOps guide](docs/DATAOPS.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [Reproducibility guide](docs/REPRODUCIBILITY.md)
- [Artefact manifest](docs/ASSET_MANIFEST.md)

## Limitations

This project should be treated as an academic analytics submission, not as an official labour market forecast. The analysis depends on the quality, coverage, and update timing of the source datasets. Modelling results should be interpreted as exploratory evidence, not causal proof.

## Attribution

Created by Goh Kun Ming for ST1510 Programming for Data Analytics CA2 at Singapore Polytechnic, School of Computing.
