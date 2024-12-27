import tkinter as tk
from tkinter import ttk

class ChatView(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Keep a reference to the parent for switching frames
        self.parent = root

        # Set styles
        self.create_styles()
        self.configure(style = 'Main.TFrame')

        # Configure grid
        self.rowconfigure(0, weight=0, minsize=10)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.generate_widgets()
    def create_styles(self):
        self.style = ttk.Style()

        self.style.configure('.', font=('MathJax_SansSerif', 24))

        # Set style for main frame
        self.style.configure('LightGrey.TFrame', background='#3E4248')

        self.style.configure('DarkGrey.TFrame', background='#2B2E32')

        self.style.configure('TMenubutton', font=('MathJax_SansSerif', 10), padding=0)  # Change font size and padding`

        self.style.configure('Send.TButton', font=('MathJax_SansSerif', 10), padding=0)  # Change font size and padding`

        self.style.configure('Bubble.TLabel', font=('MathJax_SansSerif', 15), padding=4 )

    def create_menu(self, frame):
            menubutton = ttk.Menubutton(
                    frame,
                    text='Options',
                    direction='below',
                    )
            menubutton.grid(row=0, column=0, sticky='n')

            # Create a menu for the Menubutton
            menu = tk.Menu(menubutton, tearoff=0)
            menubutton['menu'] = menu

            # Add menu options
            menu.add_command(label="Option 1")
            menu.add_command(label="Option 2")
            menu.add_separator()
            menu.add_command(label="Exit")

    def create_bubble(self, parent, chatNum, message, recieved=False):
        if (recieved):
            sticky_pos = 'nw'
        else:
            sticky_pos = 'ne'

        parent.rowconfigure(chatNum)
        bubble = ttk.Label(
                parent,
                style='Bubble.TLabel',
                text=message,
                anchor=tk.CENTER)
        bubble.grid(column=0, row=chatNum, pady=2, sticky=sticky_pos)


    def generate_widgets(self):
        # Create menu bar
        menubar = ttk.Frame(
                self,
                style='DarkGrey.TFrame')
        menubar.grid(column=0, row=0, columnspan=2, sticky='nsew')

        self.create_menu(menubar)

        # Create main containers
        left_container = ttk.Frame(
                self,
                style='LightGrey.TFrame')
        left_container.grid(column=0, row=1, sticky='nsew')

        right_container = ttk.Frame(
                self,
                style='DarkGrey.TFrame')
        right_container.grid(column=1, row=1, sticky='nsew')

        # Configure the right container to contain
        right_container.rowconfigure(0, weight=1)
        right_container.rowconfigure(1, weight=0, minsize=20) # Keeps the chat_box small
        right_container.columnconfigure(0, weight=1)
        right_container.columnconfigure(1, weight=0)

        # Requires some extra info
        chat_container = ttk.Frame(
                right_container,
                style='DarkGrey.TFrame'
                )
        chat_container.grid(column=0, row=0, columnspan=2, sticky='nsew')

        chat_bubble_container = ttk.Frame(
                chat_container,
                style='DarkGrey.TFrame',
                padding=10)
        chat_bubble_container.pack(side='bottom', fill=tk.X)

        chat_bubble_container.columnconfigure(0, weight=1)
        self.create_bubble(chat_bubble_container, 0, 'Yo', False)
        self.create_bubble(chat_bubble_container, 1, 'Bro', True)

        chat_entry = ttk.Entry(
                right_container
                )
        chat_entry.grid(column=0, row=1, sticky='nsew')

        chat_button = ttk.Button(
                right_container,
                text='Send',
                style='Send.TButton'
                )
        chat_button.grid(column=1, row=1, sticky='nsew')
