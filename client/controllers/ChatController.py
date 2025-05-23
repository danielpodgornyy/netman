import re
import json
from multiprocessing import Process

from services.ChatClient import ChatClient
from utils.Status import Status

from services.utils.HTTPRequestSender import HTTPRequestSender

class ChatController():
    def __init__(self, view):
        self.client = ChatClient(self, HTTPRequestSender)
        self.view = view
        self.username = ''
        self.active_chat_room = ''

    def init_connect_to_server(self, ip_address):
        # If you were previously connected to a server, remove your username from it
        if (self.username != ''):
            self.leave_server()

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

            # Init listening for connections on a seperate thread
            self.client.start_listening()

        except Exception as e:
            print(f"Error attempting connection: {e}")
            return Status.CONNECTION_FAILED

        return Status.SUCCESS

    def leave_server(self):
        # If there is no username set, there is nothing to be done
        if (self.username == ''):
            return

        # Convert username to json object
        json_data = json.dumps({ 'username': self.username })
        json_data_size = len(json_data.encode())

        # When leaving the connection, delete the username from the server side
        http_request_data = {
                'method': 'DELETE',
                'path': '/username',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': json_data_size,
                    'Connection': 'close'
                    },
                'body': json_data
                }

            # Send a request to delete username
        try:
            self.client.connect_to_server()
            self.client.send_http_request(http_request_data)
        except Exception as e:
            print(f"Error deleting username: ", e)


        # Reset username
        self.username = ''
        # Close connection


        self.client.stop_listening()
        self.client.close_connection()


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
        # Username cannot be empty
        if (username == ''):
            return 406

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
            response_code = 500

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
                'body': ''
                }

        response_code = ''
        body = ''
        try:
            self.client.connect_to_server()
            response_code, body = self.client.send_http_request(http_request_data)
        except Exception as e:
            print("Error getting chats: ", e)
            response_code = 500

        # load the json into an object and pull the chat list
        return json.loads(body)['chat_list']


    def add_chat(self, chat_room_name):
        # Chat room name cannot be empty
        if (chat_room_name == ''):
            return 406

        # Turn the object to a JSON string
        json_data = json.dumps({ 'chat_room_name': chat_room_name, 'username': self.username})
        json_data_size = len(json_data.encode())

        http_request_data = {
                'method': 'POST',
                'path': '/chat',
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
            print("Error adding chat room: ", e)
            response_code = 500
        print(response_code)

        return response_code

    def server_is_active(self):
        if self.username != '':
            return True
        else:
            return False

    def get_chat_room_logs(self, chat_room_name):
        self.active_chat_room = chat_room_name
        print(chat_room_name)

        # Pull chats from chat room
        http_request_data = {
                'method': 'GET',
                'path': f'/logs:{chat_room_name}',
                'headers': {
                    'Content-Type': 'application/json',
                    'Content-Length': 0,
                    'Connection': 'close'
                    },
                'body': ''
                }

        response_code = ''
        body = ''
        try:
            self.client.connect_to_server()
            response_code, body = self.client.send_http_request(http_request_data)
        except Exception as e:
            print("Error getting chat room logs: ", e)
            return []

        # Load the json into an object
        return json.loads(body)['chat_logs']

    def get_username(self):
        return self.username

    def enter_log(self, username, message):
        # Checks
        if (not self.server_is_active() or self.active_chat_room == ''):
            return 500

        # Turn the object to a JSON string
        json_data = json.dumps({ 'chat_log': {'chat_room':self.active_chat_room, 'username': username, 'message': message}})
        json_data_size = len(json_data.encode())

        http_request_data = {
                'method': 'POST',
                'path': f'/logs:{self.active_chat_room}', # Put the current chat room as the param
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
            print("Error adding chat room: ", e)
            response_code = 500
        print(response_code, ':P')

        return response_code

    def process_incoming_data(self, data_json):
        json_obj = json.loads(data_json)
        keys = json_obj.keys()
        print(json_obj)

        # If the message is one of the keys and the active chat room is the one that was updated
        if 'message' in keys:
            if json_obj["chat_room"] == self.active_chat_room:
                self.view.add_text(f'{json_obj["username"]}: {json_obj["message"]}')
        # If chat_room_name is one of the keys, its a chat room
        elif 'chat_room_name' in keys:
            self.view.create_chat(json_obj['chat_room_name'])
