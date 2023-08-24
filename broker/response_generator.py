import json


def respond(command, args):
    return json.dumps({"cmd": command, "args": args})
