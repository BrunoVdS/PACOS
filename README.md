# PACOS

Database Pacos

## Trendline configuration

The project now persists the trendline multiplier in SQLite so analysts can
adjust the calibration without editing any Python source files. The default
multiplier is ``1.0`` but it can be overridden via the ``PACOS_TRENDLINE_DEFAULT``
environment variable or by running the helper script:

```bash
python -m scripts.set_trendline_multiplier 1.25
```

Every call to :class:`pacos.trendline.TrendlineCalculator` reads the multiplier
from the database at runtime, so updated values are used immediately.

Set ``PACOS_DB_PATH`` to control the location of the SQLite database. The
default is ``data/pacos.sqlite3``.
