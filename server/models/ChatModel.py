
class ChatModel():
    def __init__(self):
        self.curr_users = []

    def get_curr_users(self):
        return self.curr_users

    def input_username(self, username):
        self.curr_users.append(username)
        print(self.curr_users)
