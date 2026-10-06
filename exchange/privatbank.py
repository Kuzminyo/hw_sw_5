import asyncio
from datetime import date

import aiohttp

from .errors import ExchangeApiError
from .models import DayRates, Rate

API_URL = "https://api.privatbank.ua/p24api/exchange_rates"


class PrivatBankSource:
    """RateSource backed by the public PrivatBank exchange archive API."""

    def __init__(self, session: aiohttp.ClientSession, url: str = API_URL):
        self._session = session
        self._url = url

    async def fetch_day(self, day: date, currencies: tuple[str, ...]) -> DayRates:
        label = day.strftime("%d.%m.%Y")
        payload = await self._get_json(label)
        return DayRates(day=day, rates=self._parse(payload, currencies, label))

    async def _get_json(self, label: str) -> dict:
        try:
            async with self._session.get(
                self._url, params={"json": "", "date": label}
            ) as response:
                if response.status != 200:
                    raise ExchangeApiError(
                        f"PrivatBank API returned HTTP {response.status} for {label}"
                    )
                return await response.json(content_type=None)
        except asyncio.TimeoutError as exc:
            raise ExchangeApiError(f"Request for {label} timed out") from exc
        except aiohttp.ClientError as exc:
            raise ExchangeApiError(f"Network error while requesting {label}: {exc}") from exc
        except ValueError as exc:
            raise ExchangeApiError(f"Invalid JSON in response for {label}") from exc

    @staticmethod
    def _parse(payload: dict, currencies: tuple[str, ...], label: str) -> dict[str, Rate]:
        if not isinstance(payload, dict) or not isinstance(payload.get("exchangeRate"), list):
            raise ExchangeApiError(f"Unexpected response format for {label}")
        by_code = {
            item.get("currency"): item
            for item in payload["exchangeRate"]
            if isinstance(item, dict)
        }
        result = {}
        for code in currencies:
            item = by_code.get(code)
            if item is None:
                raise ExchangeApiError(f"Currency {code} is not available for {label}")
            result[code] = Rate(sale=item.get("saleRate"), purchase=item.get("purchaseRate"))
        return result
