.PHONY: install lint compile test dataops dataops-smoke check

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

lint:
	ruff check src tests

compile:
	python -m compileall src tests

test:
	pytest

dataops:
	python -m sg_job_market_analysis.dataops

dataops-smoke:
	python -m sg_job_market_analysis.dataops --allow-missing

check: lint compile test dataops-smoke
