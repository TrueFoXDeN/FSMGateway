from logic.commands import connect, create_column, create_flightstrip, delete_column, delete_flightstrip, \
    edit_flightstrip, get_clients, get_data, move_flightstrip
from logs import logger


async def handle_command(command, id):
    match command['cmd']:
        case 'connect':
            logger.trace('[Connect] Command executed')
            return await connect.execute(command, id)
        case 'create_column':
            logger.trace('[Create Column] Command executed')
            return await create_column.execute(command, id)
        case 'create_flightstrip':
            logger.trace('[Create Flightstrip] Command executed')
            return await create_flightstrip.execute(command, id)
        case 'delete_column':
            logger.trace('[Delete Column] Command executed')
            return await delete_column.execute(command, id)
        case 'delete_flightstrip':
            logger.trace('[Delete Flightstrip] Command executed')
            return await delete_flightstrip.execute(command, id)
        case 'edit_flightstrip':
            logger.trace('[Edit Flightstrip] Command executed')
            return await edit_flightstrip.execute(command, id)
        case 'get_clients':
            logger.trace('[Get Clients] Command executed')
            return await get_clients.execute(command, id)
        case 'get_data':
            logger.trace('[Get Data] Command executed')
            return await get_data.execute(command, id)
        case 'move_flightstrip':
            logger.trace('[Move Flightstrip] Command executed')
            return await move_flightstrip.execute(command, id)
