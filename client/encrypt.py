from cryptography.fernet import Fernet


class Encrypt:
    def __init__(self):
        pass

    def encrypt_file(self, file_path: str, key: bytes) -> bytes:
        f = Fernet(key)
        
        with open(file_path, "rb") as file:
            with open(file_path + ".enc", "wb") as encrypted_file:
                encrypted_file.write(f.encrypt(file.read()))
                
        return file_path + ".enc"