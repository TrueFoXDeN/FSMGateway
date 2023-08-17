import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command
from logic.fsm_handler import rooms


# args["room_id", "column_id", "name", "position"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "create_column"):
        return False
    else:
        rooms[command["args"][0]][command["args"][1]] = {"name": command["args"][2], "position": command["args"][3]}
        print(rooms)
        return True
