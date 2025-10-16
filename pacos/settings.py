"""Application settings for analytics components."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_TRENDLINE_COEFFICIENT: float = 1.0
TRENDLINE_COEFFICIENT_ENV_VAR = "TRENDLINE_COEFFICIENT_DEFAULT"
DATABASE_PATH_ENV_VAR = "PACOS_DB_PATH"
DEFAULT_DATABASE_FILENAME = "pacos.db"


def _coerce_float(value: Optional[str]) -> Optional[float]:
    """Convert a string to ``float`` if possible.

    Returns ``None`` when ``value`` is empty or cannot be coerced.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the analytics stack."""

    trendline_default: float = DEFAULT_TRENDLINE_COEFFICIENT
    database_path: str = DEFAULT_DATABASE_FILENAME

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment variables with sensible defaults."""

        trendline_default = _coerce_float(os.getenv(TRENDLINE_COEFFICIENT_ENV_VAR))
        database_path = os.getenv(DATABASE_PATH_ENV_VAR) or DEFAULT_DATABASE_FILENAME

        return cls(
            trendline_default=trendline_default
            if trendline_default is not None
            else DEFAULT_TRENDLINE_COEFFICIENT,
            database_path=database_path,
        )


def get_default_trendline_coefficient() -> float:
    """Return the configured default trendline coefficient.

    This helper mirrors the behaviour of :meth:`Settings.load` for callers that only
    require access to the default coefficient.
    """

    return Settings.load().trendline_default
