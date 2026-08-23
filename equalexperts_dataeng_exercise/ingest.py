"""Incremental ingestion of vote data into DuckDB."""

import sys
from pathlib import Path
import duckdb


DB_PATH = "warehouse.db"


def _escape_path(path: str) -> str:
    return path.replace("'", "''")


def ingest(file_path: str, db_path: str = DB_PATH) -> None:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    conn = duckdb.connect(db_path)

    try:
        conn.execute("""
            CREATE SCHEMA IF NOT EXISTS blog_analysis
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS blog_analysis.votes (
                Id BIGINT PRIMARY KEY,
                PostId BIGINT,
                VoteTypeId INTEGER,
                CreationDate TIMESTAMP
            )
        """)

        path_sql = _escape_path(str(path))

        conn.execute(f"""
            CREATE OR REPLACE TEMPORARY TABLE votes_temp AS
            SELECT
                CAST(Id AS BIGINT) AS Id,
                CAST(PostId AS BIGINT) AS PostId,
                CAST(VoteTypeId AS INTEGER) AS VoteTypeId,
                CAST(CreationDate AS TIMESTAMP) AS CreationDate
            FROM read_json_auto('{path_sql}')
        """)

        conn.execute("""
            INSERT INTO blog_analysis.votes (
                Id,
                PostId,
                VoteTypeId,
                CreationDate
            )
            SELECT
                Id,
                PostId,
                VoteTypeId,
                CreationDate
            FROM votes_temp
            ON CONFLICT (Id) DO UPDATE SET
                PostId = EXCLUDED.PostId,
                VoteTypeId = EXCLUDED.VoteTypeId,
                CreationDate = EXCLUDED.CreationDate
        """)

    finally:
        conn.close()


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print(
            "Usage: python -m "
            "equalexperts_dataeng_exercise.ingest "
            "<path_to_jsonl>"
        )
        raise SystemExit(1)

    ingest(argv[0])


if __name__ == "__main__":
    main()