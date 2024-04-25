import os

from flask import Blueprint, request
from api import response_generator as r, auth
from broker import gateway
from logic import fsm_handler
from logic.fsm_handler import order_flightstrips
from logs import logger
from util import uid

management = Blueprint('management', __name__, url_prefix='/api/v1')


@management.route('/room', methods=["POST"])
def create_room():
    password = request.json['password']
    room_id = uid.room_id()
    gateway.rooms[room_id] = []
    fsm_handler.rooms[room_id] = {"password": auth.encrypt(password)}
    fsm_handler.order_flightstrips[room_id] = {}
    logger.debug(f"Room {room_id} created")
    return r.respond({"id": room_id})


@management.route('/room/<room_id>', methods=["POST"])
def create_room_id(room_id):
    password = request.json['password']
    room_id = room_id
    gateway.rooms[room_id] = []
    fsm_handler.rooms[room_id] = {"password": auth.encrypt(password)}
    fsm_handler.order_flightstrips[room_id] = {}
    logger.debug(f"Room {room_id} created")
    return r.respond({"id": room_id})


@management.route('/room/<room_id>', methods=["GET"])
def get_room_id(room_id):
    exists = room_id in fsm_handler.rooms
    logger.trace(f"Room {room_id} existence checked")
    return r.respond({"exists": exists})


@management.route('/statistics', methods=["GET"])
def get_statistics():
    rooms = len(fsm_handler.rooms)
    flightstrips = 0
    user = len(gateway.clients)

    for i in fsm_handler.rooms:
        for j in order_flightstrips[i]:
            for _ in fsm_handler.order_flightstrips[i][j]:
                flightstrips += 1
    return r.respond({'rooms': rooms, 'flightstrips': flightstrips, 'user': user})


@management.route('/data', methods=["GET"])
def get_data():
    data = {}
    for i in fsm_handler.rooms:
        data[i] = fsm_handler.rooms[i]

    clients_copy = gateway.clients
    for i in gateway.clients:
        del clients_copy[i]['websocket']

    return r.respond({'data': data, 'order': fsm_handler.order_flightstrips, 'clients': clients_copy})


@management.route('/loglevel/<level>', methods=["POST"])
def set_log_level(level):
    if os.environ.get('API_TOKEN') == request.headers['Authorization']:
        match level:
            case 'trace':
                logger.LOG_LEVEL = 0
            case 'debug':
                logger.LOG_LEVEL = 1
            case 'info':
                logger.LOG_LEVEL = 2
            case 'warning':
                logger.LOG_LEVEL = 3
            case 'error':
                logger.LOG_LEVEL = 4
            case 'critical':
                logger.LOG_LEVEL = 5
        return r.respond({"logLevel": logger.LOG_LEVEL})
    return r.respond({"success": False}, 401)
