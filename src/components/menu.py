import customtkinter as ctk
import tkinter as tk

from modules.cameras import detect_camera
from modules.app_state import AppState
from modules.log_client import LogClient

class Menu(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color='darkgray', **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        
        self.app_state = AppState()
        self.logger = LogClient()
        
        self.detect_camera = ctk.CTkButton(self, text="Detect camera", command=self.app_state.update_camera, state="disabled")
        self.detect_camera.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.predict = ctk.CTkButton(self, text="Start prediction", command=self.update_predict_button, state="disabled")
        self.predict.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.record = ctk.CTkButton(self, text="Record video", command=self.update_record_button, state="disabled")
        self.record.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.fg_color = self.detect_camera.cget("fg_color")
        
        self.app_state.camera_detected.trace_add('write', self.update_buttons_state)

    def update_buttons_state(self, *args):
        if self.app_state.camera_detected.get():
            self.detect_camera.configure(state="disabled")
            self.predict.configure(state="normal")
            self.record.configure(state="normal")
        else:
            self.detect_camera.configure(state="normal")
            self.predict.configure(state="disabled")
            self.record.configure(state="disabled")

    def update_predict_button(self):
        if not self.app_state.predicting.get():
            self.logger.log("Started prediction.", "info")
            
            self.predict.configure(fg_color="red")
            
            self.app_state.predicting.set(True)
        else:
            self.logger.log("Stopped prediction.", "info")
            
            self.predict.configure(fg_color=self.fg_color)
            
            self.app_state.predicting.set(False)
        
    def update_record_button(self):
        if not self.app_state.recording.get():
            self.logger.log("Started recording.", "info")
            
            self.record.configure(fg_color="red")
            
            self.app_state.recording.set(True)
        else:
            self.logger.log("Stopped recording.", "info")
            
            self.record.configure(fg_color=self.fg_color)
            
            self.app_state.recording.set(False)
