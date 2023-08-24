import json

from broker import gateway, message_handler
from broker.response_generator import respond
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


async def execute(command, id):
    """args["room_id", "column_id"]"""
    if not verify_command(json.dumps(command), "delete_column"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        del rooms[room_id][column_id]
        await message_handler.broadcast_without_id(room_id, id, respond("delete_column", [column_id]))

        return True
