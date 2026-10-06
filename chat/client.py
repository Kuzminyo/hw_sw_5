import asyncio

from websockets.asyncio.client import connect

from .server import HOST, PORT


async def receive(ws) -> None:
    async for message in ws:
        print(message)


async def main() -> None:
    async with connect(f"ws://{HOST}:{PORT}") as ws:
        reader = asyncio.create_task(receive(ws))
        loop = asyncio.get_running_loop()
        while not reader.done():
            line = await loop.run_in_executor(None, input)
            await ws.send(line)
        await reader


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        pass
