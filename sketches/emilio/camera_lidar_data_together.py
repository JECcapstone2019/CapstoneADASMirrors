from realsense_camera import camera_control
from arduino import arduino_control
import time
import cv2
from tools import time_stamping
import os
import csv
import numpy as np

COUNT = 'COUNT'
IMAGE_NAME = 'IMAGE_NAME'
IMAGE_TIME = 'IMAGE_TIME'
LIDAR_MEASUREMENT = 'LIDAR_MEASUREMENT'
LIDAR_TIME = 'LIDAR_TIME'
DICTIONARY = ["COUNT", "IMAGE_TIME", "IMAGE_NAME", "LIDAR_TIME", "LIDAR_MEASUREMENT"]

def grabLidarAndImages(port='COM_4', save=True):
    A_Control = arduino_control.ArduinoControl(port=port)
    Camera = camera_control.D435RealSenseCamera((640, 480), 30)
    A_Control.connect()
    Camera.addColorStream()
    Camera.start()
    time.sleep(2)
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='saved_images')
    count = 0
    filename = os.path.join(path, time_stamping.getTimeStampedString() + 'data.csv')
    with open(filename, 'wb') as csvFile:
        writer = csv.DictWriter(csvFile, DICTIONARY)
        writer.writeheader()
        writer_dict = {}
        while True:
            writer_dict[COUNT] = count
            frames = Camera.getFrames()
            camera_time = time_stamping.getTimeStampedString()
            lidar_meas = A_Control.sendCommand()
            writer_dict[LIDAR_TIME] = time_stamping.getTimeStampedString()
            writer_dict[LIDAR_MEASUREMENT] = lidar_meas
            image_name = 'image_%s.npy' % camera_time
            image_path = os.path.join(path, image_name)
            writer_dict[IMAGE_NAME] = image_name
            color_frame = frames.get_color_frame()
            if not color_frame:
                print("image not found")

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            np.save(image_path, color_image)
            print("Save")
            writer.writerow(writer_dict)
            count += 1

            # Show images
            cv2.imshow('RealSense', color_image)
            cv2.waitKey(33)