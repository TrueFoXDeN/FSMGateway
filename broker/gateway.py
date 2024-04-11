from broker.message_handler import handle
from util.uid import uuid_gen

clients = {}
rooms = {}


def client_exists(ip, dict):
    for item in dict.values():
        if item.get('ip') == ip:
            return True
    return False


def remove_id(dictionary, target_id):
    for key, id_list in dictionary.items():
        if target_id in id_list:
            id_list.remove(target_id)
            return True  # Return True if ID was found and removed
    return False


async def handle_client(websocket, path):
    ip = websocket.remote_address[0]
    id = str(uuid_gen())
    print(f"Neue Verbindung hergestellt: {ip}")

    if client_exists(ip, clients):
        print(f"Client {ip} already connected.")
        await websocket.send(f"Client already Connected")
        await websocket.close()

    clients[id] = {"websocket": websocket, "ip": ip}
    try:
        async for message in websocket:
            await handle(message, id)

    finally:
        clients.pop(id)
        remove_id(rooms, id)
        print(f"Verbindung geschlossen: {id}")
