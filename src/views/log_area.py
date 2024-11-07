import customtkinter as ctk
from components.log import Log

class LogArea(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.grid(row=0, column=1, sticky="nsew", padx=(5,0))
        
        self.rowconfigure(0, weight=0) 
        self.rowconfigure(1, weight=100)
        self.columnconfigure(0, weight=1)
        
        self.label = ctk.CTkLabel(self, text="System Logs", font=("Calibri", 20))
        self.label.grid(row=0, column=0, sticky="nw", padx=25, pady=25)
        
        Log(self)