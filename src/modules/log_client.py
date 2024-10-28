import tkinter as tk
import logging
import threading
import os

from datetime import datetime

class LogClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(self, *args, **kwargs):
        with self._lock:
            if self._instance is None:
                self._instance = super(LogClient, self).__new__(self)
                
        return self._instance

    def initialize_logger(self):
        self._current_log = tk.StringVar(value='')
        
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)

        log_file_path = self._get_daily_log_file()

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        custom_handler = SystemLogHandler(self)
        custom_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        custom_handler.setFormatter(formatter)
        

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(custom_handler)

    def _get_daily_log_file(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file_path = os.path.join(log_dir, f"{today}.txt")

        if not os.path.exists(log_file_path):
            with open(log_file_path, "w") as file:
                file.write("")

        return log_file_path

    def log(self, message, level='info'):
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        else:
            self.logger.info(message)
            
    @property
    def current_log(self):
        return self._current_log

class SystemLogHandler(logging.Handler):
        def __init__(self, log_client):
            super().__init__()
            self.log_client = log_client

        def emit(self, record):
            log_message = self.format(record)
            self.log_client.current_log.set(log_message)