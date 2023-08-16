import time

from flask import Flask
from flask_cors import CORS
import threading
import logging
import asyncio
import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

app = Flask(__name__)
cors = CORS(app)

clients = []
async def handle_client(websocket, path):
    print("Neue Verbindung hergestellt")
    clients.append(websocket)

    try:
        async for message in websocket:
            print(f"Nachricht empfangen: {message}")
            await websocket.send(f"Du hast gesagt: {message}")


    finally:
        clients.remove(websocket)
        print("Verbindung geschlossen")


def start_api():
    app.run(port=5000)


def start_websocket():
    start_server = websockets.serve(handle_client, "localhost", 4000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    thread_api = threading.Thread(target=start_api, daemon=True).start()
    thread_websocket = threading.Thread(target=start_websocket(), daemon=True).start()

    while True:
        time.sleep(1)
