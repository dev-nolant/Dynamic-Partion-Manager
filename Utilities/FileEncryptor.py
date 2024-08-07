# Utilities/FileEncryptor.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

class FileEncryptor:
    def __init__(self, api_key):
        self.api_key = api_key.encode()
        self.backend = default_backend()
        self.salt = os.urandom(16)

    def _derive_key(self):
        kdf = Scrypt(
            salt=self.salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=self.backend
        )
        key = kdf.derive(self.api_key)
        return key

    def encrypt_file(self, file_path):
        key = self._derive_key()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as f:
            data = f.read()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as f:
            f.write(self.salt + iv + encrypted_data)

        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        with open(encrypted_file_path, 'rb') as f:
            data = f.read()

        salt = data[:16]
        iv = data[16:32]
        encrypted_data = data[32:]

        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=self.backend
        )
        key = kdf.derive(self.api_key)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        decrypted_file_path = encrypted_file_path.replace('.enc', '')
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)

        return decrypted_file_path
