import tkinter as tk
from tkinter import ttk

class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas and a vertical scrollbar
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vscrollbar.config(command=canvas.yview)

        self.canvas = canvas

        # Create a frame inside the canvas which will be scrolled with
        self.interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

        # Update scroll region when the interior frame is resized
        def _configure_interior(event):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)  # Update scrollregion
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Sync the canvas width to match the interior frame's width
                self.canvas.config(width=self.interior.winfo_reqwidth())

        self.interior.bind('<Configure>', _configure_interior)

        # Update the width of the inner frame when the canvas is resized
        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)

        # Scroll view reset (if needed)
        self.canvas.yview_moveto(0)


