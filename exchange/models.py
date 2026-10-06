from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class Rate:
    sale: Optional[float]
    purchase: Optional[float]


@dataclass(frozen=True)
class DayRates:
    day: date
    rates: dict[str, Rate]

    @property
    def day_label(self) -> str:
        return self.day.strftime("%d.%m.%Y")
