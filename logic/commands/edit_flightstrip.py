import json
from datetime import datetime

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command


async def execute(command, id):
    """args["token", "room_id", "column_id", "flightstrip_id", "data"]"""
    if not verify_command(json.dumps(command), "edit_flightstrip"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        flightstrip_id = command["args"][3]
        data = command["args"][4]
        if not auth.verify_token(token, room_id):
            return False

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        fsm_handler.rooms[room_id][column_id][flightstrip_id] = data
        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("edit_flightstrip", [column_id, flightstrip_id, data]))
        return True
