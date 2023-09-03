import json

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command


async def execute(command, id):
    """args["roomid", "password", "name"]"""
    if not verify_command(json.dumps(command), "connect"):
        return False
    else:
        room_id = command["args"][0]
        password = command["args"][1]
        name = command["args"][2]
        print(password, fsm_handler.rooms[room_id]["password"])
        if auth.check_password(password, fsm_handler.rooms[room_id]["password"]):
            token = auth.encode_token({'room': room_id})
            print(token)
        else:
            return False
        gateway.clients[id]['name'] = name
        if room_id not in gateway.rooms:
            return False
        if id not in gateway.rooms[room_id]:
            gateway.rooms[room_id].append(id)
        print(gateway.rooms)
        await message_handler.send(id, respond('token', [token]))
        await message_handler.broadcast_without_id(room_id, id, respond('connect', [name]))
        return True
