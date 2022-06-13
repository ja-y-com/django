import string
import random


def generate_random_string(size=16, chars=string.ascii_lowercase):
    return "".join(random.choice(chars) for _ in range(size))


def generate_random_number(size=6):
    return "".join(str(random.randrange(1, 10)) for _ in range(size))
