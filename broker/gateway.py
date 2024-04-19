from broker.message_handler import handle
from util.uid import uuid_gen

clients = {}
rooms = {}


def client_exists(name, dict):
    for item in dict.values():
        if item.get('name') == name:
            return True
    return False


def remove_id(dictionary, target_id):
    for key, id_list in dictionary.items():
        if target_id in id_list:
            id_list.remove(target_id)
            return True  # Return True if ID was found and removed
    return False


async def handle_client(websocket, path):

    id = str(uuid_gen())
    print(f"Neue Verbindung hergestellt")


    clients[id] = {"websocket": websocket}
    try:
        async for message in websocket:
            await handle(message, id)

    finally:
        clients.pop(id)
        remove_id(rooms, id)
        print(f"Verbindung geschlossen: {id}")
