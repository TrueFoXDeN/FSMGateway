import json

from broker import gateway, message_handler
from broker.message_handler import send
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "get_data"):
        return False
    else:
        await send(id, rooms[command["args"][0]])
        return True