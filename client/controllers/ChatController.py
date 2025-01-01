import re
import json

from services.ChatClient import ChatClient
from utils.Status import Status

class ChatController():
    def __init__(self):
        self.client = ChatClient()

    def connect_to_server(self, ip_address):
        # Check for a valid pattern
        ip_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'

        valid_ip = re.fullmatch(ip_pattern, ip_address)
        if (valid_ip is None):
            return Status.SYNTAX_ERROR

        # Attempt a connection
        try:
            self.client.connect_to_server(ip_address)
        except Exception as e:
            print(f"Error: {e}")
            return Status.CONNECTION_FAILED

        return Status.SUCCESS

    def get_open_chats(self):
        # Test this
        try:
            chats = self.client.get_open_chats()

        except Exception as e:
            print(f"Error: {e}")
            chats = None

        return chats

    def send_username(self, username):
        # Turn the object to a JSON string
        json_data = json.dumps({ 'username': username })
        json_data_size = len(json_data.encode())
        http_request_data = {
                'method': 'POST',
                'path': '/username',
                'headers': {
                    'Content-Type': 'application/jason',
                    'Content-Length': json_data_size,
                    'Connection': 'close'
                    },
                'body': json_data
                }


        response_code = self.client.send_http_request(http_request_data)

        return response_code



