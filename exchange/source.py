from datetime import date
from typing import Protocol

from .models import DayRates


class RateSource(Protocol):
    """Anything able to return the exchange rates for a single day."""

    async def fetch_day(self, day: date, currencies: tuple[str, ...]) -> DayRates: ...
