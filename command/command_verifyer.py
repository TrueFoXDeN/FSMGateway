import os
from json_schema import json_schema

schemas = {"connect": open(os.path.join(os.path.dirname(__file__), "schemas/connect.schema"), "r").read()}


def verify_command(command, schema):
    return json_schema.match(command, schemas[schema])
