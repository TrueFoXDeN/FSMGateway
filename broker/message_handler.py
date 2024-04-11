import json

from broker.response_generator import respond
from logic import fsm_handler
from logic.command_handler import handle_command
from broker import gateway


async def handle(command, id):
    res = False
    try:
        command = json.loads(command)
        try:
            if command['cmd'] == 'connect':
                res = await handle_command(command, id)
                if not res:
                    await gateway.clients[id]["websocket"].send(respond('error_connect', ['Wrong room or password']))
                    await gateway.clients[id]['websocket'].close()

            else:
                res = await handle_command(command, id)
                if not res:
                    data = {'order': fsm_handler.order_flightstrips[command['args'][1]], 'data': dict(fsm_handler.rooms[command['args'][1]])}
                    del data['data']['password']
                    await gateway.clients[id]["websocket"].send(respond('error',
                                                                        ['Command not accepted', data]))
        except Exception as e:
            data = {'order': fsm_handler.order_flightstrips[command['args'][1]], 'data': dict(fsm_handler.rooms[command['args'][1]])}
            del data['data']['password']
            await gateway.clients[id]["websocket"].send(respond('error', ['Command caused an exception', data]))

    except Exception as e:
        await gateway.clients[id]["websocket"].send(respond('error', ['Command has wrong format', str(e)]))


async def broadcast(room_id, msg):
    for client_id in gateway.rooms[room_id]:
        await gateway.clients[client_id]["websocket"].send(msg)


async def broadcast_without_id(room_id, id, msg):
    for client_id in gateway.rooms[room_id]:
        if client_id != id:
            await gateway.clients[client_id]["websocket"].send(msg)


async def send(id, msg):
    await gateway.clients[id]["websocket"].send(msg)
