import json

from broker import message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms


async def execute(command, id):
    """args["room_id"]"""
    if not verify_command(json.dumps(command), "get_data"):
        return False
    else:
        room_id = command["args"][0]
        await message_handler.send(id, respond('get_data', [rooms[room_id]]))
        return True