import random
import string


def random_string(length):
    return str(''.join(random.choices(string.ascii_lowercase, k=length)))