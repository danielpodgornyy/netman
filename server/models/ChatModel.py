from collections import deque

class ChatModel():
    def __init__(self):
        self.curr_users = []
        # Test
        self.curr_chats = {
                'Chat1': '',
                'Chat2': ''}

    def get_curr_users(self):
        return self.curr_users

    def input_username(self, username):
        self.curr_users.append(username)
        print(self.curr_users)

    def delete_username(self, username):
        self.curr_users.remove(username)
        print(self.curr_users)

    def get_curr_chats(self):
        return list(self.curr_chats.keys())

