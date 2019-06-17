from realsense_camera import camera_control
from arduino import arduino_control
import time
import cv2
from tools import time_stamping
import os

def grabLidarAndImages(save=True):
    A_Control = arduino_control.ArduinoControl(port='')
    Camera = camera_control.D435RealSenseCamera((640, 480), 30)
    A_Control.connect()
    Camera.addColorStream()
    Camera.start()
    time.sleep(2)
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    if save:
        path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='saved_images')
    count = 0
