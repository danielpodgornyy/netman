import os
from dotenv import load_dotenv, dotenv_values
import socket as sock
import threading

from services.utils.HTTPRequestSender import HTTPRequestSender

load_dotenv()

class ChatClient():
    def __init__(self):
        self.port = int(os.getenv('PORT'))
        self.client = None
        self.server_address = ''

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
            req_handler = HTTPRequestSender(req_stream, res_stream, http_request_data)

        # return the response code and body
        return req_handler.response_code, req_handler.body
