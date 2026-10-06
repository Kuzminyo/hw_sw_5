from exchange.errors import ExchangeError
from exchange.formatters import TextFormatter
from exchange.runner import fetch_rates
from exchange.service import MAX_DAYS

USAGE = f"Usage: exchange [days 1..{MAX_DAYS}] [extra currencies, e.g. CHF PLN]"


async def handle_exchange(args: list[str]) -> str:
    """Execute `exchange [days] [CUR ...]` and return the text to show in chat."""
    days = 1
    if args and args[0].isdigit():
        days = int(args[0])
        args = args[1:]
    if any(not (a.isalpha() and len(a) == 3) for a in args):
        return USAGE
    try:
        rates = await fetch_rates(days, tuple(args))
    except ExchangeError as exc:
        return f"Error: {exc}"
    return TextFormatter().format(rates)
