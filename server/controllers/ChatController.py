from models.ChatModel import ChatModel

class ChatController():
    def __init__(self):
        self.model = ChatModel()

    def input_username(self, username):
        # Check if the username already exists
        curr_users = self.model.get_curr_users()
        if username in curr_users:
            return False

        # Input username
        self.model.input_username(username)
        return True

    def delete_username(self, username):
        curr_users = self.model.get_curr_users()
        if username in curr_users:
            self.model.delete_username(username)


    def get_curr_chats(self):
        chat_list = self.model.get_curr_chats()

        chat_list_object = {
                'chat_list': chat_list
                }
        return chat_list_object

    def add_chat(self, chat_room_name):
        # Check if the chat room exists
        curr_chats = self.model.get_curr_chats()
        if chat_room_name in curr_chats:
            return False

        # Input username
        self.model.add_chat(chat_room_name)
        return True

    def get_chat_logs(self, chat_room_name):
        print(chat_room_name)
        chat_logs = self.model.get_chat_logs(chat_room_name)
        chat_logs_object = {
                'chat_logs': chat_logs # list of dicts
                }

        return chat_logs_object


