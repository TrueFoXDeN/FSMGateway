import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command

# args["column_id", "flightstrip_id", "type", "position"]
async def execute(command, id):
    if not verify_command(json.dumps(command), "create_flightstrip"):
        return False
    else:
        return True