import random
import string

def generate_slug():
    return ''.join(str(random.randint(0,9)) for _ in range(6))