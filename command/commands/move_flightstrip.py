import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "flightstrip_id", "new_column_id", "position"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "move_flightstrip"):
        return False
    else:
        flightstrip = rooms[command["args"][0]][command["args"][1]][command["args"][2]]
        del rooms[command["args"][0]][command["args"][1]]
        rooms[command["args"][0]][command["args"][3]] = flightstrip
        rooms[command["args"][0]][command["args"][3]][command["args"][2]]["position"] = command["args"][4]
        return True