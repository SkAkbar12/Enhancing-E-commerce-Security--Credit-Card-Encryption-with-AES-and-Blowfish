import random

def generate_pin():
    # Generate a random 6-digit PIN
    pin = random.randint(100000, 999999)
    return str(pin)


