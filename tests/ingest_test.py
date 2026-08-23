"""Unit tests for the ingestion implementation.

These tests exercise the ingest.ingest(...) function using the provided
sample JSONL resource. They are intended to be fast and self-contained.
"""
from pathlib import Path
import os
import duckdb
import json
import pytest

from equalexperts_dataeng_exercise import ingest as ingest_module


SAMPLES = Path(__file__).parent / "test-resources" / "samples-votes.jsonl"
DB = "warehouse.db"


@pytest.fixture(autouse=True)
def remove_db():
    if os.path.exists(DB):
        os.remove(DB)


def count_file_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as fh:
        return sum(1 for _ in fh)


def test_ingest_creates_table_and_loads_rows():
    line_count = count_file_lines(SAMPLES)
    ingest_module.ingest(str(SAMPLES))

    con = duckdb.connect(DB)
    try:
        result = con.execute("SELECT COUNT(*) FROM blog_analysis.votes").fetchall()
        assert result[0][0] == line_count

        # check row exists
        row = con.execute("SELECT Id, PostId, VoteTypeId FROM blog_analysis.votes WHERE Id=1").fetchone()
        assert row is not None
        assert row[0] == 1
    finally:
        con.close()


def test_ingest_updates_existing_records_and_inserts_new_records(tmp_path):
    # First ingest full sample
    ingest_module.ingest(str(SAMPLES))
    con = duckdb.connect(DB)
    try:
        before_count = con.execute("SELECT COUNT(*) FROM blog_analysis.votes").fetchone()[0]
    finally:
        con.close()

    # Create a small incremental file that updates Id=1 and adds a new Id=9999
    updated = [
        {"Id": "1", "PostId": "999", "VoteTypeId": "2", "CreationDate": "2022-01-02T00:00:00.000"},
        {"Id": "9999", "PostId": "42", "VoteTypeId": "2", "CreationDate": "2026-01-01T00:00:00.000"},
    ]
    inc_file = tmp_path / "inc.jsonl"
    with inc_file.open("w", encoding="utf-8") as fh:
        for obj in updated:
            fh.write(json.dumps(obj) + "\n")

    # Run ingestion on incremental file
    ingest_module.ingest(str(inc_file))

    con = duckdb.connect(DB)
    try:
        # The updated Id=1 should be present with new PostId
        row = con.execute("SELECT Id, PostId FROM blog_analysis.votes WHERE Id=1").fetchone()
        assert row is not None
        assert row[1] == 999

        # New id should be added
        new_row = con.execute("SELECT Id FROM blog_analysis.votes WHERE Id=9999").fetchone()
        assert new_row is not None

        # Total count should increase by 1 (one new row, one updated replaced)
        after_count = con.execute("SELECT COUNT(*) FROM blog_analysis.votes").fetchone()[0]
        assert after_count == before_count + 1

        # No duplicate Ids
        cnt_id1 = con.execute("SELECT COUNT(*) FROM blog_analysis.votes WHERE Id=1").fetchone()[0]
        assert cnt_id1 == 1

    finally:
        con.close()


def test_ingest_is_idempotent():
    ingest_module.ingest(str(SAMPLES))

    con = duckdb.connect(DB)
    try:
        before_count = con.execute(
            "SELECT COUNT(*) FROM blog_analysis.votes"
        ).fetchone()[0]
    finally:
        con.close()

    # Ingest the same file again
    ingest_module.ingest(str(SAMPLES))

    con = duckdb.connect(DB)
    try:
        after_count = con.execute(
            "SELECT COUNT(*) FROM blog_analysis.votes"
        ).fetchone()[0]

        assert after_count == before_count
    finally:
        con.close()