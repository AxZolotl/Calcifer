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
        self.app_state.initialize_state()
        
        self.logger = LogClient()
        self.logger.initialize_logger()
        
        self.init_layout()
        self.init_ui()
        
        self.after(0, self.state, 'zoomed')
        
        threading.Thread(target=self.app_state.update_state).start()
        
    def init_layout(self):
        self.columnconfigure(0, weight=67)
        self.columnconfigure(1, weight=33)
        self.rowconfigure(0, weight=1)
        
    def init_ui(self):
        Display(self)
        LogArea(self)
    
if __name__ == "__main__":
    App().mainloop()
