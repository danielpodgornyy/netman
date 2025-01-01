import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showerror

from utils.Status import Status
from views.utils.VerticalScrolledFrame import VerticalScrolledFrame
from views.utils.PromptWindow import PromptWindow


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

    def set_controller(self, controller):
        self.controller = controller

    def create_styles(self):
        self.style = ttk.Style()

        self.style.configure('.', font=('MathJax_SansSerif', 24))

        # Background styles
        self.style.configure('LightGrey.TFrame', background='#3E4248')
        self.style.configure('DarkGrey.TFrame', background='#2B2E32')
        self.style.configure('TMenubutton', font=('MathJax_SansSerif', 10), padding=0)
        self.style.configure('Profile.TLabel', font=('MathJax_SansSerif', 20), padding=0, background='#3E4248', foreground='white')
        self.style.configure('Send.TButton', font=('MathJax_SansSerif', 10), padding=0)

        self.style.configure('Prompt.TLabel', font=('MathJax_SansSerif', 10), padding=0 )

    def create_menu(self, frame):
            # PROGRAMS
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

            # CHAT
            chat_menu = ttk.Menubutton(
                    frame,
                    text='Chat',
                    direction='below',
                    )
            chat_menu.grid(row=0, column=1, sticky='n')

            # Create chat menu
            chat = tk.Menu(chat_menu, tearoff=0)
            chat_menu['menu'] = chat

            # Add chat option
            chat.add_command(label="Add Chat")

            # SERVER
            chat_menu = ttk.Menubutton(
                    frame,
                    text='Server',
                    direction='below',
                    )
            chat_menu.grid(row=0, column=2, sticky='n')

            # Create chat menu
            chat = tk.Menu(chat_menu, tearoff=0)
            chat_menu['menu'] = chat

            # Add chat option
            chat.add_command(label="Connect to Server", command=lambda: self.prompt_connect_to_server())

    def create_chat(self, parent, chat_num, name):
        parent.rowconfigure(chat_num, weight=1)
        chat_profile = tk.Frame(parent.interior, background='white')
        chat_profile.grid(column=0, row=chat_num, padx=1, pady=1, sticky='new')

        name = ttk.Label(
                chat_profile,
                text=name,
                padding = (0, 10),
                style='Profile.TLabel',
                anchor=tk.CENTER
                )
        name.pack(fill=tk.X)

    def add_text(self, textbox, text):
        textbox.config(state=tk.NORMAL)
        textbox.insert(tk.END, '>: ' + text + '\n')
        textbox.config(state=tk.DISABLED)

    def generate_left_content(self, left_container):
        # USE INTERIOR TO REFERENCE THE FRAME
        self.chat_container = VerticalScrolledFrame(left_container)
        self.chat_container.pack(side='top', fill=tk.BOTH, expand=True)

        # set frame background
        self.chat_container.canvas.config(background='#3E4248')


        # Configure the left container to contain the chatlist
        self.chat_container.interior.columnconfigure(0, weight=1)
        self.chat_container.interior.rowconfigure(0, weight=1)

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
        chat_response.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self.add_text(chat_response, '--- CONNECT TO A SERVER ---')

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
                style='LightGrey.TFrame'
                )
        left_container.grid(column=0, row=1, sticky='nsew')

        right_container = ttk.Frame(
                self,
                style='DarkGrey.TFrame'
                )
        right_container.grid(column=1, row=1, sticky='nsew')

        self.generate_left_content(left_container)
        self.generate_right_content(right_container)

    # DYNAMIC PROMPTS AND CHANGES

    def prompt_connect_to_server(self):
        # Create prompt for IP address
        prompt_window = PromptWindow(self.parent, 'Enter IP Address')
        prompt_window.grab_set()

        prompt = ttk.Label(
                prompt_window.prompt_container,
                text='Enter valid server IP address:',
                style='Prompt.TLabel'
                )
        prompt.grid(column=0, row=0, sticky='nesw')

        result = tk.StringVar()
        textbox = ttk.Entry(
               prompt_window.prompt_container,
               textvariable = result
                )
        textbox.grid(column=1, row=0, sticky='ew')

        # Allows me to both destroy the window and call the controller method on the same line
        textbox.bind('<Return>', lambda e: (prompt_window.destroy(), self.try_connection(result.get())))

    def try_connection(self, ip_address):
        # Try to connect to the server, routing through the controller
        connection_successful = self.controller.init_connect_to_server(ip_address)

        if (connection_successful == Status.SUCCESS):
            # Prompt for a username
            self.prompt_username()

            # Pull data from the server and populate page appropriately
            # chatlist = self.controller.get_open_chats()
        elif (connection_successful == Status.SYNTAX_ERROR):
            showerror(
                    title='Syntax Error',
                    message='Syntax is invalid'
                    )
        else: # 0
            showerror(
                    title='Connection Failed',
                    message='Error, connection couldn\'t be made'
                    )

    def prompt_username(self):
        # Create prompt for username
        prompt_window = PromptWindow(self.parent, 'Enter username')
        prompt_window.grab_set()

        prompt = ttk.Label(
                prompt_window.prompt_container,
                text='Enter username:',
                style='Prompt.TLabel'
                )
        prompt.grid(column=0, row=0, sticky='nesw')

        result = tk.StringVar()
        textbox = ttk.Entry(
               prompt_window.prompt_container,
               textvariable = result
                )
        textbox.grid(column=1, row=0, sticky='ew')

        textbox.bind('<Return>', lambda e: (prompt_window.destroy(), self.try_send_username(result.get())))

    def try_send_username(self, username):
        response_code = int(self.controller.send_username(username))

        # SUCCESS
        if response_code == 200:
            self.populate_window()
        elif response_code == 409:
            showerror(
                    title='Conflict Error',
                    message='Username already exists on this server'
                    )
        else:
            showerror(
                    title='Error',
                    message='An error has occured'
                    )

    def populate_window(self):
        #page_data
        chat_list = self.controller.get_chats()

        for index, chat_name in enumerate(chat_list):
            self.create_chat(self.chat_container, index, chat_name)

