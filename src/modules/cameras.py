import cv2

from cv2_enumerate_cameras import enumerate_cameras

from modules.log_client import LogClient

def detect_camera():
    logger = LogClient()
    logger.log("Detecting camera...", "info")
    
    cameras = enumerate_cameras()
    if cameras:
        camera = cameras[0]
        
        logger.log("Camera detected: {}.".format(camera.name), "info")
        
        return camera
    else:
        logger.log("No camera detected.", 'warning')
        
        return None