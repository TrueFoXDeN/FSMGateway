import json

from broker import gateway, message_handler
from broker.response_generator import respond
from logic.command_verifyer import verify_command
from logic.fsm_handler import rooms, order_columns, order_flightstrips


async def execute(command, id):
    """args["room_id", "column_id", "name", "position"]"""
    if not verify_command(json.dumps(command), "create_column"):
        return False
    else:
        room_id = command["args"][0]
        column_id = command["args"][1]
        name = command["args"][2]
        position = command["args"][3]
        rooms[room_id][column_id] = {"name": name}
        order_columns[room_id].insert(int(position), column_id)
        order_flightstrips[room_id][column_id] = []
        await message_handler.broadcast_without_id(room_id, id, respond("create_column", [column_id, name, position]))

        print(rooms)
        print(order_columns)
        print(order_flightstrips)
        return True
