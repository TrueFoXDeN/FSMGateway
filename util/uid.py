import uuid
import random
import string


def uuid_gen():
    return uuid.uuid4()


def room_id():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(5))
    return random_string
