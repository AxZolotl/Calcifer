import customtkinter as ctk
from components.display import Display
from components.log_area import LogArea

class AppView(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master, 
            fg_color='white', 
            **kwargs
        )
        
        self.grid(row=0, column=0, sticky="nsew")
        self.pack(fill="both", expand=True)
        self.init_ui()

    def init_ui(self):
        self.columnconfigure(0, weight=67)
        self.columnconfigure(1, weight=33)
        self.rowconfigure(0, weight=1)

        self.display = Display(self)
        self.log_area = LogArea(self)
