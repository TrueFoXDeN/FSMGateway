import json

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms


async def execute(command, id):
    """args["token", "room_id", "column_id", "flightstrip_id", "status"]"""
    if not verify_command(json.dumps(command), "edit_status"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        flightstrip_id = command["args"][3]
        status = command["args"][4]
        if not auth.verify_token(token, room_id):
            return False

        rooms[room_id][column_id][flightstrip_id]["status"] = status
        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("edit_status", [column_id, flightstrip_id, status]))
        print(rooms)
        return True
