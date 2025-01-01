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

