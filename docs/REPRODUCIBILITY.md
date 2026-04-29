# Reproducibility Guide

## Environment

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Data

Place raw source files in `data/raw/` using the filenames listed in `README.md` and `docs/DATA_DICTIONARY.md`.

## Checks

Run:

```bash
ruff check src tests
python -m compileall src tests
pytest
python -m sg_job_market_analysis.dataops
```

If raw data is not present, use:

```bash
python -m sg_job_market_analysis.dataops --allow-missing
```

## Notebook Execution

Open `notebooks/01_student_submission.ipynb` from the repository root or from Jupyter Lab. The notebook uses paths relative to its own folder and expects raw files in `../data/raw/`.

## Known Reproducibility Limits

- Public datasets may change over time.
- Local raw files are not versioned in Git.
- Notebook outputs may depend on library versions and plotting backends.
- NLTK resources may need to be downloaded locally before NLP cells run.
