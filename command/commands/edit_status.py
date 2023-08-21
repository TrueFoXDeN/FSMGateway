import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "flightstrip_id", "status"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "edit_status"):
        return False
    else:
        rooms[command["args"][0]][command["args"][1]][command["args"][2]]["status"] = command["args"][3]
        return True