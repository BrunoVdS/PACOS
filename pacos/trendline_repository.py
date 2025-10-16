"""Persistence layer for trendline configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import database
from .settings import Settings, get_default_trendline_coefficient


@dataclass
class TrendlineRepository:
    """Repository for managing the trendline coefficient."""

    database_path: Optional[str] = None

    def _get_connection(self):
        return database.connect(self.database_path)

    def get_coefficient(self) -> float:
        """Return the active trendline coefficient.

        Falls back to the configured default when the database does not store a
        specific value.
        """

        with database.session(self.database_path) as connection:
            row = connection.execute(
                "SELECT coefficient FROM trendline_settings WHERE id = 1"
            ).fetchone()

        if row is None:
            return get_default_trendline_coefficient()
        return float(row["coefficient"])

    def set_coefficient(self, value: float) -> None:
        """Persist the trendline coefficient for subsequent reads."""

        try:
            coefficient = float(value)
        except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
            raise ValueError("Coefficient must be numeric") from exc

        with database.session(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO trendline_settings (id, coefficient, updated_at)
                VALUES (1, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    coefficient = excluded.coefficient,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (coefficient,),
            )

    def reset_to_default(self) -> None:
        """Remove the stored coefficient to fall back to the default value."""

        with database.session(self.database_path) as connection:
            connection.execute("DELETE FROM trendline_settings WHERE id = 1")

    def get_effective_settings(self) -> Settings:
        """Return a snapshot of the settings used by this repository."""

        settings = Settings.load()
        if self.database_path is not None:
            settings = Settings(
                trendline_default=settings.trendline_default,
                database_path=self.database_path,
            )
        return settings
