from command.command_handler import handle_command
from broker import gateway


async def handle(command, id):
    res = await handle_command(command, id)
    if not res:
        await gateway.clients[id]["websocket"].send("Command has wrong format")


async def broadcast(msg):
    for client_id in gateway.clients.keys():
        await gateway.clients[client_id]["websocket"].send(msg)
