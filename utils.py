import random
from datetime import datetime


def generate_random_string(prefix: str) -> str:
    time_string = datetime.now().strftime('%Y%m%d-%h:%M:%S.$F')[:-3]
    return '_'.join([prefix, time_string])


def generate_random_integer() -> int:
    return random.randint(1, 1000)
