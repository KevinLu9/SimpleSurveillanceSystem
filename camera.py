import cv2
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

        
    def __str__(self):
        out = f"Camera: {self.index}, "
        out += f"RES: {int(self.width)} x {int(self.height)}, "
        out += f"FPS: {int(self.fps)}"
        return out


    def get_frame(self):
        image = self.frame
        return image
        # Output as JPG for webapp video feed
        #_, jpeg = cv2.imencode('.jpg', image)
        #return jpeg.tobytes()


    def update(self):
        while True:
            self.grabbed, self.frame = self.cam.read()
 

    def __del__(self):
        self.cam.release()


if __name__ == "__main__":
    cam = CameraCapture(0)
    print(cam)
    
    while True:
        cv2.imshow(f"Camera {cam.index}", cam.get_frame())
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            del cam
            break
    cv2.destroyAllWindows()
