from __future__ import annotations

import os

import pytest

from pacos import calibration_store, settings, trendline


@pytest.fixture(autouse=True)
def reset_settings(monkeypatch, tmp_path):
    db_path = tmp_path / "pacos.sqlite3"
    monkeypatch.setenv("PACOS_DB_PATH", str(db_path))
    if "PACOS_TRENDLINE_DEFAULT" in os.environ:
        monkeypatch.delenv("PACOS_TRENDLINE_DEFAULT", raising=False)
    settings.reload_settings()
    yield
    settings.reload_settings()


def test_default_multiplier_seeded(tmp_path):
    conn = calibration_store.database.get_connection(tmp_path / "db.sqlite3")
    try:
        value = calibration_store.get_trendline_multiplier(conn)
        assert value == settings.get_settings().trendline_multiplier_default
    finally:
        conn.close()


def test_multiplier_updates_immediately(monkeypatch):
    calc = trendline.TrendlineCalculator()
    initial = calc.calculate([(0, 0), (1, 1)]).slope
    assert initial == pytest.approx(1.0)

    calibration_store.set_trendline_multiplier(2.0)
    updated = calc.calculate([(0, 0), (1, 1)]).slope
    assert updated == pytest.approx(2.0)


def test_environment_default_used(monkeypatch):
    monkeypatch.setenv("PACOS_TRENDLINE_DEFAULT", "3.5")
    settings.reload_settings()
    calc = trendline.TrendlineCalculator()
    slope = calc.calculate([(0, 0), (1, 1)]).slope
    assert slope == pytest.approx(3.5)
