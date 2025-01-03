import os
from dotenv import load_dotenv, dotenv_values
import socket as sock
import threading

load_dotenv()

class ChatClient():
    def __init__(self, controller, req_sender):
        # For sending
        self.port = int(os.getenv('PORT'))
        self.client = None
        self.server_address = ''
        self.req_sender = req_sender

        self.controller = controller

        # For listening
        self.listen_thread = None
        self.accept = None
        self.accept_addr = ('', self.port+1)
        self.listener_limit = 5

        self.stop_flag = threading.Event()

    def set_server_address(self, ip_address):
        self.server_address = ip_address

    def connect_to_server(self):
        if self.client is not None:
            self.client.close()

        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.client.settimeout(5) # Stop trying after 5 seconds

        try:
            self.client.connect((self.server_address, self.port))
        except Exception as e:
            raise e

    def send_http_request(self, http_request_data):
        req_stream = self.client.makefile('wb')
        res_stream = self.client.makefile('rb')

        with req_stream, res_stream:
            # We write the request and recieve the response (other way around on server side)
            res_data = self.req_sender(req_stream, res_stream, http_request_data)

        # return the response code and body
        return res_data.response_code, res_data.body

    # LISTEN FOR

    def listen_for_connections(self):
        # Clear stop flag
        self.stop_flag.clear()

        # Create a socket to accept clients on
        self.accept = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        # Make sure the port is reusable after exit
        self.accept.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        # Bind socket to address and port
        self.accept.bind(self.accept_addr)

        print(f"Listening for server on port {self.accept_addr[1]}")
        # Set listener limit and listen
        self.accept.listen(self.listener_limit)

        while not self.stop_flag.is_set():
            try:
                self.accept.settimeout(1)  # Check stop flag periodically
                server, address = self.accept.accept()
                print(f"Connected to client {address[0]} {address[1]}")

                threading.Thread(target=self.handle_request, args=(server, )).start()
            except sock.timeout:
                continue

        # Stopping thread
        self.accept.close()

    def handle_request(self, server):
        with server:
            data_json = server.recv(1024)
            self.controller.process_incoming_data(data_json.decode())

    def start_listening(self):
        if self.listen_thread and self.listen_thread.is_alive():
            self.stop_listening()

        self.stop_flag.clear()
        self.listen_thread = threading.Thread(target=self.listen_for_connections)
        self.listen_thread.start()

    def stop_listening(self):
        if self.accept:
            self.stop_flag.set()  # Signal the thread to stop
            self.listen_thread.join()  # Wait for the thread to exit
            self.accept.close()
            print("Listener stopped.")


    # Allows controller to also close connection
    def close_connection(self):
        self.client.close()
        self.server_address = ''

        print('closed')
