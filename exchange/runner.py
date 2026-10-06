import aiohttp

from .privatbank import PrivatBankSource
from .service import ExchangeService

REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=15)


async def fetch_rates(days: int, extra_currencies: tuple[str, ...] = ()):
    """Open a session, fetch the rates and close the session again."""
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        service = ExchangeService(PrivatBankSource(session))
        return await service.get_rates(days, extra_currencies)

