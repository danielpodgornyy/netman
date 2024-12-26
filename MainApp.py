import tkinter as tk
from tkinter import ttk

from HomeView import HomeView
from HomeController import HomeController

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Init root frame
        self.title('Netscope')
        self.resizable(True, True)

        # Create and pack main frame (psuedo root frame)
        view = HomeView(self)
        view.pack(fill='both', expand=True)

        # Create controller
        controller = HomeController()

        #Set the controller of the main view to the main controller
        view.set_controller(controller)


if (__name__ == '__main__'):
    # Create the root frame and initilize the tkinter application
    app = MainApp()
    app.mainloop()

