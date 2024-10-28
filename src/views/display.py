import customtkinter as ctk
from components.menu import Menu
from components.feed import Feed

class Display(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.init_layout()
        self.init_ui()

    def init_layout(self):
        self.rowconfigure(0, weight=0) 
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)
        
    def init_ui(self):
        Menu(self)
        Feed(self)
