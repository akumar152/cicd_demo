Tests in this folder

This README explains the purpose and usage of the project-level unit tests provided alongside the exercise evaluation tests.

Files covered

- tests/ingest_test.py
  - Purpose: unit tests that exercise the ingestion implementation in
    `equalexperts_dataeng_exercise.ingest`.
  - What it verifies:
    - Ingesting the sample JSONL file creates the `blog_analysis.votes` table and
      loads the expected number of rows (one per line in the sample file).
    - Re-running ingestion with a small incremental file updates an existing
      record (same Id) and inserts a new record (new Id), without creating
      duplicate Ids in the target table.
  - How to run locally:
    - Ensure a Python 3.11 environment with dependencies installed (see root README/SETUP.md).
    - From the project root:
      ```bash
      poetry run pytest tests/ingest_test.py
      ```

- tests/outliers_test.py
  - Purpose: unit test that verifies the outlier calculation/view creation in
    `equalexperts_dataeng_exercise.outliers` using the sample dataset included
    in `tests/test-resources/samples-votes.jsonl`.
  - What it verifies:
    - The sample dataset is ingested into `blog_analysis.votes`.
    - The `blog_analysis.outlier_weeks` view is created and contains the
      expected rows (Year, WeekNumber, VoteCount) as described in the
      assignment README.
  - How to run locally:
    - Make sure ingestion works (see ingest_test) and then run:
      ```bash
      poetry run pytest tests/outliers_test.py
      ```

Notes and assumptions

- These tests are intended to be self-contained and to run without depending on
  the evaluation tests in `tests/exercise_tests/`.
- The project expects Python 3.11 and DuckDB to be available. Follow the
  instructions in the project README and SETUP.md for environment setup. If you
  can't install DuckDB locally, consider using the provided Dockerfile.
- The tests create and remove `warehouse.db` in the project root during their
  execution, so they should be run from the repository root.

If you want additional test coverage (e.g. malformed input, schema validation,
or quarantine behaviour), add new tests next to these files following the same
pattern (use pytest fixtures and `tmp_path` for temporary files).