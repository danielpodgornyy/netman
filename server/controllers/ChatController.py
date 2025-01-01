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




