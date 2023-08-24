import json

from broker import gateway, message_handler
from broker.response_generator import respond
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "flightstrip_id", "type", "position"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "create_flightstrip"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        flightstrip_id = command["args"][2]
        type = command["args"][3]
        position = command["args"][4]

        rooms[room_id][column_id][flightstrip_id] = {"type": type, "position": position}
        await message_handler.broadcast_without_id(room_id, id, respond("create_flightstrip",
                                                                        [column_id, flightstrip_id, type, position]))
        print(rooms)
        return True
