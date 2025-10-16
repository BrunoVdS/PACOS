"""CLI utility to update the trendline multiplier."""

from __future__ import annotations

import argparse

from pacos.calibration_store import set_trendline_multiplier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "value",
        type=float,
        help="New trendline multiplier value",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_trendline_multiplier(args.value)
    print(f"Trendline multiplier updated to {args.value}")


if __name__ == "__main__":
    main()
