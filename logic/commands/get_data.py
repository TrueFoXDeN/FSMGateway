import json
from datetime import datetime

from api import auth
from broker import message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from logs import logger


async def execute(command, id):
    """args["token", "room_id"]"""
    if not verify_command(json.dumps(command), "get_data"):
        logger.trace('[Get Data] Command verification failed', command)
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        if not auth.verify_token(token, room_id):
            logger.trace('[Get Data] Token verification failed', token)
            return False

        data = {'order': fsm_handler.order_flightstrips[room_id], 'data': dict(fsm_handler.rooms[room_id])}
        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()
        del data['data']['password']
        del data['data']['activity']
        logger.trace('[Get Data] Data gathered', data)
        await message_handler.send(id, respond('get_data', ['', data]))
        return True
