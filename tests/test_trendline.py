from __future__ import annotations

import os
import tempfile
import unittest

from pacos.settings import (
    DEFAULT_TRENDLINE_COEFFICIENT,
    TRENDLINE_COEFFICIENT_ENV_VAR,
)
from pacos.trendline_repository import TrendlineRepository
from pacos.trendline_service import TrendlineService


class TrendlineConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.db_path = self.tmp.name
        os.environ.pop(TRENDLINE_COEFFICIENT_ENV_VAR, None)

    def tearDown(self) -> None:
        os.unlink(self.db_path)

    def test_default_coefficient_used_when_database_empty(self) -> None:
        repository = TrendlineRepository(database_path=self.db_path)
        self.assertEqual(repository.get_coefficient(), DEFAULT_TRENDLINE_COEFFICIENT)

    def test_environment_variable_overrides_default(self) -> None:
        os.environ[TRENDLINE_COEFFICIENT_ENV_VAR] = "2.5"
        repository = TrendlineRepository(database_path=self.db_path)
        self.assertEqual(repository.get_coefficient(), 2.5)

    def test_setting_coefficient_persists_value(self) -> None:
        repository = TrendlineRepository(database_path=self.db_path)
        repository.set_coefficient(3.2)
        self.assertEqual(repository.get_coefficient(), 3.2)

    def test_trendline_updates_immediately_after_setting(self) -> None:
        repository = TrendlineRepository(database_path=self.db_path)
        service = TrendlineService(repository=repository)

        before = service.apply([1, 2, 3])
        repository.set_coefficient(2)
        after = service.apply([1, 2, 3])

        self.assertEqual(before, [1.0, 2.0, 3.0])
        self.assertEqual(after, [2.0, 4.0, 6.0])


if __name__ == "__main__":  # pragma: no cover - test entry point
    unittest.main()
