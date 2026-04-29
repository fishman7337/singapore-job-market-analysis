# GitHub Actions Workflows

This folder contains automated checks that run on GitHub.

| Workflow | Purpose |
| --- | --- |
| `ci.yml` | Runs linting, compilation, tests, Bandit, pip-audit, notebook split verification, and DataOps smoke checks |
| `codeql.yml` | Runs CodeQL static analysis for Python security review |

CI is expected to pass before changes are considered ready.
