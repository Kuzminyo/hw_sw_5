import argparse
import asyncio
import sys

from exchange.errors import ExchangeError
from exchange.formatters import JsonFormatter
from exchange.runner import fetch_rates
from exchange.service import MAX_DAYS


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="PrivatBank EUR/USD exchange rates for the last N days")
    parser.add_argument("days", type=int, help=f"number of days (1..{MAX_DAYS})")
    parser.add_argument(
        "-c", "--currency", nargs="+", default=[], metavar="CODE",
        help="additional currencies, e.g. -c CHF PLN",
    )
    return parser.parse_args(argv)


async def run(days: int, currencies: list[str]) -> int:
    try:
        rates = await fetch_rates(days, tuple(currencies))
    except ExchangeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(JsonFormatter().format(rates))
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(asyncio.run(run(args.days, args.currency)))
