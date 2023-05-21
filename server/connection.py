import socket
import threading
from dotenv import load_dotenv
import os
from types import FunctionType

CHUNK_SIZE = 250 * 1000


class Server:
    backlog = 2

    def __init__(self) -> None:
        self.self_host: str = ""
        self.connection_port: str = ""
        self.set_connection()

    def multithread(func) -> FunctionType:
        def wrap(*args, **kwargs) -> None:
            accept_thread = threading.Thread(target=func, args=args)
            accept_thread.start()
            return

        return wrap

    def set_connection(self) -> None:
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        load_dotenv()
        self.set_tcp_parameter()
        if self.self_host is None or self.connection_port == None:
            raise AssertionError(" Socket parameters not passed")

    def set_tcp_parameter(self) -> None:
        self.self_host = os.getenv("SELFIP")
        self.connection_port = int(os.getenv("TCP_PORT"))

    def start_server(self) -> None:
        print("Start Server", flush=True)
        self.socket.bind((self.self_host, self.connection_port))
        self.socket.listen(Server.backlog)
        self.accept_connections()

    def accept_connections(self) -> None:
        while True:
            client_socket, client_address = self.socket.accept()
            self.receive_messages(client_socket)

    @multithread
    def receive_messages(self, client_socket: socket.socket) -> None:
        while True:
            data: bytes = client_socket.recv(CHUNK_SIZE)
            if data == b"":
                continue
            headers: list[bytes] = data.split()
            print(headers[1])
            data = b" ".join(data.split()[2:])
            length: int = int(headers[0].decode())
            file_name: str = headers[1].decode()
            while len(data) < length:
                data += client_socket.recv(CHUNK_SIZE)
                print(length, len(data))
            with open(f"./files/{file_name}", "bw") as file:
                file.write(data)
