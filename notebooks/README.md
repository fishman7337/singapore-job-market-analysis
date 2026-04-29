# Notebooks

This folder contains the original CA2 notebook and a sequentially split version for easier review.

## Files

- `01_student_submission.ipynb`: Original full analysis notebook for ST1510 Programming for Data Analytics CA2.
- `02_project_context_and_research_design.ipynb`: Research context, question, objectives, and boundaries.
- `03_environment_and_data_overview.ipynb`: Imports, dataset loading, overview checks, and early reshaping.
- `04_duplicates_and_anomaly_handling.ipynb`: Duplicate handling and abnormal data inspection/correction.
- `05_data_types_outliers_and_imputation.ipynb`: Type corrections, outlier handling, missing data, and modelling-based imputation.
- `06_standardisation_and_feature_engineering.ipynb`: Categorical standardisation, numeric validation, and engineered features.
- `07_visual_analysis_findings_and_references.ipynb`: Visual analysis, conclusions, and references.

The split notebooks collectively contain every cell from the original notebook in the same order. They are intended to be read or executed sequentially.

## Maintenance

Regenerate and verify the split notebooks with:

```bash
python scripts/split_notebook.py
python scripts/split_notebook.py --verify
```

## Running

Install dependencies, place source files in `../data/raw/`, and open the notebook in Jupyter Lab or Jupyter Notebook.
