"""Unit tests for the outlier view implementation.
"""
from pathlib import Path
import duckdb
import os

import pytest

from equalexperts_dataeng_exercise import ingest as ingest_module
from equalexperts_dataeng_exercise.outliers import create_outlier_weeks_view


SAMPLE = Path(__file__).parent / "test-resources" / "samples-votes.jsonl"
DB = "warehouse.db"


@pytest.fixture(autouse=True)
def remove_db():
    if os.path.exists(DB):
        os.remove(DB)
    yield
    if os.path.exists(DB):
        os.remove(DB)


def test_outlier_weeks_matches_expected_sample_data():
    ingest_module.ingest(str(SAMPLE))
    create_outlier_weeks_view()

    con = duckdb.connect(DB)
    try:
        rows = con.execute(
            "SELECT Year, WeekNumber, VoteCount FROM blog_analysis.outlier_weeks ORDER BY Year, WeekNumber"
        ).fetchall()
    finally:
        con.close()

    expected = [
        (2022, 0, 1),
        (2022, 1, 3),
        (2022, 2, 3),
        (2022, 5, 1),
        (2022, 6, 1),
        (2022, 8, 1),
    ]

    assert rows == expected
