import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms



async def execute(command, id):
    """args["room_id", "column_id", "flightstrip_id", "data"]"""
    if not verify_command(json.dumps(command), "edit_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        data = command["args"][3]
        rooms[room_id][column_id][flightstrip_id] = data
        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("edit_flightstrip", [column_id, flightstrip_id, data]))
        print(rooms)
        return True