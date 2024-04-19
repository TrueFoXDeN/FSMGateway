import uuid
import random
import string


def uuid_gen():
    return str(uuid.uuid4())


def room_id():
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(5))
    return random_string
