import json

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from logic.fsm_handler import order_flightstrips, rooms
from datetime import datetime

async def execute(command, id):
    """args["roomid", "password", "name"]"""
    if not verify_command(json.dumps(command), "connect"):
        return False
    else:
        room_id = command["args"][0]
        password = command["args"][1]
        name = command["args"][2]

        if room_id not in gateway.rooms:
            return False

        if auth.check_password(password, fsm_handler.rooms[room_id]["password"]):
            token = auth.encode_token({'room': room_id})
        else:
            return False

        if id not in gateway.rooms[room_id]:
            gateway.rooms[room_id].append(id)

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        gateway.clients[id]['name'] = name
        data = {'order': order_flightstrips[room_id], 'data': dict(rooms[room_id])}
        del data['data']['password']
        del data['data']['activity']

        client_ids = gateway.rooms[room_id]
        client_names = [gateway.clients[i]["name"] for i in client_ids]

        await message_handler.send(id, respond('token', [token, data]))
        await message_handler.send(id, respond('get_clients', client_names))
        await message_handler.broadcast_without_id(room_id, id, respond('connect', [name]))
        return True
