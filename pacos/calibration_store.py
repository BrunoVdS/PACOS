"""Persistence layer for calibration parameters."""

from __future__ import annotations

from datetime import datetime, timezone

from . import database, settings


TRENDLINE_KEY = "trendline_multiplier"


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_default(connection) -> float:
    """Ensure the default multiplier exists in the database."""

    cursor = connection.execute(
        "SELECT value FROM calibration_settings WHERE key = ?",
        (TRENDLINE_KEY,),
    )
    row = cursor.fetchone()
    if row is not None:
        return float(row["value"])

    default_value = settings.get_settings().trendline_multiplier_default
    connection.execute(
        """
        INSERT INTO calibration_settings(key, value, updated_at)
        VALUES(?, ?, ?)
        """,
        (TRENDLINE_KEY, default_value, _utcnow()),
    )
    connection.commit()
    return default_value


def get_trendline_multiplier(conn=None) -> float:
    """Return the persisted trendline multiplier, creating it if needed."""

    own_connection = False
    if conn is None:
        conn = database.get_connection()
        own_connection = True

    try:
        return _ensure_default(conn)
    finally:
        if own_connection:
            conn.close()


def set_trendline_multiplier(value: float, conn=None) -> None:
    """Persist a new trendline multiplier value."""

    own_connection = False
    if conn is None:
        conn = database.get_connection()
        own_connection = True

    try:
        conn.execute(
            """
            INSERT INTO calibration_settings(key, value, updated_at)
            VALUES(?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (TRENDLINE_KEY, float(value), _utcnow()),
        )
        conn.commit()
    finally:
        if own_connection:
            conn.close()
