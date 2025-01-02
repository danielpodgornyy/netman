import tkinter as tk
from tkinter import ttk

from views.HomeView import HomeView
from views.ChatView import ChatView
from controllers.ChatController import ChatController

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Init root frame
        self.title('NetMan')
        self.geometry('300x400')
        self.resizable(True, True)

        # Create frames
        self.frames = {
                'home': HomeView(self),
                'chat': ChatView(self)
                }

        # Connect controllers
        # CHAT
        chat_controller = ChatController(self.frames['chat'])
        self.frames['chat'].set_controller(chat_controller)

        # Initialize frames
        self.init_frames()

        # Set home frame
        self.switch_frame('home')

    def init_frames(self):
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def switch_frame(self, frame_name):
        self.frames[frame_name.lower()].tkraise()


if (__name__ == '__main__'):
    # Create the root frame and initialize the tkinter application
    app = MainApp()
    app.mainloop()

