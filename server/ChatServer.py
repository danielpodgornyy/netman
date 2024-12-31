import socket as sock
import threading

from utils.HTTPRequestHandler import HTTPRequestHandler
from controllers.ChatController import ChatController

class ChatServer():
    def __init__(self, sock_addr, req_handler):
        self.sock_addr = sock_addr
        self.req_handler = req_handler
        self.listener_limit = 5

    def listen_for_client(self, client):
        with client:
            # File objects that hold data to be written to or from (works similarly to python file handling)
            req_stream = client.makefile('rb')
            res_stream = client.makefile('wb')
            controller = ChatController()

            HTTPRequestHandler(req_stream, res_stream, controller)
            # Wait for a username, if a nonvalid one is provided, end the connection

    def accept_username(self, client):
        return
        with client:
            while(True):
                data = client.recv(2048)
                if not data:
                   client.sendall("Username is required")
                # Wait for a username, if a nonvalid one is provided, end the connection

    def start_server(self):
        # Create a socket to accept clients on
        self.server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        # Make sure the port is reusable after exit
        self.server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        # Bind socket to address and port
        self.server.bind(self.sock_addr)

        print(f"Running server on port {self.sock_addr[1]}")
        # Set listener limit and listen
        self.server.listen(self.listener_limit)

        while True:
            client, address = self.server.accept()
            print(f"Connected to client {address[0]} {address[1]}")

            threading.Thread(target=self.listen_for_client, args=(client, )).start()

    def stop_server(self, *args):
        sock.close(self.server)
