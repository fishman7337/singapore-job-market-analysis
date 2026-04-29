# DataOps Guide

## Goals

The DataOps setup keeps the project reproducible, reviewable, and safe to share.

## Data Zones

- `data/raw/`: source files copied exactly as received or downloaded
- `data/interim/`: temporary cleaned or reshaped files
- `data/processed/`: final datasets ready for modelling or visualisation
- `data/external/`: reference data from outside the main analysis flow

Only README and placeholder files are tracked. Dataset files are intentionally ignored by Git.

## Dataset Contracts

Dataset expectations are defined in `src/sg_job_market_analysis/contracts.py` and summarised in `configs/datasets.yml`. Contracts cover:

- Expected filenames
- File types
- Required columns
- Non-negative numeric fields
- Year range checks
- Optional uniqueness checks for future extensions

## Data Quality Commands

Run strict checks when raw data is available:

```bash
python -m sg_job_market_analysis.dataops
```

Run a smoke check when raw data is absent:

```bash
python -m sg_job_market_analysis.dataops --allow-missing
```

Use JSON output for automation:

```bash
python -m sg_job_market_analysis.dataops --format json
```

## CI Behaviour

CI does not require private or local datasets. It runs with `--allow-missing` so the validation CLI is exercised while keeping raw data out of the repository.

The CI pipeline also includes security checks:

- Bandit scans Python source and maintenance scripts for common security issues.
- pip-audit checks runtime Python dependencies for known vulnerabilities.
- CodeQL runs code scanning on push, pull request, and a weekly schedule.

## Operational Rules

- Keep raw data immutable.
- Make cleaning steps reproducible in code or notebook cells.
- Record assumptions in documentation when a cleaning choice affects interpretation.
- Do not commit large generated outputs unless they are final report artefacts.
- Re-run tests and DataOps checks before publishing changes.
