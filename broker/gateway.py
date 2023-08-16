from broker.message_handler import handle
from util.uid import uuid_gen

clients = {}


def client_exists(ip, dict):
    for item in dict.values():
        if item.get('ip') == ip:
            return True
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
        print(clients)
        print(f"Verbindung geschlossen: {id}")
