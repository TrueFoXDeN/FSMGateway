import os
import json
from json_schema import json_schema

from broker import gateway

schemas = {"init": open(os.path.join(os.path.dirname(__file__), "schemas/init.schema"), "r").read()}


def verify_command(command, schema):
    return json_schema.match(command, schemas[schema])


def handle_command(command, id):
    try:
        command = json.loads(command)
    except:
        return False
    match command['cmd']:
        case 'init':
            return init_command(command, id)


def init_command(command, id):
    if not verify_command(json.dumps(command), "init"):
        return False
    else:

        gateway.clients[id]['name'] = command['args'][0]
        gateway.clients[id]['room'] = command['args'][1]
        print(gateway.clients)
        return True
