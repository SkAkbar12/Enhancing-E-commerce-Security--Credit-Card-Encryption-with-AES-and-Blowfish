
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

def encrypt_aes_pass(data):
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

# Function to perform AES decryption
# Function to perform AES decryption
def decrypt_aes_pass(encrypted_data):
    key = "encrypted_key"
    salt = "encrypted_salt"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt.encode('utf-8'),
        iterations=100000,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(key.encode())

    encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
    iv = b'iv12345678901234'
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data_aes = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove null byte padding
    return decrypted_data_aes.rstrip(b'\0')