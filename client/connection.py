from dotenv import load_dotenv
import os
from socket import socket
from math import ceil

CHUNK_SIZE = 250*1000

class Client:
    def __init__(self):
        pass

    def start_client(self, target_host: str, connection_port: str, file_path : str) -> None:
        client_socket = self.get_socket()
        client_socket.connect((target_host, connection_port))
        self.send_file(client_socket, file_path)

    def get_socket(self) -> socket:  # Creates a BT socket
        s = socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def send_file(self, client_socket : socket, file_path : str) -> None:
        # Compress file
        file_size = os.path.getsize(file_path)
        chunks = ceil(file_size / CHUNK_SIZE)
        with open(file_path, "rb") as file:
            for _ in range(chunks):
                client_socket.send(file.read(self.buffer))
        client_socket.close()