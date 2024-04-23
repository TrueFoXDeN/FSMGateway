import json
import os
import traceback
from time import time

import requests

LOKI_URL = os.environ.get('LOKI_URL')

LOG_LEVEL = 0


def trace(msg, body=''):
    if LOG_LEVEL <= 0:
        send('trace', msg, body)


def debug(msg, body=''):
    if LOG_LEVEL <= 1:
        send('debug', msg, body)


def info(msg, body=''):
    if LOG_LEVEL <= 2:
        send('info', msg, body)


def warning(msg, body=''):
    if LOG_LEVEL <= 3:
        send('warning', msg, body)


def error(msg, body=''):
    if LOG_LEVEL <= 4:
        send('error', msg, body)


def critical(msg, body=''):
    if LOG_LEVEL <= 5:
        send('critical', msg, body)


def send(level, msg, body):
    data = {
        "streams": [
            {
                "stream": {
                    "app": "gateway",
                    "level": level,
                    "message": msg
                },
                "values": [
                    [f"{int(time() * 1e9)}", json.dumps({"description": body})]
                ]
            }
        ]
    }
    headers = {
        'Content-type': 'application/json'
    }
    try:
        response = requests.post(LOKI_URL, data=json.dumps(data), headers=headers)
        if response.status_code != 204:
            print(f'ERROR STATUSCODE WHILE SENDING LOG TO {os.environ.get("LOKI_URL")}')
    except Exception as e:
        traceback.print_exc()
        print(f'ERROR SENDING LOG TO {os.environ.get("LOKI_URL")}')
