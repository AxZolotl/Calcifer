import customtkinter as ctk

from modules.log_client import LogClient
class Log(ctk.CTkTextbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, font=("Calibri", 18), state="disabled", **kwargs)
        self.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0,25))
        
        self.logger = LogClient()
        self.logger.current_log.trace_add('write', self.add_log)
        
    def add_log(self, *args):
        self.configure(state="normal")
        self.insert("end", self.logger.current_log.get() + "\n")
        self.yview("end")
        self.configure(state="disabled")