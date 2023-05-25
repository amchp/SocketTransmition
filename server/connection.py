import socket
import threading
from dotenv import load_dotenv
import os
from types import FunctionType
from decompress import Decompress
from decrypt import Decrypt


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
        
    def set_key(self, client_socket: socket.socket, key: bytes) -> None:
        client_socket.send(key)

    def accept_connections(self) -> None:
        while True:
            client_socket, client_address = self.socket.accept()
            
            self.receive_messages(client_socket)

    @multithread
    def receive_messages(self, client_socket: socket.socket) -> None:
        decompressor = Decompress()
        decryptor = Decrypt()
        key = decryptor.generate_key()
        self.set_key(client_socket, key)
        
        while True:            
            data: bytes = b""
            while True:
                chunk_data = client_socket.recv(CHUNK_SIZE)
                
                if chunk_data == b"":
                    break
                
                print(f"socket {client_socket.getpeername()} received {len(chunk_data)} bytes")
                data += chunk_data
            
            if data != b"":
                print(f"socket {client_socket.getpeername()} complete data received")
                # Decrypt data
                print(f"socket {client_socket.getpeername()} decrypting data")
                data = decryptor.decrypt(data, key)
                print(f"socket {client_socket.getpeername()} decrypted data")
                
                # Decompress data
                print(f"socket {client_socket.getpeername()} decompressing data")
                decompressor.decompress_data(data) 
                print(f"socket {client_socket.getpeername()} decompressed data")
