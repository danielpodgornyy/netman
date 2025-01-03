import json

from models.ChatModel import ChatModel

class ChatController():
    def __init__(self, server):
        self.model = ChatModel()

        self.server = server

    def input_username(self, username, address):
        # Check if the username already exists
        curr_users = self.model.get_curr_users()
        usernames = list(user['username'] for user in curr_users)
        if username in usernames:
            return False

        # Input username
        user = { 'username': username, 'address': address }
        self.model.input_user(user)
        return True

    def delete_username(self, username):
        curr_users = self.model.get_curr_users()
        usernames = list(user['username'] for user in curr_users)

        if username in usernames:
            self.model.delete_username(username)

    def get_curr_chats(self):
        chat_list = self.model.get_curr_chats()

        chat_list_object = {
                'chat_list': chat_list
                }

        return chat_list_object

    def add_chat(self, chat_room_name, username):
        # Check if the chat room exists
        curr_chats = self.model.get_curr_chats()
        if chat_room_name in curr_chats:
            return False

        # Input username
        self.model.add_chat(chat_room_name)

        chat_list_obj = {'chat_room_name': chat_room_name}

        self.broadcast_data(json.dumps(chat_list_obj), username)
        return True

    def get_chat_logs(self, chat_room_name):
        print(chat_room_name)
        chat_logs = self.model.get_chat_logs(chat_room_name)
        chat_logs_object = {
                'chat_logs': chat_logs # list of dicts
                }

        return chat_logs_object

    def enter_log(self, chat_log):
        chat_room = chat_log['chat_room']
        username = chat_log['username']
        message = chat_log['message']

        chat_log_object = {
                'username': username,
                'message': message
                }

        self.model.enter_log(chat_room, chat_log_object)

        # Broadcast the adding of the log to clients
        self.broadcast_data(json.dumps(chat_log_object), username)

        return True

    # Don't broadcast to the user who sent the message
    def broadcast_data(self, json_data, sender_username):
        curr_users = self.model.get_curr_users()
        addresses = list(user['address'] for user in curr_users if user['username'] != sender_username)

        print(addresses)

        # Broadcasting
        for address in addresses:
            self.server.send_json(address, json_data)
