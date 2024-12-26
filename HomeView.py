import tkinter as tk
from tkinter import ttk

class HomeView(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.generate_home_widgets()

    def set_controller(self, controller):
        self.controller = controller

    def create_styles(self):
        self.style = ttk.Style()

        # Set style for header
        self.style.configure('Header.TFrame', background='black')
        self.style.configure('Header.TLabel',
                             background='black',
                             font=('MathJax_SansSerif', 24),
                             foreground='white',
                             anchor='center')


    def generate_home_widgets(self):

        self.create_styles()

        header_container = ttk.Frame(
                self,
                padding=(20, 0, 20, 5),
                style='Header.TFrame'
                )

        header_container.pack()

        header = ttk.Label(
                header_container,
                text='Netscope',
                style='Header.TLabel')
        header.pack()

        #sizegrip = ttk.Sizegrip(self)

