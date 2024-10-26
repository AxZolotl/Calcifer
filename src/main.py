import customtkinter as ctk

from views.app_view import AppView

# Initialize customtkinter
ctk.set_appearance_mode("Dark")  # Can be "System", "Dark" or "Light"
ctk.set_default_color_theme("dark-blue")  # Sets a default theme color

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CalciferNet")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.resizable(False, False)
    
        self.app_view = AppView(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
