import json

from broker import gateway, message_handler
from command.command_verifyer import verify_command


async def execute(command, id):
    """args["roomid", "Name"]"""
    if not verify_command(json.dumps(command), "connect"):
        return False
    else:
        gateway.clients[id]['name'] = command['args'][1]
        if command['args'][0] not in gateway.rooms:
            return False
        if id not in gateway.rooms[command['args'][1]]:
            gateway.rooms[command['args'][0]].append(id)
        print(gateway.rooms)
        await message_handler.broadcast(command['args'][0], f"User {gateway.clients[id]['name']} connected to room {command['args'][0]}.")
        return True
