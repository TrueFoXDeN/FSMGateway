import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command


async def execute(command, id):
    """args["roomid", "Name"]"""
    if not verify_command(json.dumps(command), "connect"):
        return False
    else:
        room_id = command["args"][0]
        name = command["args"][1]
        gateway.clients[id]['name'] = name
        if room_id not in gateway.rooms:
            return False
        if id not in gateway.rooms[room_id]:
            gateway.rooms[room_id].append(id)
        print(gateway.rooms)
        await message_handler.broadcast(room_id, respond('connect', [name]))
        return True
