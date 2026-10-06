import asyncio
import logging

import websockets
from websockets.asyncio.server import ServerConnection, serve

from .commands import handle_exchange
from .exchange_log import ExchangeLog

logging.basicConfig(level=logging.INFO)

HOST, PORT = "localhost", 8765


class ChatServer:
    def __init__(self, exchange_log: ExchangeLog):
        self._clients: dict[ServerConnection, str] = {}
        self._log = exchange_log

    async def handler(self, ws: ServerConnection) -> None:
        await ws.send("Enter your name:")
        name = (await ws.recv()).strip() or "anonymous"
        self._clients[ws] = name
        await self.broadcast(f"* {name} joined the chat")
        try:
            async for message in ws:
                await self.process(name, message.strip())
        except websockets.ConnectionClosed:
            pass
        finally:
            del self._clients[ws]
            await self.broadcast(f"* {name} left the chat")

    async def process(self, name: str, message: str) -> None:
        if not message:
            return
        await self.broadcast(f"{name}: {message}")
        parts = message.split()
        if parts[0].lower() == "exchange":
            await self._log.record(name, message)
            await self.broadcast(await handle_exchange(parts[1:]))

    async def broadcast(self, text: str) -> None:
        if self._clients:
            websockets.broadcast(set(self._clients), text)


async def main() -> None:
    server = ChatServer(ExchangeLog())
    async with serve(server.handler, HOST, PORT):
        logging.info("Chat server started on ws://%s:%s", HOST, PORT)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
