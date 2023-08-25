import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms
from util import uid


async def execute(command, id):
    """args["room_id", "column_id", "flightstrip_id", "type", "position"]"""
    if not verify_command(json.dumps(command), "create_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        type = command["args"][3]
        position = command["args"][4]

        positions = [int(flightstrip["position"]) for flightstrip in rooms[room_id][column_id].values() if
                     isinstance(flightstrip, dict) and "position" in flightstrip]

        if len(positions) > 0:
            max_position = max(positions) + 1
            if position != max_position:
                position = max_position
                await message_handler.send(id, respond('edit_position', [flightstrip_id, max_position]))

        rooms[room_id][column_id][flightstrip_id] = {"type": type, "position": position}

        await message_handler.broadcast_without_id(room_id, id, respond("create_flightstrip",
                                                                        [column_id, flightstrip_id, type, position]))
        print(rooms)
        return True
