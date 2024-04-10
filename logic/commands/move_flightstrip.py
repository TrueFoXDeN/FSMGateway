import json

from api import auth
from broker import message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips


async def execute(command, id):
    """args["token", "room_id", "column_id", "flightstrip_id", "new_column_id", "position"]"""
    if not verify_command(json.dumps(command), "move_flightstrip"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        flightstrip_id = command["args"][3]
        new_column_id = command["args"][4]
        position = command["args"][5]
        if not auth.verify_token(token, room_id):
            return False

        order_flightstrips[room_id][column_id].remove(flightstrip_id)
        order_flightstrips[room_id][new_column_id].insert(position, flightstrip_id)

        fl = rooms[room_id][column_id][flightstrip_id]
        del rooms[room_id][column_id][flightstrip_id]
        rooms[room_id][new_column_id][flightstrip_id] = fl

        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("move_flightstrip",
                                                           [column_id, flightstrip_id, new_column_id, position]))

        print(rooms)
        print(order_flightstrips)
        return True
