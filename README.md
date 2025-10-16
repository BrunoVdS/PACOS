# PACOS

Configurable trendline management for the PACOS analytics stack.

## Trendline configuration

The application reads the trendline coefficient from environment variables and
persists overrides in a SQLite database. By default the coefficient is set to
`1.0`, but it can be customised without modifying any source code.

1. Configure a default via environment variables:

   ```bash
   export TRENDLINE_COEFFICIENT_DEFAULT=1.15
   export PACOS_DB_PATH=/tmp/pacos.db  # optional custom database location
   ```

2. Use the CLI helper to inspect or update the active coefficient:

   ```bash
   python -m pacos.cli show
   python -m pacos.cli set 1.35
   python -m pacos.cli simulate 10,20,30
   ```

   Updating the coefficient updates the stored value immediately, and any
   subsequent graph rendering reuses the new value at runtime.

## Tests

Run the unit tests with:

```bash
python -m unittest discover -s tests
```
