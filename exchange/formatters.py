import json

from .models import DayRates


def to_data(days: list[DayRates]) -> list[dict]:
    return [
        {
            d.day_label: {
                code: {"sale": rate.sale, "purchase": rate.purchase}
                for code, rate in d.rates.items()
            }
        }
        for d in days
    ]


class JsonFormatter:
    def format(self, days: list[DayRates]) -> str:
        return json.dumps(to_data(days), indent=2, ensure_ascii=False)


class TextFormatter:
    """Human friendly format used by the chat."""

    def format(self, days: list[DayRates]) -> str:
        lines = []
        for d in days:
            lines.append(d.day_label)
            for code, rate in d.rates.items():
                lines.append(f"  {code}: buy {_fmt(rate.purchase)} / sell {_fmt(rate.sale)}")
        return "\n".join(lines)


def _fmt(value) -> str:
    return "n/a" if value is None else f"{value:.2f}"
