# Security Policy

## Supported Scope

This is an academic data analytics repository. Security handling focuses on protecting datasets, notebooks, credentials, and generated outputs.

## Reporting A Concern

Open a private communication channel with the repository owner if you find:

- Committed credentials or tokens
- Private or sensitive datasets
- Personal data that should not be public
- Dependency or workflow issues that could expose secrets

Avoid posting sensitive details in public issues.

## Data Handling

- Do not commit raw data unless licensing and privacy permissions are clear.
- Store source data under `data/raw/`, which is ignored by Git.
- Store generated intermediate and processed data under `data/interim/` and `data/processed/`, which are also ignored by Git.
- Review notebooks before publishing to ensure outputs do not expose sensitive records.

## Automated Checks

The repository CI includes Bandit static security scanning, pip-audit dependency vulnerability checks, and CodeQL code scanning.
