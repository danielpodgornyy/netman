import re
import json

from services.ChatClient import ChatClient
from utils.Status import Status

class ChatController():
    def __init__(self):
        self.client = ChatClient()
        self.username = ''

    def init_connect_to_server(self, ip_address):

        # Check for a valid pattern
        ip_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'

        valid_ip = re.fullmatch(ip_pattern, ip_address)
        if (valid_ip is None):
            return Status.SYNTAX_ERROR

        # Attempt a connection
        try:
            # A connection to the server will be made for every request
            self.client.set_server_address(ip_address)
            self.client.connect_to_server()
            # Used to make sure the server recieves some input on connection
            self._send_test_message()

        except Exception as e:
            print(f"Error: {e}")
            return Status.CONNECTION_FAILED

        return Status.SUCCESS

    def _send_test_message(self):
        http_request_data = {
                'method': 'HEAD',
                'path': '/',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': 0,
                    'Connection': 'close'
                    },
                'body': ''
                }

        response_code, body = self.client.send_http_request(http_request_data)

    def send_username(self, username):
        # Set the username
        self.username = username

        # Turn the object to a JSON string
        json_data = json.dumps({ 'username': username })
        json_data_size = len(json_data.encode())

        http_request_data = {
                'method': 'POST',
                'path': '/username',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': json_data_size,
                    'Connection': 'close'
                    },
                'body': json_data
                }



        response_code = ''
        try:
            self.client.connect_to_server()
            response_code, body = self.client.send_http_request(http_request_data)
        except Exception as e:
            print("Error sending username: ", e)

        return response_code

    def get_chats(self):
        http_request_data = {
                'method': 'GET',
                'path': '/chat',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': 0,
                    'Connection': 'close'
                    },
                'body': 'd'
                }


        response_code = ''
        body = ''
        try:
            self.client.connect_to_server()
            response_code, body = self.client.send_http_request(http_request_data)
        except Exception as e:
            print("Error getting chats: ", e)

        # load the json into an object and pull the chat list
        return json.loads(body)['chat_list']



