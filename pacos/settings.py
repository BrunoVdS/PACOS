"""Application settings for PACOS.

The module reads configuration from environment variables while providing
sensible defaults that work out of the box. The trendline multiplier can be
configured through the ``PACOS_TRENDLINE_DEFAULT`` environment variable and the
SQLite database location through ``PACOS_DB_PATH``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


def _parse_float(value: str | None, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    """Centralised configuration container."""

    trendline_multiplier_default: float
    database_path: Path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return application settings, loading them from the environment."""

    default_multiplier = _parse_float(
        os.environ.get("PACOS_TRENDLINE_DEFAULT"),
        1.0,
    )
    database_path = Path(os.environ.get("PACOS_DB_PATH", "data/pacos.sqlite3"))
    return Settings(
        trendline_multiplier_default=default_multiplier,
        database_path=database_path,
    )


def reload_settings() -> None:
    """Clear the cached settings instance to re-read environment variables."""

    get_settings.cache_clear()
