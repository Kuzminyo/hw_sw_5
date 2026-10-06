import asyncio
from datetime import date, timedelta
from typing import Optional

from .errors import InvalidDaysError
from .models import DayRates
from .source import RateSource

DEFAULT_CURRENCIES = ("EUR", "USD")
MAX_DAYS = 10


class ExchangeService:
    """Collects rates for the last N days (today included, newest first)."""

    def __init__(self, source: RateSource, max_days: int = MAX_DAYS):
        self._source = source
        self._max_days = max_days

    async def get_rates(
        self,
        days: int = 1,
        extra_currencies: tuple[str, ...] = (),
        today: Optional[date] = None,
    ) -> list[DayRates]:
        if not 1 <= days <= self._max_days:
            raise InvalidDaysError(f"Days must be between 1 and {self._max_days}, got {days}")
        today = today or date.today()
        currencies = tuple(dict.fromkeys(DEFAULT_CURRENCIES + tuple(c.upper() for c in extra_currencies)))
        requested = [today - timedelta(days=offset) for offset in range(days)]
        return list(
            await asyncio.gather(*(self._source.fetch_day(d, currencies) for d in requested))
        )
