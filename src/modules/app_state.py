import tkinter as tk
import threading

from modules.cameras import detect_camera
from modules.log_client import LogClient
from modules.db_client import DBClient

class AppState:
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(AppState, self).__new__(self)
            
        return self._instance
    
    def initialize_state(self):
        self._status = tk.StringVar(value="initializing")
        self._camera = None
        self._camera_detected = tk.BooleanVar(value=False)
        self._predicting = tk.BooleanVar(value=False)
        self._recording = tk.BooleanVar(value=False)
        
        self._logger = LogClient()

    @property
    def status(self):
        return self._status
    
    @property
    def camera(self):
        return self._camera
    
    @property
    def camera_detected(self):
        return self._camera_detected

    @property
    def predicting(self):
        return self._predicting

    @property
    def recording(self):
        return self._recording
    
    def update_state(self):
        self._logger.log("Detecting camera...", "info")
        
        self._camera = detect_camera()
        
        if self.camera:
            self._logger.log("Camera detected: {}.".format(self.camera.name), "info")
            self.camera_detected.set(True)
        else:
            self._logger.log("No camera detected.", 'warning')
        
        self._logger.log("Connecting to the database...", "info")
        self.db = DBClient()
        self.db.init_connection()