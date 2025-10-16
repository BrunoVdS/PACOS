"""Simple CLI for interacting with the trendline configuration."""

from __future__ import annotations

import argparse
from typing import Sequence

from .trendline_repository import TrendlineRepository
from .trendline_service import TrendlineService


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="Display the active coefficient")

    set_parser = subparsers.add_parser("set", help="Persist a new coefficient")
    set_parser.add_argument("coefficient", type=float, help="New coefficient value")

    simulate_parser = subparsers.add_parser(
        "simulate", help="Apply the trendline to a comma separated series"
    )
    simulate_parser.add_argument(
        "values",
        type=str,
        help="Comma separated list of numeric values to calibrate",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _create_parser()
    args = parser.parse_args(argv)

    repository = TrendlineRepository()

    if args.command == "show":
        print(repository.get_coefficient())
        return 0

    if args.command == "set":
        repository.set_coefficient(args.coefficient)
        print(f"Trendline coefficient updated to {args.coefficient}")
        return 0

    if args.command == "simulate":
        values = [float(item) for item in args.values.split(",") if item.strip()]
        service = TrendlineService(repository=repository)
        result = service.apply(values)
        print(",".join(f"{value:.4f}" for value in result))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
