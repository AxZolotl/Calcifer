import cv2
import customtkinter as ctk
import threading
import numpy as np
import os

from datetime import datetime
from PIL import Image, ImageTk, ImageDraw

from modules.app_state import AppState
from modules.log_client import LogClient

class Feed(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)
        
        self.app_state = AppState()
        self.logger = LogClient()
        
        self.canvas = ctk.CTkCanvas(self, bg="gray16")
        self.canvas.pack(fill="both", expand=True)
        
        self.cap = None
        self.out = None
        self.start_time_recording = None
        self.temp_file_path = None
        self.stopEvent = threading.Event()
        
        self.app_state.camera_detected.trace_add('write', self.start_video_feed)
        self.app_state.recording.trace_add('write', self.update_recording_state)
        
        self.master.master.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    
    def start_video_feed(self, *args):
        if self.app_state.camera:
            self.cap = cv2.VideoCapture(self.app_state.camera.index, self.app_state.camera.backend)
            self.stopEvent.clear()
            self.update_video_feed()
    
    def update_recording_state(self, *args):
        if self.app_state.recording.get():
            self.start_time_recording = datetime.now().strftime('%Y-%m-%d, %H-%M-%S')
            assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
            os.makedirs(assets_path, exist_ok=True)

            temp_file_name = f"{self.start_time_recording}_unsaved.mp4"
            self.temp_file_path = os.path.join(assets_path, temp_file_name)
            
            print(self.temp_file_path)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            frame_width, frame_height = int(self.cap.get(3)), int(self.cap.get(4))
            self.out = cv2.VideoWriter(self.temp_file_path, fourcc, 20.0, (frame_width, frame_height))
        
        else:
            self.out.release()
            self.out = None

            end_time_recording = datetime.now().strftime('%Y-%m-%d, %H-%M-%S')
            final_file_name = f"{self.start_time_recording} - {end_time_recording}.mp4"
            final_file_path = os.path.join(os.path.dirname(self.temp_file_path), final_file_name)

            os.rename(self.temp_file_path, final_file_path)
            self.logger.log(f"Recording saved as {final_file_name}.", "info")
        
    def update_video_feed(self, *args):
        if not self.stopEvent.is_set():
            ret, frame = self.cap.read()
            if ret:
                if self.app_state.recording.get():
                    self.out.write(frame)

                frame = cv2.resize(frame, (self.winfo_width(), self.winfo_height()))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)

                if self.app_state.recording.get():
                    draw = ImageDraw.Draw(frame)
                    
                    radius = 15
                    x = frame.width - 70
                    y = 50
                    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="red")
                    
                    rec_text_position = (x + radius + 5, y - radius)
                    draw.text(rec_text_position, "REC", fill="red")

                tk_image = ImageTk.PhotoImage(frame)

                self.canvas.create_image(0, 0, image=tk_image, anchor='nw')
                self.canvas.image = tk_image

            self.after(1, self.update_video_feed)

    def onClose(self):
        self.logger.log("Closed program", "info")
        
        self.stopEvent.set()
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        self.master.master.destroy()