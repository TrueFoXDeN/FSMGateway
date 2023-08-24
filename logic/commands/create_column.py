import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms


async def execute(command, id):
    """args["room_id", "column_id", "name", "position"]"""
    if not verify_command(json.dumps(command), "create_column"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        name = command["args"][2]
        position = command["args"][3]
        rooms[room_id][column_id] = {"name": name, "position": position}
        await message_handler.broadcast_without_id(room_id, id, respond("create_column", [column_id, name, position]))

        print(rooms)
        return True
