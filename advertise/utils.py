import random
import string

def generate_slug():
    return ''.join(str(random.choice(string.ascii_uppercase + string.ascii_lowercase)) for _ in range(6))


