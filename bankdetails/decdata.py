
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from shoppingapp.pinaunthenticator import Data,storingdata
from bankdetails.models import EncryptData
from bankdetails.encdec import perform_xor,perform_xor_strings

def bankdata(card,date,cvv):
    bankdata=EncryptData.objects.all()
    for data in bankdata:
        cardnumber=data.cardnumber
        date_cvv=data.date_cvv
        key1=data.key1
        key2=data.key2
        pin=data.pin
        password=data.password
       
        try:
            decrypt_password=decrypt_pass(password).decode('utf-8')

            print('decrypt_password',decrypt_password)

            dec_key1=perform_xor_strings(key1,decrypt_password)
            dec_key2=perform_xor_strings(key2,decrypt_password)
        
            pinphase1=perform_xor(pin,dec_key2)
            pinfinal=perform_xor(pinphase1,dec_key1)
            decrypted_xor_credit_card = perform_xor(decrypt_aes(pinfinal, cardnumber, dec_key1).decode('utf-8'), dec_key1)
            decrypted_xor_secret_cvv = perform_xor(decrypt_aes(pinfinal, date_cvv, dec_key2).decode('utf-8'), dec_key2)

# Split decrypted data into secret key and CVV
            separator_index = decrypted_xor_secret_cvv.find(',')
            decrypted_secret_key = decrypted_xor_secret_cvv[:separator_index] if separator_index != -1 else decrypted_xor_secret_cvv
            decrypted_cvv = decrypted_xor_secret_cvv[separator_index + 1:] if separator_index != -1 else ""
        
        
            if card==decrypted_xor_credit_card and date==decrypted_secret_key and cvv==decrypted_cvv:
               
                storingdata(pinfinal)
            
            
        
                return True
        except Exception as e:
            
            print(e)
            pass
 

        
    return False



def decrypt_aes(key, encrypted_data, salt):
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

    return decrypted_data_aes.rstrip(b'\0')

     


def decrypt_pass(encrypted_data):
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

    encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
    iv = b'iv12345678901234'
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data_aes = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data_aes.rstrip(b'\0')

