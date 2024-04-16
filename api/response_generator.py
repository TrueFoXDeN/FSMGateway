import json

from flask import Response


def respond(r={"success": True}, status=200, json_dump=True):
    if json_dump:
        return Response(json.dumps(r), status=status, mimetype='application/json')
    return Response(r, status=status, mimetype='application/json')
