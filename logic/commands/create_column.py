import json
from datetime import datetime

from api import auth
from broker import message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from logs import logger


async def execute(command, id):
    """args["token", "room_id", "column_id", "name"]"""
    if not verify_command(json.dumps(command), "create_column"):
        logger.trace('[Create Column] Command verification failed', command)
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        name = command["args"][3]
        if not auth.verify_token(token, room_id):
            logger.trace('[Create Column] Token verification failed', token)
            return False

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        fsm_handler.rooms[room_id][column_id] = {"name": name}
        fsm_handler.order_flightstrips[room_id][column_id] = []
        logger.trace('[Create Column] Column created', {"created": column_id,
                                                        "room": fsm_handler.rooms[room_id],
                                                        "order": fsm_handler.order_flightstrips[room_id]})
        await message_handler.broadcast_without_id(room_id, id, respond("create_column", [column_id, name]))
        return True
