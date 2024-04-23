from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from flask import Flask
from flask_cors import CORS
# import logging
import asyncio
import websockets

from waitress import serve

from broker import gateway
from broker.gateway import handle_client
from broker.response_generator import respond
from logic import fsm_handler
from logs import logger
from routes.management import management

app = Flask(__name__)
app.register_blueprint(management)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


async def start_api():
    logger.info("Starting API")
    serve(app, port=5002, host='0.0.0.0', url_scheme='https')
    while True:
        await asyncio.sleep(10)


async def start_websocket():
    logger.info("Starting Websocket")
    async with websockets.serve(handle_client, "", 4000):
        await asyncio.Future()


async def start_pruning():
    logger.info("Starting Room Pruning")
    while True:
        rooms_to_delete = []

        for room in fsm_handler.rooms:
            if 'activity' in fsm_handler.rooms[room]:
                activity = datetime.fromisoformat(fsm_handler.rooms[room]['activity'])
                if datetime.now() > activity + timedelta(hours=1):
                    rooms_to_delete.append(room)

                    ids = gateway.rooms[room]

                    for id in ids:
                        await gateway.clients[id]["websocket"].send(
                            respond('room_closed', ['Room closed due to inactivity']))
                        await gateway.clients[id]['websocket'].close()
                    del gateway.rooms[room]
                    logger.info(f'Room {room} pruned')
        for room in rooms_to_delete:
            del fsm_handler.rooms[room]
            del fsm_handler.order_flightstrips[room]
        await asyncio.sleep(60 * 10)


def run_async_function(coroutine):
    asyncio.run(coroutine)


def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(run_async_function, start_api())
        executor.submit(run_async_function, start_websocket())
        executor.submit(run_async_function, start_pruning())


if __name__ == '__main__':
    logger.info("Gateway started")
    main()
