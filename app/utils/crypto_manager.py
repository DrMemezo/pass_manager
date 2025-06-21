from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from cryptography.fernet import Fernet 
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend # ? TO CLAUDE: What is a backend as used in cryptography?

import base64
from typing import Optional

class CryptographyManager:
    pass_hasher:PasswordHasher # Since it's only used for password hashing irrespective of the user, i don't consider clearing it after user logout necessary. 
    __fernet:Optional[Fernet]

    def __init__(self):
        self.clear()
        self.pass_hasher = PasswordHasher()         

    def on_login(self, password:str, hash:str):
        """ Loads the configuration and Fernet for the user"""


    def hash(self, password:str) -> str:
        """Creates and returns the hash of the master password"""
        return self.pass_hasher.hash(password) 
    
    def verify(self, password:str, hash:str) -> bool:
        """Verifies the password and the hash, returns False if they don't match."""
        try:
            return self.pass_hasher.verify(hash, password)
        except VerifyMismatchError:
            return False
    
    def set_fernet(self, password:str, salt:bytes): 
        """Derive a key from the master password to use with Fernet"""        
        kdf = PBKDF2HMAC( 
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.__fernet = Fernet(key)
        key = None 
        del key 

    def encrypt_password(self, plain:str) -> bytes:
        return self.__fernet.encrypt(plain.encode())
    
    def decrypt_passwrd(self, cipher:str) -> str:
        return self.__fernet.decrypt(cipher).decode()

    def clear(self):
        """ Clears the class of the user's data """
        self.__fernet = None