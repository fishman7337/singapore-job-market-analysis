import importlib.util
import json
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "split_notebook.py"
SPEC = importlib.util.spec_from_file_location("split_notebook", SCRIPT_PATH)
assert SPEC is not None
split_notebook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = split_notebook
SPEC.loader.exec_module(split_notebook)

SOURCE_NOTEBOOK = split_notebook.SOURCE_NOTEBOOK
SPLIT_PLAN = split_notebook.SPLIT_PLAN


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_original_notebook_is_retained():
    assert SOURCE_NOTEBOOK.exists()


def test_split_notebooks_cover_original_cells_in_order():
    source = _load(SOURCE_NOTEBOOK)
    reconstructed_cells = []

    for notebook_split in SPLIT_PLAN:
        split_path = SOURCE_NOTEBOOK.parent / notebook_split.filename
        assert split_path.exists()
        split_notebook = _load(split_path)
        reconstructed_cells.extend(split_notebook["cells"])

    assert reconstructed_cells == source["cells"]


def test_split_plan_has_no_gaps_or_overlaps():
    expected_start = 1
    for notebook_split in SPLIT_PLAN:
        assert notebook_split.start_cell == expected_start
        assert notebook_split.end_cell >= notebook_split.start_cell
        expected_start = notebook_split.end_cell + 1

    source = _load(SOURCE_NOTEBOOK)
    assert expected_start == len(source["cells"]) + 1
