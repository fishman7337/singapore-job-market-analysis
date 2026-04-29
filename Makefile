.PHONY: install lint compile test security notebooks-verify dataops dataops-smoke check

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

lint:
	ruff check src scripts tests

compile:
	python -m compileall src scripts tests

test:
	pytest

security:
	bandit -r src scripts -c pyproject.toml
	pip-audit --requirement requirements.txt

notebooks-verify:
	python scripts/split_notebook.py --verify

dataops:
	python -m sg_job_market_analysis.dataops

dataops-smoke:
	python -m sg_job_market_analysis.dataops --allow-missing

check: lint compile test security notebooks-verify dataops-smoke
