import customtkinter as ctk
import tkinter as tk

from modules.app_state import AppState
from modules.log_client import LogClient

class Menu(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color='darkgray', **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        
        self.app_state = AppState()
        self.logger = LogClient()
        
        self.detect_camera = ctk.CTkButton(self, text="Detect camera", command=self.button1_action, state="disabled")
        self.detect_camera.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.predict = ctk.CTkButton(self, text="Start prediction", command=self.button2_action, state="disabled")
        self.predict.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.record = ctk.CTkButton(self, text="Record video", command=self.button3_action, state="disabled")
        self.record.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.app_state.camera_detected.trace_add('write', self.update_buttons_state)

    def update_buttons_state(self, *args):
        if self.app_state.camera_detected:
            self.detect_camera.configure(state="disabled")
            self.predict.configure(state="normal")
            self.record.configure(state="normal")
        else:
            self.detect_camera.configure(state="normal")
            self.predict.configure(state="disabled")
            self.record.configure(state="disabled")
        
    def button1_action(self):
        self.logger.log("Detecting camera...", "info")

    def button2_action(self):
        self.logger.log("Starting prediction...", "info")
        
    def button3_action(self):
        self.logger.log("Recording video...", "info")
