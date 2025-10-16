"""Database helpers for PACOS analytics components."""

from __future__ import annotations

import contextlib
import sqlite3
from pathlib import Path
from typing import Callable, Iterator, Optional

from .settings import Settings


ConnectionFactory = Callable[[], sqlite3.Connection]


def _initialise_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS trendline_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            coefficient REAL NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def connect(database_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a SQLite connection and ensure required tables exist."""

    settings = Settings.load()
    db_path = Path(database_path or settings.database_path)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    _initialise_schema(connection)
    return connection


@contextlib.contextmanager
def session(database_path: Optional[str] = None) -> Iterator[sqlite3.Connection]:
    """Context manager yielding a database session with initialised schema."""

    connection = connect(database_path=database_path)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()
