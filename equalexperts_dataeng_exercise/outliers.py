"""Outlier detection entry point.

Creates the blog_analysis.outlier_weeks view and prints its contents.
"""

import duckdb

from equalexperts_dataeng_exercise.scripts.exercise import run_query


DB_PATH = "warehouse.db"


def create_outlier_weeks_view(db_path: str = DB_PATH) -> None:
    conn = duckdb.connect(db_path)

    try:
        conn.execute("""
            CREATE SCHEMA IF NOT EXISTS blog_analysis
        """)

        conn.execute("""
            CREATE OR REPLACE VIEW blog_analysis.outlier_weeks AS

            WITH weekly_votes AS (
                SELECT
                    YEAR(CreationDate) AS Year,
                    CAST(strftime(CreationDate, '%U') AS INTEGER) - 1 AS WeekNumber,
                    COUNT(*) AS VoteCount
                FROM blog_analysis.votes
                GROUP BY
                    YEAR(CreationDate),
                    CAST(strftime(CreationDate, '%U') AS INTEGER) - 1
            ),

            weekly_with_average AS (
                SELECT
                    Year,
                    WeekNumber,
                    VoteCount,
                    AVG(VoteCount) OVER () AS AverageVoteCount
                FROM weekly_votes
            )

            SELECT
                Year,
                WeekNumber,
                VoteCount
            FROM weekly_with_average
            WHERE ABS(1 - VoteCount / AverageVoteCount) > 0.2
            ORDER BY
                Year,
                WeekNumber
        """)

    finally:
        conn.close()


def main() -> None:
    create_outlier_weeks_view()

    run_query("""
        SELECT
            Year,
            WeekNumber,
            VoteCount
        FROM blog_analysis.outlier_weeks
    """)


if __name__ == "__main__":
    main()