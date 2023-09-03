import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips


async def execute(command, id):
    """args["room_id", "column_id", "flightstrip_id", "new_column_id", "position"]"""
    if not verify_command(json.dumps(command), "move_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        new_column_id = command["args"][3]
        position = int(command["args"][4])

        order_flightstrips[room_id][column_id].remove(flightstrip_id)
        order_flightstrips[room_id][new_column_id].insert(position, flightstrip_id)

        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("move_flightstrip",
                                                           [column_id, flightstrip_id, new_column_id, position]))

        print(rooms)
        print(order_flightstrips)
        return True
