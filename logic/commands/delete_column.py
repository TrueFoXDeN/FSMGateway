import json
from datetime import datetime

from api import auth
from broker import gateway, message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from logs import logger


async def execute(command, id):
    """args["token", "room_id", "column_id"]"""
    if not verify_command(json.dumps(command), "delete_column"):
        logger.trace('[Delete Column] Command verification failed', command)
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        if not auth.verify_token(token, room_id):
            logger.trace('[Delete Column] Token verification failed', token)
            return False

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        del fsm_handler.rooms[room_id][column_id]
        del fsm_handler.order_flightstrips[room_id][column_id]
        logger.trace('[Delete Column] Column deleted', column_id)
        await message_handler.broadcast_without_id(room_id, id, respond("delete_column", [column_id]))


        return True
