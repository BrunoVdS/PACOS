"""Database helpers for PACOS."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .settings import get_settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS calibration_settings (
    key TEXT PRIMARY KEY,
    value REAL NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def _ensure_parent_directory(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def get_database_path() -> Path:
    """Return the path to the SQLite database file."""

    return get_settings().database_path


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    """Open a SQLite connection, initialising the schema if necessary."""

    db_path = path or get_database_path()
    _ensure_parent_directory(db_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    initialize(connection)
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    """Initialise the database schema."""

    connection.executescript(SCHEMA)
    connection.commit()


@contextmanager
def get_connection_context(path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Context manager that yields a SQLite connection."""

    connection = get_connection(path)
    try:
        yield connection
    finally:
        connection.close()
