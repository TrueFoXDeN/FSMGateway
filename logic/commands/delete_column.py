import json

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips


async def execute(command, id):
    """args["token", "room_id", "column_id"]"""
    if not verify_command(json.dumps(command), "delete_column"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        if not auth.verify_token(token, room_id):
            return False

        del rooms[room_id][column_id]
        del order_flightstrips[room_id][column_id]
        await message_handler.broadcast_without_id(room_id, id, respond("delete_column", [column_id]))
        print(rooms)

        return True
