import json
from datetime import datetime

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command


async def execute(command, id):
    """args["token", "room_id"]"""
    if not verify_command(json.dumps(command), "get_clients"):
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        if not auth.verify_token(token, room_id):
            return False

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        client_ids = gateway.rooms[room_id]
        client_names = [gateway.clients[i]["name"] for i in client_ids]
        await message_handler.send(id, respond('get_clients', client_names))
        return True
