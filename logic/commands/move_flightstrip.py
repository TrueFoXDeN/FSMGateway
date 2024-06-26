import json
from datetime import datetime

from api import auth
from broker import message_handler
from broker.response_generator import respond
from logic import fsm_handler
from logic.command_verifyer import verify_command
from logs import logger


async def execute(command, id):
    """args["token", "room_id", "column_id", "flightstrip_id", "new_column_id", "position"]"""
    if not verify_command(json.dumps(command), "move_flightstrip"):
        logger.trace('[Move Flightstrip] Command verification failed', command)
        return False
    else:
        token = command["args"][0]
        room_id = command["args"][1]
        column_id = command["args"][2]
        flightstrip_id = command["args"][3]
        new_column_id = command["args"][4]
        position = command["args"][5]
        if not auth.verify_token(token, room_id):
            logger.trace('[Move Flightstrip] Token verification failed', token)
            return False

        fsm_handler.order_flightstrips[room_id][column_id].remove(flightstrip_id)
        fsm_handler.order_flightstrips[room_id][new_column_id].insert(position, flightstrip_id)

        fl = fsm_handler.rooms[room_id][column_id][flightstrip_id]
        del fsm_handler.rooms[room_id][column_id][flightstrip_id]
        fsm_handler.rooms[room_id][new_column_id][flightstrip_id] = fl

        fsm_handler.rooms[room_id]['activity'] = datetime.now().isoformat()

        logger.trace('[Move Flightstrip] Moved Flightstrip',
                     {'column_id': column_id, 'flightstrip_id': flightstrip_id, 'new_column_id': new_column_id,
                      'position': position, 'room': fsm_handler.rooms[room_id],
                      'order': fsm_handler.order_flightstrips[room_id]})

        await message_handler.broadcast_without_id(room_id, id,
                                                   respond("move_flightstrip",
                                                           [column_id, flightstrip_id, new_column_id, position]))

        return True
