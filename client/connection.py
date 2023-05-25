import os
import socket
from math import ceil
from compress import Compress
from encrypt import Encrypt

CHUNK_SIZE = 250*1000
KEY_SIZE = 1000*1000

class Client:
    def __init__(self):
        self.key = None
        
    def get_key(self, client_socket : socket) -> None:
        key_data = client_socket.recv(KEY_SIZE)
        print(f"Received key: {key_data}")
        self.key = key_data

    def start_client(self, target_host: str, connection_port: str, file_path : str) -> None:
        client_socket = self.get_socket()
        client_socket.connect((target_host, connection_port))
        self.get_key(client_socket)
        self.send_file(client_socket, file_path)

    def get_socket(self) -> socket:  # Creates a BT socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def send_file(self, client_socket : socket, file_path : str) -> None:
        # Compress file
        compressor = Compress()
        file_compressed = compressor.compress_file(file_path)
        
        # Encrypt file
        encryptor = Encrypt()
        file_encrypted = encryptor.encrypt_file(file_compressed, self.key)
        
        # Send file
        file_size = os.path.getsize(file_encrypted)
        chunks = ceil(file_size / CHUNK_SIZE)
        print(f"Sending {file_path} ({file_size} bytes) in {chunks} chunks")
        with open(file_encrypted, "rb") as file:
            for _ in range(chunks):
                print(f"Sending chunk {_+1}/{chunks}")
                client_socket.send(file.read(CHUNK_SIZE))
        client_socket.close()
        
        os.remove(file_compressed)
        os.remove(file_encrypted)