from os import environ
import jwt

import bcrypt


def encrypt(password):
    if password == "":
        return ""
    return bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())


def check_password(input, saved_password):
    if saved_password == "" and input == "":
        return True
    return bcrypt.checkpw(input.encode('UTF-8'), saved_password)


JWT_PASSWORD = environ.get('JWT_PASSWORD')


def encode_token(param):
    return jwt.encode(param, JWT_PASSWORD, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, JWT_PASSWORD, algorithms=["HS256"])


def verify_token(token, room_id):
    try:
        room = decode_token(token)['room']
        print(room)
        if room == room_id:
            return True
    except Exception as e:
        return False
