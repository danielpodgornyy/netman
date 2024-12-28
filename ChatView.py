import tkinter as tk
from tkinter.scrolledtext import ScrolledText
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

        self.style.configure('Profile.TLabel', font=('MathJax_SansSerif', 20), padding=0, background='#3E4248', foreground='white')  # Change font size and padding

        self.style.configure('Send.TButton', font=('MathJax_SansSerif', 10), padding=0)  # Change font size and padding`

        self.style.configure('Bubble.TLabel', font=('MathJax_SansSerif', 15), padding=4 )

    def create_menu(self, frame):
            programs_menu = ttk.Menubutton(
                    frame,
                    text='Programs',
                    direction='below',
                    )
            programs_menu.grid(row=0, column=0, sticky='n')

            # Create programs menu
            programs = tk.Menu(programs_menu, tearoff=0)
            programs_menu['menu'] = programs

            # Add programs
            programs.add_command(label="Home", command=lambda: self.parent.switch_frame('home'))
            programs.add_command(label="Option 2")


            chats_menu = ttk.Menubutton(
                    frame,
                    text='Chats',
                    direction='below',
                    )
            chats_menu.grid(row=0, column=1, sticky='n')

            # Create programs menu
            chats = tk.Menu(chats_menu, tearoff=0)
            chats_menu['menu'] = chats

            # Add programs
            chats.add_command(label="Add Chat")
            chats.add_command(label="Option 2")

    def create_chat(self, parent, chat_num, name):
        parent.rowconfigure(chat_num, weight=1)
        chat_profile = tk.Frame(parent, background='white')
        chat_profile.grid(column=0, row=chat_num, padx=1, pady=1, sticky='new')

        name = ttk.Label(
                chat_profile,
                text=name,
                padding = (0, 10),
                style='Profile.TLabel',
                anchor=tk.CENTER)
        name.pack(fill=tk.X)

    def generate_left_content(self, left_container):

        chats = ttk.Frame(left_container)
        chats.pack(side='top', fill=tk.X)

        # Configure the left container to contain the chatlist
        chats.columnconfigure(0, weight=1)
        self.create_chat(chats, 0, 'id')
        self.create_chat(chats, 1, 'Billy')

    def generate_right_content(self, right_container):
        # Configure the right container to contain chat functionality
        right_container.rowconfigure(0, weight=1)
        right_container.rowconfigure(1, weight=0, minsize=20) # Keeps the chat_box small
        right_container.columnconfigure(0, weight=1)
        right_container.columnconfigure(1, weight=0)

        chat_response = ScrolledText(
                right_container,
                background='#2B2E32',
                foreground='white',
                highlightcolor='white'
                )
        chat_response['state'] = 'disabled'
        chat_response.grid(column=0, row=0, columnspan=2, sticky='nsew')
        chat_response.insert('1.0', 'This is a Text widget demo')


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


    def generate_widgets(self):
        # Create menu bar
        menubar = ttk.Frame(
                self)
        menubar.grid(column=0, row=0, columnspan=2, sticky='nsew')

        self.create_menu(menubar)

        # MAIN CONTAINERS
        left_container = ttk.Frame(
                self,
                style='LightGrey.TFrame')
        left_container.grid(column=0, row=1, sticky='nsew')

        right_container = ttk.Frame(
                self,
                style='DarkGrey.TFrame')
        right_container.grid(column=1, row=1, sticky='nsew')

        self.generate_left_content(left_container)
        self.generate_right_content(right_container)

