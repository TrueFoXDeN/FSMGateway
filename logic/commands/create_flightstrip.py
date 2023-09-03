import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips
from util import uid


async def execute(command, id):
    """args["room_id", "column_id", "flightstrip_id", "type"]"""
    if not verify_command(json.dumps(command), "create_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        type = command["args"][3]

        order_flightstrips[room_id][column_id].append(flightstrip_id)

        rooms[room_id][column_id][flightstrip_id] = {"type": type}

        await message_handler.broadcast_without_id(room_id, id, respond("create_flightstrip",
                                                                        [column_id, flightstrip_id, type]))
        print(rooms)
        print(order_flightstrips)
        return True
