import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command

# args["room_id"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "get_clients"):
        return False
    else:
        return True