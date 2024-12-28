from services.ChatClient import ChatClient

class ChatController():
    def __init__(self):
        self.client = ChatClient

    def connect_to_server(self, IP_address):
        return self.client.connect_to_server(IP_address)

