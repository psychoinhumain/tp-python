import asyncio

import websockets


async def handler(websocket):
    async for message in websocket:
        print(f"Message reçu : {message}")
        count = message.count("b")
        await websocket.send(f'{count} caractère(s) "b"')


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serveur WebSocket lancé sur ws://localhost:8765")
        await asyncio.Future()  # tourne indéfiniment


if __name__ == "__main__":
    asyncio.run(main())
