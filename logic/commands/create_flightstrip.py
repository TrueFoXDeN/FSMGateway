import json
from datetime import datetime

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from util import uid


async def execute(command, id):
    """args["token", "room_id", "column_id", "flightstrip_id", "type"]"""
    if not verify_command(json.dumps(command), "create_flightstrip"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        flightstrip_id = command["args"][3]
        type = command["args"][4]
        if not auth.verify_token(token, room_id):
            return False

        fsm_handler.order_flightstrips[room_id][column_id].append(flightstrip_id)

        fsm_handler.rooms[room_id][column_id][flightstrip_id] = {"type": type}
        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()

        await message_handler.broadcast_without_id(room_id, id, respond("create_flightstrip",
                                                                        [column_id, flightstrip_id, type]))

        return True
