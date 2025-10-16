"""Domain logic for generating trendlines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .trendline_repository import TrendlineRepository


@dataclass
class TrendlineService:
    """Apply trendline calibration to value series."""

    repository: TrendlineRepository

    def apply(self, values: Sequence[float]) -> List[float]:
        """Scale ``values`` using the current trendline coefficient."""

        coefficient = self.repository.get_coefficient()
        return [float(value) * coefficient for value in values]

    def stream(self, values: Iterable[float]):
        """Yield calibrated values lazily, loading the coefficient per batch."""

        coefficient = self.repository.get_coefficient()
        for value in values:
            yield float(value) * coefficient
