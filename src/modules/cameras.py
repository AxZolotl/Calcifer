import cv2

from cv2_enumerate_cameras import enumerate_cameras

def detect_camera():
    cameras = enumerate_cameras()
    
    if cameras:
        return cameras[0]
    else:
        return None