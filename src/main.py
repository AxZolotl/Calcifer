import customtkinter as ctk
import threading

from views.display import Display
from views.log_area import LogArea

from modules.app_state import AppState
from modules.log_client import LogClient

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("CalciferNet")
        
        self.app_state = AppState()
        self.logger = LogClient()
        
        self.app_state.initialize_state()
        self.logger.initialize_logger()
        
        self.columnconfigure(0, weight=67)
        self.columnconfigure(1, weight=33)
        self.rowconfigure(0, weight=1)
        
        Display(self)
        LogArea(self)
        
        self.after(0, self.state, 'zoomed')        
        threading.Thread(target=self.app_state.update_state).start()
    
if __name__ == "__main__":
    App().mainloop()
