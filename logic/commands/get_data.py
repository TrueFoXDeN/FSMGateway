import json

from broker import message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_flightstrips


async def execute(command, id):
    """args["room_id"]"""
    if not verify_command(json.dumps(command), "get_data"):
        return False
    else:
        room_id = command["args"][0]
        data = {'order': order_flightstrips[room_id], 'data': rooms[room_id]}
        await message_handler.send(id, respond('get_data', [data]))
        return True
