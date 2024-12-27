import tkinter as tk
from tkinter import ttk

from HomeView import HomeView
from ChatView import ChatView
from FrameController import FrameController

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
        self.init_frames()

        # Set home frame
        self.switch_frame('home')

    def init_frames(self):
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def switch_frame(self, frame_name):
        self.frames[frame_name].tkraise()


if (__name__ == '__main__'):
    # Create the root frame and initialize the tkinter application
    app = MainApp()
    app.mainloop()

