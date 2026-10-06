from datetime import datetime
from pathlib import Path

from aiofile import async_open
from aiopath import AsyncPath


class ExchangeLog:
    """Appends a line to a file every time the exchange command is executed."""

    def __init__(self, path: str | Path = "exchange_commands.log"):
        self._path = AsyncPath(path)

    async def record(self, user: str, command: str) -> None:
        if not await self._path.parent.exists():
            await self._path.parent.mkdir(parents=True, exist_ok=True)
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {user} | {command}\n"
        async with async_open(self._path, "a", encoding="utf-8") as file:
            await file.write(line)
