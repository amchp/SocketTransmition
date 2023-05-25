import os
import socket
from math import ceil
from compress import Compress

CHUNK_SIZE = 250*1000

class Client:
    def __init__(self):
        pass

    def start_client(self, target_host: str, connection_port: str, file_path : str) -> None:
        client_socket = self.get_socket()
        client_socket.connect((target_host, connection_port))
        self.send_file(client_socket, file_path)

    def get_socket(self) -> socket:  # Creates a BT socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def send_file(self, client_socket : socket, file_path : str) -> None:
        # Compress file
        compressor = Compress()
        file_compressed = compressor.compress_file(file_path)
  
        file_size = os.path.getsize(file_compressed)
        chunks = ceil(file_size / CHUNK_SIZE)
        print(f"Sending {file_path} ({file_size} bytes) in {chunks} chunks")
        with open(file_compressed, "rb") as file:
            for _ in range(chunks):
                print(f"Sending chunk {_+1}/{chunks}")
                client_socket.send(file.read(CHUNK_SIZE))
        client_socket.close()
        
        os.remove(file_compressed)