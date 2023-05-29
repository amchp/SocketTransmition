from cryptography.fernet import Fernet


class Decrypt:
    def __init__(self):
        pass
    
    def generate_key(self) -> bytes:
        return Fernet.generate_key()

    def decrypt(self, data: bytes, key: bytes) -> bytes:
        f = Fernet(key)
        return f.decrypt(data)