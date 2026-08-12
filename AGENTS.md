# Repository agent instructions

## Scope and precedence

These instructions apply to the entire repository. If a future directory contains a more specific `AGENTS.md`, follow that file for work inside its directory. Direct maintainer instructions take precedence.

## Project context

- **Project:** Singapore Graduate Employment, Salary & Labour-Market Analysis
- **Repository shape:** Python, Jupyter notebooks
- Read `README.md` before changing behaviour, architecture, data handling, or public claims.
- Treat `CONTRIBUTING.md` as the authoritative development workflow and command reference.
- Follow `SECURITY.md` for vulnerability reporting and `CODE_OF_CONDUCT.md` for collaboration.
- Use the workflows under `.github/workflows/` as the final cross-platform CI contract.

## Working agreement

1. Keep each change focused on a clear problem; avoid unrelated cleanup.
2. Inspect nearby tests, configuration, documentation, and generated artifacts before editing.
3. Add or update tests for behavioural changes, including failure and boundary cases.
4. Preserve public APIs and file formats unless the change explicitly includes a documented migration.
5. Never commit credentials, personal data, local environments, caches, or unlicensed datasets.
6. Do not weaken lint, coverage, security, or dependency gates merely to obtain a passing run.
7. After code or architecture changes, run `graphify update .` and review the graph diff; do not commit cache-only churn.
8. Do not stage, commit, push, or publish changes unless the maintainer explicitly requests that action.

## Required validation

Run commands from the repository root. Use a clean environment when dependency or packaging behaviour changes.

### Standard development gate

```text
python -m venv .venv
python -m pip install -e ".[dev]"
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m compileall scripts src tests
```

### Repository-specific CI-equivalent checks

```text
python -m bandit -r src scripts -c pyproject.toml
python -m pip_audit --requirement requirements.txt
python scripts/split_notebook.py --verify
python -m sg_job_market_analysis.dataops --allow-missing
```

Also run `git diff --check`. Record exactly which commands ran, their outcomes, and any documented prerequisite that prevented a check. Do not describe an unexecuted check as passing.

### Conditional or integration setup

- Full DataOps validation requires the seven documented raw datasets; CI and fresh clones use `python -m sg_job_market_analysis.dataops --allow-missing`.

## Managed artifacts and data

- Treat `notebooks/01_student_submission.ipynb` as the source notebook; regenerate and verify notebooks `02_` through `07_` with `scripts/split_notebook.py`.
- Keep raw, interim, processed, and external datasets plus generated figures out of Git.

## Integration and claim boundaries

- The raw datasets are not committed, so an allow-missing smoke is not equivalent to full data validation.
- This is academic exploratory graduate-employment, salary, and labour-market analysis, not an official forecast or causal result.
- **Verified local capability:** Python 3.10-3.12; seven clean notebooks and data reconstruction.
- **Known boundary:** Scope is graduate employment, salary, and labour-market analysis.

## Code, documentation, and evidence standards

- For Python, follow PEP 8, PEP 257, and Google-style docstrings in the production scopes configured by Ruff.
- Prefer small, typed, testable units and explicit error handling. Avoid silent fallbacks that hide invalid data, missing models, credentials, or services.
- Update README, architecture, data/model documentation, examples, and changelog material when interfaces or behaviour change.
- Every quantitative claim must retain its denominator, dataset/version, split, date range, run/configuration, and calculation method.
- Distinguish measured results from targets, examples, heuristics, previews, and prior runs. Do not infer deployment, accuracy, security, causality, or impact from tests or scaffolding alone.
- Update generated files through their source script. If no generator exists, document the manual process and verify semantic equivalence.

## Review and handoff

Before handing off a change, provide a concise summary, list changed files, report validation evidence, and call out residual risks or unavailable integrations. Keep commits imperative and scoped; do not add tool-attribution or automated co-author trailers.
