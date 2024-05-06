import random
import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



import base64

def generate(length):
    if length <= 0:
        raise ValueError("Length should be a positive integer")

    
    min_value = 10 ** (length - 1)
    max_value = (10 ** length) - 1

   
    random_integer = random.randint(min_value, max_value)

    return random_integer

# Function to generate a random XOR key
def generate_random_xor_key(length):
    return secrets.token_hex(length)

# Function to perform XOR operation
def perform_xor(data, key):
    return ''.join(chr(ord(char) ^ int(bit, 16)) for char, bit in zip(data, key))

# Function to perform AES encryption
def encrypt_aes(key, data, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt.encode('utf-8'),
        iterations=100000,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(key.encode())

    data = data.encode('utf-8') + b'\0' * (16 - len(data) % 16)

    iv = b'iv12345678901234'
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

# Take user input


def perform_xor_strings(str1, str2):
   
    length = max(len(str1), len(str2))
    
    # Pad the strings with null bytes to make them equal in length
    str1 = str1.ljust(length, ' ')
    str2 = str2.ljust(length, ' ')
    
    result = ''.join(chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2))
    return result



def decrypt_xor_result(encrypted_result, key):
    decrypted_result = perform_xor_strings(encrypted_result, key)
    return decrypted_result



def encrypt_pass(data):
    key="encrypted_key"
    salt="encrypted_salt"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt.encode('utf-8'),
        iterations=100000,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(key.encode())

    data = data.encode('utf-8') + b'\0' * (16 - len(data) % 16)

    iv = b'iv12345678901234'
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

