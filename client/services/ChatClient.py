import os
from dotenv import load_dotenv, dotenv_values
import socket as sock
import threading

load_dotenv()

class ChatClient():
    def __init__(self):
        self.port = int(os.getenv('PORT'))

    def connect_to_server(self, ip_address):
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        try:
            self.client.connect((ip_address, self.port))
        except Exception as e:
            raise e

    def get_open_chats():
        pass
