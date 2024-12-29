import re

from services.ChatClient import ChatClient
from utils.Status import Status

class ChatController():
    def __init__(self):
        self.client = ChatClient()

    def connect_to_server(self, ip_address):
        ip_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'

        valid_ip = re.search(ip_pattern, ip_address)
        if (valid_ip is None):
            return Status.SYNTAX_ERROR

        try:
            self.client.connect_to_server(ip_address)
        except Exception as e:
            print(f"Error: {e}")
            return Status.CONNECTION_FAILED

        return Status.SUCCESS
