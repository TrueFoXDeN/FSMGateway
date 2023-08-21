import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "flightstrip_id"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "delete_flightstrip"):
        return False
    else:
        del rooms[command["args"][0]][command["args"][1]][command["args"][2]]
        return True