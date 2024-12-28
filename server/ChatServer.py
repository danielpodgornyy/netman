import socket as sock
import threading

class ChatServer():
    def __init__(self):
        self.host = ''
        self.port = 3510
        self.listener_limit = 5

    def client_handler(self, client):
        print('Connected')
        pass

    def start_server(self):
        # Create a socket to accept clients on
        self.server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        # Bind socket to host and port
        try:
            self.server.bind((self.host, self.port))
            print(f"Running server on port {self.port}")
        except:
            print(f"Unable to bind to host and port {self.host}, {self.port}")

        # Set listener limit
        self.server.listen(self.listener_limit)

        while True:
            client, address = self.server.accept()
            print(f"Connected to client {address[0]} {address[1]}")

            threading.Thread(target=self.client_handler, args=(client, )).start()


    def stop_server(self):
        sock.close(self.server)

if __name__ == '__main__':
    server = ChatServer()
    server.start_server()


