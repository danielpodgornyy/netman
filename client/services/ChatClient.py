import socket as sock
import threading

class ChatClient():
    def __init__(self):
        self.host = '192.168.1.54'
        self.port = 3510
    def connect_to_server(self, ip_address):
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        try:
            self.client.connect((self.host, self.port))
        except Exception as e:
            raise e


if __name__ == '__main__':
    client = ChatClient()
    client.connect_to_server()

