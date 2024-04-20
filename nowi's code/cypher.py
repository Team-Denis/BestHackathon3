
from cryptography.fernet import Fernet


class FernetEncryption:
    
    def __init__(self, key: bytes = None) -> None:
        
        self._key = key if key else Fernet.generate_key()

    @staticmethod
    def encode_fernet(text: str, key: bytes):
        fernet = Fernet(key)
        encoded_text = fernet.encrypt(text.encode())
        return encoded_text

    @staticmethod
    def decode_fernet(encrypted_text, key):
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text).decode()
        return decrypted_text