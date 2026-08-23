"""Database helper for the exercise.

Provides a small convenience wrapper for creating a connection to the
persistent DuckDB database file `warehouse.db` used by the tests and
exercise scripts.
"""
from __future__ import annotations

import duckdb
from typing import Any


DB_PATH = "warehouse.db"


def get_connection(**kwargs: Any) -> duckdb.DuckDBPyConnection:
    """Return a duckdb connection to the persistent warehouse DB.

    Any kwargs are forwarded to duckdb.connect(...).
    """
    return duckdb.connect(DB_PATH, **kwargs)
