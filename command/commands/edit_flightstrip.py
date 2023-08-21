import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "flightstrip_id", "data"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "edit_flightstrip"):
        return False
    else:
        rooms[command["args"][0]][command["args"][1]][command["args"][2]] = command["args"][3]
        return True