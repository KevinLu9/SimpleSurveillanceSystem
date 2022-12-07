## Human Detection Surveillance Camera ##
## Author: Kevin Lu ##

import cv2
import imutils
import numpy as np
import time

# Initialize Camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
print(f"Camera Resolution: {frame_width}x{frame_height}")

while True:    
    ret, frame = cam.read()
    timeStr = time.asctime().replace("  ", " ").replace(" ", "_").replace(":", "-")
    frameDetails = f"TIME: {timeStr}"
    lastSampleTime = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, frameDetails, (7, 70), font, 1, (255, 255, 255), 3, cv2.LINE_AA)   

    # Show video in window
    cv2.imshow('Camera', frame)

    # Quit condition by key interrupt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
