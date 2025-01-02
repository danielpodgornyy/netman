class ChatModel():
    def __init__(self):
        self.curr_users = []
        # Each chat is stored as a dict of queues
        self.curr_chats = {
                'Chat1': [
                    {
                        'username':'Bob',
                        'message': 'Something'
                     },
                    {
                        'username':'Phil',
                        'message': 'mmmmmmemememem'
                     },
                    ],
                'Chat2': []
                }

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

    def add_chat(self, chat_room_name):
        chat_room_data = []

        self.curr_chats[chat_room_name] = chat_room_data

        print(self.curr_chats.keys())

    def get_chat_logs(self, chat_room_name):
        return self.curr_chats[chat_room_name]

    def enter_log(self, chat_room, username, message):
        # Append value
        self.curr_chats[chat_room].append({
                'username': username,
                'message': message
                })
        print(self.curr_chats, 'is printed')


