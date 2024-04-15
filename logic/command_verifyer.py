import os
from json_schema import json_schema

schemas = {"connect": open(os.path.join(os.path.dirname(__file__), "schemas/connect.schema"), "r").read(),
           "create_column": open(os.path.join(os.path.dirname(__file__), "schemas/create_column.schema"), "r").read(),
           "create_flightstrip": open(os.path.join(os.path.dirname(__file__), "schemas/create_flightstrip.schema"), "r").read(),
           "delete_column": open(os.path.join(os.path.dirname(__file__), "schemas/delete_column.schema"), "r").read(),
           "delete_flightstrip": open(os.path.join(os.path.dirname(__file__), "schemas/delete_flightstrip.schema"), "r").read(),
           "edit_flightstrip": open(os.path.join(os.path.dirname(__file__), "schemas/edit_flightstrip.schema"), "r").read(),
           "get_clients": open(os.path.join(os.path.dirname(__file__), "schemas/get_clients.schema"), "r").read(),
           "get_data": open(os.path.join(os.path.dirname(__file__), "schemas/get_data.schema"), "r").read(),
           "move_flightstrip": open(os.path.join(os.path.dirname(__file__), "schemas/move_flightstrip.schema"), "r").read(),
           }


def verify_command(command, schema):
    return json_schema.match(command, schemas[schema])
