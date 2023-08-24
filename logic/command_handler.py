import json

from logic.commands import connect, create_column, create_flightstrip, delete_column, delete_flightstrip, \
    edit_flightstrip, edit_status, get_clients, get_data, move_flightstrip


async def handle_command(command, id):
    try:
        print(command)
        command = json.loads(command)
    except:
        return False
    match command['cmd']:
        case 'connect':
            return await connect.execute(command, id)
        case 'create_column':
            return await create_column.execute(command, id)
        case 'create_flightstrip':
            return await create_flightstrip.execute(command, id)
        case 'delete_column':
            return await delete_column.execute(command, id)
        case 'delete_flightstrip':
            return await delete_flightstrip.execute(command, id)
        case 'edit_flightstrip':
            return await edit_flightstrip.execute(command, id)
        case 'edit_status':
            return await edit_status.execute(command, id)
        case 'get_clients':
            return await get_clients.execute(command, id)
        case 'get_data':
            return await get_data.execute(command, id)
        case 'move_flightstrip':
            return await move_flightstrip.execute(command, id)
