## Camera Class ##
## Author: Kevin Lu ##
## Start Date: 08/12/2022 ##

import cv2
import time
import threading
import numpy as np

class CameraCapture(object):
    def __init__(self, index):
        # Initialize camera variables
        self.cam = cv2.VideoCapture(index)
        (self.grabbed, self.frame) = self.cam.read()
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        self.height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.index = index
        self.status = True
        self.MAX_TIMEOUT_SECONDS = 20
        self.timeout = time.time()
        self.forcequit = False
        # Initialization when no camera is available
        if self.frame is None:
            self.frame = np.full((480, 640, 3), np.uint8(0))
            self.height = 480
            self.width = 640
        self.rec = threading.Thread(target=self.update, args=()).start()
        
        

        
    def __str__(self):
        out = f"Camera: {self.index}, "
        out += f"RES: {int(self.width)} x {int(self.height)}, "
        out += f"FPS: {int(self.fps)}"
        return out


    def get_frame(self):
    """
    Gets the next frame from memory
    """
        if self.status:
            image = self.frame
            return image
            #_, jpeg = cv2.imencode('.jpg', image)
            #return jpeg.tobytes()

        # Handle Timeout countdown
        count = self.MAX_TIMEOUT_SECONDS -(time.time() - self.timeout)
        if time.time() - self.timeout >= self.MAX_TIMEOUT_SECONDS:
            self.forcequit = True 
        # Add text to camera feed
        font = cv2.FONT_HERSHEY_SIMPLEX
        self.cam = cv2.VideoCapture(self.index)
        image = self.frame.copy()
        return cv2.putText(image,
                           f"No Camera Signal, Timeout in: {round(count, 2)}s",
                           (4, int(self.height//2)),
                           font,
                           1,
                           (0, 0, 255),
                           1,
                           cv2.LINE_AA)


    
    def update(self):
    """
    Gets the next frame from the camera and writes it to memory
    """
        while True:
            try:
                g, f = self.cam.read()
                if f is not None:
                    (self.grabbed, self.frame) = (g, f)
                    self.status = True
                else:
                    raise exception("Camera Feed Error")
            except:  # camera not plugged in so cam.read() returns exception
                if self.status:
                    self.timeout = time.time()
                    self.status = False
            if self.forcequit:
                break
        # Terminate camera
        self.cam.release()
                
                
    def __del__(self):
        self.cam.release()

