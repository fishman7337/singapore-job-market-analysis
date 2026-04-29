"""Split the original CA2 notebook into sequential review notebooks."""

from __future__ import annotations

import argparse
import copy
import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTEBOOK = REPO_ROOT / "notebooks" / "01_student_submission.ipynb"


@dataclass(frozen=True)
class NotebookSplit:
    """A contiguous one-based cell range for a split notebook."""

    filename: str
    title: str
    start_cell: int
    end_cell: int


SPLIT_PLAN: tuple[NotebookSplit, ...] = (
    NotebookSplit(
        filename="02_project_context_and_research_design.ipynb",
        title="Project Context and Research Design",
        start_cell=1,
        end_cell=15,
    ),
    NotebookSplit(
        filename="03_environment_and_data_overview.ipynb",
        title="Environment Setup and Data Overview",
        start_cell=16,
        end_cell=122,
    ),
    NotebookSplit(
        filename="04_duplicates_and_anomaly_handling.ipynb",
        title="Duplicate Checks and Anomaly Handling",
        start_cell=123,
        end_cell=292,
    ),
    NotebookSplit(
        filename="05_data_types_outliers_and_imputation.ipynb",
        title="Data Types, Outliers, and Imputation",
        start_cell=293,
        end_cell=457,
    ),
    NotebookSplit(
        filename="06_standardisation_and_feature_engineering.ipynb",
        title="Standardisation and Feature Engineering",
        start_cell=458,
        end_cell=540,
    ),
    NotebookSplit(
        filename="07_visual_analysis_findings_and_references.ipynb",
        title="Visual Analysis, Findings, and References",
        start_cell=541,
        end_cell=597,
    ),
)


def load_notebook(path: Path) -> dict:
    """Load a notebook as raw JSON."""

    return json.loads(path.read_text(encoding="utf-8"))


def build_split_notebook(source: dict, notebook_split: NotebookSplit) -> dict:
    """Create one split notebook while preserving original cells and metadata."""

    cells = source["cells"][notebook_split.start_cell - 1 : notebook_split.end_cell]
    notebook = copy.deepcopy(source)
    notebook["cells"] = copy.deepcopy(cells)
    notebook.setdefault("metadata", {})
    notebook["metadata"]["split_from"] = {
        "source": SOURCE_NOTEBOOK.relative_to(REPO_ROOT).as_posix(),
        "title": notebook_split.title,
        "start_cell": notebook_split.start_cell,
        "end_cell": notebook_split.end_cell,
    }
    return notebook


def write_split_notebooks(source_path: Path = SOURCE_NOTEBOOK) -> list[Path]:
    """Write all configured split notebooks."""

    source = load_notebook(source_path)
    output_paths: list[Path] = []
    for notebook_split in SPLIT_PLAN:
        output_path = source_path.parent / notebook_split.filename
        output_path.write_text(
            json.dumps(build_split_notebook(source, notebook_split), ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
        output_paths.append(output_path)
    return output_paths


def verify_split_notebooks(source_path: Path = SOURCE_NOTEBOOK) -> None:
    """Verify split notebooks reconstruct the original cell sequence exactly."""

    source = load_notebook(source_path)
    reconstructed_cells = []
    for notebook_split in SPLIT_PLAN:
        split_path = source_path.parent / notebook_split.filename
        split_notebook = load_notebook(split_path)
        reconstructed_cells.extend(split_notebook["cells"])

    if reconstructed_cells != source["cells"]:
        raise AssertionError("Split notebooks do not reconstruct the original cell sequence.")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing split notebooks instead of rewriting them.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    args = build_parser().parse_args(argv)
    if args.verify:
        verify_split_notebooks()
        print("Split notebooks reconstruct the original notebook cell-for-cell.")
        return 0

    output_paths = write_split_notebooks()
    for output_path in output_paths:
        print(output_path.relative_to(REPO_ROOT).as_posix())
    verify_split_notebooks()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
