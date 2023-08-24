import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms


async def execute(command, id):
    """args["room_id", "column_id", "flightstrip_id", "new_column_id", "position"]"""
    if not verify_command(json.dumps(command), "move_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        new_column_id = command["args"][3]
        position = command["args"][4]

        flightstrip = rooms[room_id][column_id][flightstrip_id]
        del rooms[room_id][column_id]
        rooms[room_id][new_column_id] = flightstrip
        rooms[room_id][new_column_id][flightstrip_id]["position"] = position
        await message_handler.broadcast_without_id(room_id, id, respond("move_flightstrip",
                                                                        [column_id, flightstrip_id, new_column_id,
                                                                         position]))

        print(rooms)
        return True
