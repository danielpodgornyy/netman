import tkinter as tk
from tkinter import ttk

class PromptWindow(tk.Toplevel):
    def __init__(self, root, title, result_string):
        super().__init__(root)

        self.title(title)
        self.geometry('400x50')
        self.resizable(False, False)

        self.prompt_container = ttk.Frame(
                self,
                padding=10
                )
        self.prompt_container.pack(expand=True, fill=tk.BOTH)

        self.prompt_container.rowconfigure(0, weight=1)
        self.prompt_container.columnconfigure(0, weight=1)
        self.prompt_container.columnconfigure(1, weight=2)

        prompt = ttk.Label(
                self.prompt_container,
                text=title,
                style='Prompt.TLabel'
                )
        prompt.grid(column=0, row=0, sticky='nesw')

        self.textbox = ttk.Entry(
               self.prompt_container,
               textvariable = result_string
                )
        self.textbox.grid(column=1, row=0, sticky='ew')
