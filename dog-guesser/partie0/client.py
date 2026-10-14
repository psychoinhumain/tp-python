import asyncio
import sys

import websockets


async def main():
    if len(sys.argv) < 2:
        print("Usage : python client.py <message>")
        return
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            await websocket.send(sys.argv[1])
            print(await websocket.recv())
    except OSError:
        print("Impossible de se connecter : le serveur est-il lancé ?")


if __name__ == "__main__":
    asyncio.run(main())
