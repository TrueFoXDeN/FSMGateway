from flask import Blueprint, request
from api import response_generator as r, auth
from broker import gateway
from logic import fsm_handler
from util import uid

management = Blueprint('management', __name__, url_prefix='/api/v1')


@management.route('/room', methods=["POST"])
def create_room():
    password = request.json['password']
    room_id = uid.room_id()
    gateway.rooms[room_id] = []
    fsm_handler.rooms[room_id] = {"password": auth.encrypt(password)}
    fsm_handler.order_flightstrips[room_id] = {}
    return r.respond({"id": room_id})


@management.route('/room/<room_id>', methods=["POST"])
def create_room_id(room_id):
    password = request.json['password']
    room_id = room_id
    gateway.rooms[room_id] = []
    fsm_handler.rooms[room_id] = {"password": auth.encrypt(password)}
    fsm_handler.order_flightstrips[room_id] = {}
    return r.respond({"id": room_id})
