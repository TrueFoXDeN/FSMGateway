import json

from command.commands import connect_command


async def handle_command(command, id):
    try:
        command = json.loads(command)
    except:
        return False
    match command['cmd']:
        case 'connect':
            return await connect_command.execute(command, id)
