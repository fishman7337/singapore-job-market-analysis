# Contributing

Thank you for improving this project. The goal is to keep the academic analysis reproducible, well-documented, and easy to review.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## Before Submitting Changes

Run:

```bash
ruff check src tests
python -m compileall src tests
pytest
python -m sg_job_market_analysis.dataops --allow-missing
```

If you have the raw datasets locally, also run:

```bash
python -m sg_job_market_analysis.dataops
```

## Contribution Guidelines

- Keep raw data out of Git unless there is explicit permission to publish it.
- Add or update tests for reusable Python code.
- Update documentation when changing project structure, methodology, or data assumptions.
- Preserve the original CA2 notebook as an academic artefact unless a change is needed for reproducibility.
- Use clear commit messages that describe the user-facing or reviewer-facing change.
