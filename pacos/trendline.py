"""Trendline utilities that use the configurable multiplier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

from .calibration_store import get_trendline_multiplier


@dataclass
class TrendlineResult:
    """Result of a linear regression trendline."""

    slope: float
    intercept: float


class TrendlineCalculator:
    """Compute a simple least squares trendline for a sequence of points."""

    @staticmethod
    def _prepare(points: Iterable[Tuple[float, float]]) -> Tuple[Sequence[float], Sequence[float]]:
        xs: list[float] = []
        ys: list[float] = []
        for x, y in points:
            xs.append(float(x))
            ys.append(float(y))
        if not xs:
            raise ValueError("Trendline requires at least one point")
        return xs, ys

    def _compute_slope(self, xs: Sequence[float], ys: Sequence[float]) -> float:
        n = len(xs)
        if n == 1:
            return 0.0
        sum_x = sum(xs)
        sum_y = sum(ys)
        sum_xy = sum(x * y for x, y in zip(xs, ys))
        sum_x2 = sum(x * x for x in xs)
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return 0.0
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        multiplier = get_trendline_multiplier()
        return slope * multiplier

    def calculate(self, points: Iterable[Tuple[float, float]]) -> TrendlineResult:
        xs, ys = self._prepare(points)
        slope = self._compute_slope(xs, ys)
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        intercept = mean_y - slope * mean_x
        return TrendlineResult(slope=slope, intercept=intercept)
