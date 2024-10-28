import cv2
import customtkinter as ctk
import threading
import imutils
import sys

from PIL import Image
from PIL import ImageTk

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
        self.stopEvent = threading.Event()
        
        self.app_state.camera_detected.trace_add('write', self.start_video_feed)
        self.master.master.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    
    def start_video_feed(self, *args):
        self.cap = cv2.VideoCapture(self.app_state.camera.index, self.app_state.camera.backend)
        self.stopEvent.clear()
        self.update_video_feed()

    def update_video_feed(self, *args):
        if not self.stopEvent.is_set():
            ret, frame = self.cap.read()
            if ret:
                canvas_width = self.winfo_width()
                canvas_height = self.winfo_height()
                
                frame = cv2.resize(frame, (canvas_width, canvas_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
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