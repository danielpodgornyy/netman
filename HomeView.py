import tkinter as tk
from tkinter import ttk

class HomeView(ttk.Frame):
    def __init__(self, root):
        # Add an outer padding
        super().__init__(root, padding=15)

        self.create_styles()
        self.configure(style = 'Main.TFrame')
        self.generate_home_widgets()


    def set_controller(self, controller):
        self.controller = controller

    def create_styles(self):
        self.style = ttk.Style()

        self.style.configure('.', font=('MathJax_SansSerif', 24))

        # Set style for main frame
        self.style.configure('Main.TFrame', background='#3E4248')

        # Set style for header
        self.style.configure('Header.TFrame')

        self.style.configure(
                'Header.TLabel',
                background='#2B2E32',
                font=('MathJax_SansSerif', 24),
                foreground='white')

        self.style.configure('Content.TFrame', background='#2B2E32')

        self.style.configure(
                'Content.TButton',
                background='#2B2E32',
                font=('MathJax_SansSerif', 14),
                foreground='white')

        self.style.map(
                'Content.TButton',
                background=[('active', '#2b2d41')])

    def createButton(self, container, name, row):
        button = ttk.Button(
                container,
                text=name,
                style='Content.TButton'
                )
        button.grid(column=0, row=row, sticky='nesw')

    def generate_home_widgets(self):

        # HEADER
        header_container = ttk.Frame(
                self,
                padding=2,
                style='Header.TFrame'
                )
        header_container.pack()

        header = ttk.Label(
                header_container,
                text='NetMan',
                style='Header.TLabel',
                anchor=tk.CENTER,
                )
        header.pack(ipadx='10', ipady='5')

        # CONTENT

        content_container = ttk.Frame(
                self,
                padding=10,
                )

        content_container.place(width=200, height=170, relx=0.5, rely=0.5, anchor=tk.CENTER)

        # CURRENTLY AVAILABLE FUNCTIONS
        functions = ('Chat', 'TBD', 'TBD', 'TBD')

        # configure grid within content_container
        content_container.columnconfigure(0, weight=1)
        for row in range(len(functions)):
            content_container.rowconfigure(row, weight=1)

        # Populate content entries
        for row, name in enumerate(functions):
            self.createButton(content_container, name, row)

        #sizegrip = ttk.Sizegrip(self)



