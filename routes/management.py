from flask import Blueprint, request
from api import response_generator as r
from broker import gateway
from util import uid

management = Blueprint('management', __name__)


@management.route('/room', methods=["POST"])
def create_room():
    room_id = uid.room_id()
    gateway.rooms[room_id] = []
    return r.respond({"id": room_id})

