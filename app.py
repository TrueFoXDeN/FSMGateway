from datetime import datetime, timedelta

from flask import Flask
from flask_cors import CORS
import logging
import asyncio
import websockets

from hypercorn.config import Config
from hypercorn.asyncio import serve

from broker import gateway
from broker.gateway import handle_client
from broker.response_generator import respond
from logic import fsm_handler
from routes.management import management

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = Flask(__name__)
app.register_blueprint(management)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


async def start_api():
    config = Config()
    config.bind = ["0.0.0.0:5002"]
    await serve(app, config)


async def start_websocket():
    async with websockets.serve(handle_client, "", 4000):
        await asyncio.Future()


async def start_pruning():
    while True:
        print('room pruning...')
        rooms_to_delete = []

        for room in fsm_handler.rooms:
            activity = datetime.fromisoformat(fsm_handler.rooms[room]['activity'])
            if datetime.now() > activity + timedelta(hours=1):
                rooms_to_delete.append(room)

                ids = gateway.rooms[room]

                for id in ids:
                    await gateway.clients[id]["websocket"].send(
                        respond('room_closed', ['Room closed due to inactivity']))
                    await gateway.clients[id]['websocket'].close()
                del gateway.rooms[room]
                print(f'room {room} pruned')
        for room in rooms_to_delete:
            del fsm_handler.rooms[room]
            del fsm_handler.order_flightstrips[room]
        await asyncio.sleep(60 * 10)


async def main():
    await asyncio.gather(
        start_api(),
        start_websocket(),
        start_pruning()
    )


if __name__ == '__main__':
    asyncio.run(main())
