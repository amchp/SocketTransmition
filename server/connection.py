import socket
import threading
from dotenv import load_dotenv
import os
from types import FunctionType


class Server():
    backlog = 2

    def __init__(self)  -> None:
        self.self_host = None
        self.socket = None
        self.set_connection()
    
    def multithread(func) -> FunctionType:
        def wrap(*args, **kwargs) -> None:
            accept_thread = threading.Thread(target=func, args=[args])
            accept_thread.start()
            return
        return wrap
    
    def set_connection(self) -> None:
        self.socket = self.get_socket()
        load_dotenv()
        self.set_tcp_parameter()
        if self.self_host is None or self.connection_port == None:
            raise AssertionError(" Socket parameters not passed")
    
    def set_tcp_parameter(self) -> None:
        self.self_host = os.getenv("SELFIP")
        self.connection_port = int(os.getenv("TCP_PORT"))

    def get_socket(self) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s

    def start_server(self) -> None:
        self.socket.bind((self.self_host, self.connection_port))
        self.socket.listen(Server.backlog)
        self.accept_connections()

    @multithread
    def accept_connections(self) -> None:
        while True:
            client_socket, client_address = self.socket.accept()
            self.receive_messages(client_socket)
    
    @multithread
    def receive_messages(self, client_socket) -> None:
        while True:
            incoming_data = b"1"
            data = b""
            while incoming_data:
                incoming_data = client_socket.recv(1024)
                data += incoming_data
            # Decompress data
            print("Data:", data)