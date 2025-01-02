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

        # Keeps track of the string within the entry box
        self.entry_var = tk.StringVar()

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

        # Once controller is set, if the window is deleted, leave the server
        self.parent.protocol("WM_DELETE_WINDOW", lambda: (self.controller.leave_server(), self.parent.destroy()))

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
            chat.add_command(label="Add Chat", command=lambda: self.prompt_add_chat())

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

    def create_chat(self, parent, chat_num, chat_name):
        parent.rowconfigure(chat_num, weight=1)
        chat_profile = tk.Frame(parent.interior, background='white')
        chat_profile.grid(column=0, row=chat_num, padx=1, pady=1, sticky='new')

        name = ttk.Label(
                chat_profile,
                text=chat_name,
                padding = (0, 10),
                style='Profile.TLabel',
                anchor=tk.CENTER
                )
        name.pack(fill=tk.X)

        # Bind to the container and name
        chat_profile.bind('<Button-1>', lambda e: self.populate_chat_data(chat_name))
        name.bind('<Button-1>', lambda e: self.populate_chat_data(chat_name))

    def add_text(self, textbox, text):
        textbox.config(state=tk.NORMAL)
        textbox.insert(tk.END, '>: ' + text + '\n')
        textbox.config(state=tk.DISABLED)

    def clear_text(self, textbox):
        textbox.config(state=tk.NORMAL)
        textbox.delete("1.0", tk.END)
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

        self.chat_response = ScrolledText(
                right_container,
                background='#2B2E32',
                foreground='white',
                highlightcolor='white'
                )
        self.chat_response.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self.add_text(self.chat_response, '--- CONNECT TO A SERVER ---')

        chat_entry = ttk.Entry(
                right_container,
                textvariable=self.entry_var
                )
        chat_entry.grid(column=0, row=1, sticky='nsew')

        chat_button = ttk.Button(
                right_container,
                text='Send',
                style='Send.TButton',
                command=self.enter_log
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
        # Result string
        result = tk.StringVar()

        # Create prompt for IP address
        prompt_window = PromptWindow(self.parent, 'Enter valid IP Address', result)
        prompt_window.grab_set()

        # Allows me to both destroy the window and call the controller method on the same line
        prompt_window.textbox.bind('<Return>', lambda e: (prompt_window.destroy(), self.try_connection(result.get())))

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
        # Keep resultant string
        result = tk.StringVar()

        # Create prompt for username
        prompt_window = PromptWindow(self.parent, 'Enter username', result)
        prompt_window.grab_set()

        prompt_window.textbox.bind('<Return>', lambda e: (prompt_window.destroy(), self.try_send_username(result.get())))

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
        elif response_code == 406:
            showerror(
                    title='Username Error',
                    message='Username cannot be empty'
                    )
        else:
            showerror(
                    title='Error',
                    message='An error has occured'
                    )

    def populate_window(self):
        # Update the current chat_list
        chat_list = self.controller.get_chats()
        for index, chat_name in enumerate(chat_list):
            self.create_chat(self.chat_container, index, chat_name)
            self.chat_index = index

        # Update textbox
        self.clear_text(self.chat_response)
        self.add_text(self.chat_response, '--- SELECT A CHATROOM ---')

    def prompt_add_chat(self):
        # Keep resultant string
        result = tk.StringVar()

        # Create prompt for chat room name
        prompt_window = PromptWindow(self.parent, 'Enter chat room name:', result)
        prompt_window.grab_set()

        prompt_window.textbox.bind('<Return>', lambda e: (prompt_window.destroy(), self.try_add_chat(result.get())))

    def try_add_chat(self, chat_room_name):
        # Must be connected to a server
        if (not self.controller.server_is_active()):
             showerror(
                title='Server Error',
                message='Must be connected to a server'
                )
             return


        response_code = int(self.controller.add_chat(chat_room_name))

        # SUCCESS
        if response_code == 200:
            self.chat_index += 1
            self.create_chat(self.chat_container, self.chat_index, chat_room_name)
        elif response_code == 409:
            showerror(
                    title='Conflict Error',
                    message='Chat room already exists on this server'
                    )
        elif response_code == 406:
            showerror(
                    title='Chat Room Name Error',
                    message='Chat room name cannot be empty'
                    )
        else:
            showerror(
                    title='Error',
                    message='An error has occured'
                    )

    def populate_chat_data(self, chat_room_name):
        # Get, chatroom logs
        chat_logs = self.controller.get_chat_room_logs(chat_room_name)

        self.clear_text(self.chat_response)

        for log in chat_logs:
            self.add_text(self.chat_response, f'{log["username"]}: {log["message"]}')

    def enter_log(self):
        # Get username
        username = self.controller.get_username()

        # Save and clear var
        message = self.entry_var.get()
        self.entry_var.set('')

        response_code = int(self.controller.enter_log(username, message))

        if (response_code == 200):
            self.add_text(self.chat_response, f'{username}: {message}')
        else:
            self.add_text(self.chat_response, 'server: Message not sent, connection error')






