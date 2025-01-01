import tkinter as tk
from tkinter import ttk

class PromptWindow(tk.Toplevel):
    def __init__(self, root, title):
        super().__init__(root)

        self.prompt_container = ttk.Frame(
                self,
                padding=10
                )
        self.prompt_container.pack(expand=True, fill=tk.BOTH)

        self.prompt_container.rowconfigure(0, weight=1)
        self.prompt_container.columnconfigure(0, weight=1)
        self.prompt_container.columnconfigure(1, weight=2)

        self.title(title)
        self.geometry('400x50')
        self.resizable(False, False)
