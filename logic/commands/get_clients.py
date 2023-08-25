import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command


async def execute(command, id):
    """args["room_id"]"""
    if not verify_command(json.dumps(command), "get_clients"):
        print(command)
        return False
    else:
        room_id = command["args"][0]
        print(gateway.rooms[room_id])
        client_ids = gateway.rooms[room_id]
        client_names = [gateway.clients[i]["name"] for i in client_ids]
        await message_handler.send(id, respond('get_clients', [client_names]))
        return True
