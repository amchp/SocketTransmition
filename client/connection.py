from dotenv import load_dotenv
import os
import socket
from math import ceil

CHUNK_SIZE = 250*1000

class Client:
    def __init__(self):
        pass

    def start_client(self, target_host: str, connection_port: int, file_path : str) -> None:
        client_socket = self.get_socket()
        client_socket.connect((target_host, connection_port))
        self.send_file(client_socket, file_path)

    def get_socket(self) -> socket.socket:  # Creates a BT socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def send_file(self, client_socket : socket.socket, file_path : str) -> None:
        # Compress file
        file_name = file_path.split("/")[-1]
        file_size = os.path.getsize(file_path)
        headers = (f"{file_size} {file_name} ").encode()
        client_socket.send(headers)
        chunks = ceil(file_size / CHUNK_SIZE)
        with open(file_path, "rb") as file:
            for _ in range(chunks):
                client_socket.send(file.read(CHUNK_SIZE))
        client_socket.close()