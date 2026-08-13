import asyncio

import websockets


async def main():
    print("Connecting...")
    async with websockets.connect("ws://127.0.0.1:8000/ws/chat") as ws:
        print("CONNECTED")
        await ws.send("ping")
        try:
            message = await asyncio.wait_for(
                ws.recv(),
                timeout=5,
            )
            print("RECEIVED:", message)
        except TimeoutError:
            print("NO_MESSAGE")


asyncio.run(main())
