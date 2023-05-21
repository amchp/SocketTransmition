from connection import Client

def main():
    client = Client()
    client.start_client("192.168.1.103", 3000, "/Users/juanmcewen/Desktop/Alejandro/Estudios/SistemasOperativos/SocketTransmition/client/test-music.mp3")

if __name__ == "__main__":
    main()