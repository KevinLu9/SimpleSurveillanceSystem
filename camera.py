## Simple Surveillance System ##
## Author: Kevin Lu ##
## Start Date: 08/12/2022 ##

import cv2
import time
import threading


class CameraCapture(object):
    def __init__(self, index):
        self.cam = cv2.VideoCapture(index)
        (self.grabbed, self.frame) = self.cam.read()
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        self.height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.index = index
        threading.Thread(target=self.update, args=()).start()
        self.status = True
        self.MAX_TIMEOUT_SECONDS = 20
        self.timeout = 0

        
    def __str__(self):
        out = f"Camera: {self.index}, "
        out += f"RES: {int(self.width)} x {int(self.height)}, "
        out += f"FPS: {int(self.fps)}"
        return out


    def get_frame(self):
        if self.status:
            image = self.frame
            return image
            #_, jpeg = cv2.imencode('.jpg', image)
            #return jpeg.tobytes()
        else:
            # Handle Timeout countdown
            count = self.MAX_TIMEOUT_SECONDS -(time.time() - self.timeout)
            if time.time() - self.timeout >= self.MAX_TIMEOUT_SECONDS:
                self.__del__()   
            #
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
        while True:
            g, f = self.cam.read()
            if f is not None:
                (self.grabbed, self.frame) = (g, f)
                self.status = True
            else:
                if self.status:
                    self.timeout = time.time()
                self.status = False
                
                
    def __del__(self):
        self.cam.release()


if __name__ == "__main__":
    cam = CameraCapture(0)
    print(cam)
    
    while True:
        aframe = cam.get_frame()
        cv2.imshow(f"Camera {cam.index}", aframe)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            del cam
            break
    cv2.destroyAllWindows()
