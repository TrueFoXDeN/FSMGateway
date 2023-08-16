from auth.commands import verify_command, handle_command
from broker import gateway


async def handle(command, id):
    res = handle_command(command, id)
    if not res:
        await gateway.clients[id]["websocket"].send("Command has wrong format")
    # if not verify_command(command, "base"):
    #     await gateway.clients[id]["websocket"].send("Command has wrong format")
    # else:
    #     handle_command(command, id)
