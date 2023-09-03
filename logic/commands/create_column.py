import json

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips


async def execute(command, id):
    """args["token", "room_id", "column_id", "name"]"""
    if not verify_command(json.dumps(command), "create_column"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        name = command["args"][3]
        if not auth.verify_token(token, room_id):
            return False

        rooms[room_id][column_id] = {"name": name}
        order_flightstrips[room_id][column_id] = []
        await message_handler.broadcast_without_id(room_id, id, respond("create_column", [column_id, name]))

        print(rooms)
        print(order_flightstrips)
        return True
