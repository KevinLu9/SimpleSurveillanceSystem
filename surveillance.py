## Simple Surveillance System ##
## Author: Kevin Lu ##
## Start Date: 08/12/2022 ##

from camera import CameraCapture
import cv2



def start():
"""
Starts cameras and connections for surveillance
"""
    camera_count = 2
    cameras = []
    cameras_forcequit = False
    for i in range(camera_count):
        cameras.append(CameraCapture(i))
        print("Initialized " + str(cameras[i]))
    
    while True:
        cameras_forcequit = True
        for i in range(camera_count):
            cv2.imshow(f"Camera {cameras[i].index}", cameras[i].get_frame())
            cameras_forcequit = cameras_forcequit and cameras[i].forcequit
        if cv2.waitKey(1) & 0xFF == ord('q') or cameras_forcequit:
            for i in range(camera_count):
                cameras[i].forcequit = True
            break
        
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start()
