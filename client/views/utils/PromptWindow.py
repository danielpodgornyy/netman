import tkinter as tk

class PromptWindow(tk.Toplevel):
    def __init__(self, root, title):
        super().__init__(root)


        self.title(title)
        self.geometry('400x50')
        self.resizable(False, False)
