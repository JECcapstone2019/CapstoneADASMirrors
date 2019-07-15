import cv2
import time
import sys
from imutils.video import FPS
import os
import numpy as np
import re

class VirtualStream:
    def __init__(self, numpyFolder):
        self.folder = numpyFolder
        self.np_images = {}
        for image in os.listdir(self.folder):
            if '.npy' in image:
                path = os.path.join(self.folder, image)
                self.np_images[int(re.search(r'\d+', image).group())] = path
        self.count = 200
        self.end = len(self.np_images) - 1
    
    def grabImage(self):
        image = np.load(self.np_images[self.count])
        self.count += 1
        if self.count >= self.end:
            self.reset()
        return image
    
    def reset(self):
        self.count = 0






testData = true

# get video source
def getVideo():
    try:
        vs = cv2.VideoCapture(sys.argv[1])
    except:
        print("ERROR: Path to video missing from arugument")
        sys.exit()
    return vs


#tracker = cv2.TrackerKCF_create()  # openCV tracker api to track objects (specifically KCF tracker)
roi = None                         # initilize box used to hi-light objects
fps = None                         # inizilize fps of video

if testData != True:
    videoStream = getVideo()
else:
    vs = VirtualStream('/Users/user/Desktop/saved_images_2019_6_13-17_49_52')

while True:
    # grab new frame
    if testData != True:
        bool_result, frame = videoStream.read()
    else:
        frame = vs.grabImage()
        bool_result = True

    

    if bool_result == None: # No more frames
        break

    if roi == None: # initilize roi
        roi = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
        tracker = cv2.TrackerKCF_create()
        test = tracker.init(frame, roi)
        print('roi initilize correctly:',test)
        fps = FPS().start() # currently not being used
    else:             # update roi
        bool_updated, box = tracker.update(frame)
        if bool_updated == True:
            (x, y, w, h) = [int(i) for i in box] # box holds new roi coordinates
            pt1 = (x,y)
            pt2 = (x+w, y+h)
            cv2.rectangle(frame, pt1, pt2, (0,255,0), 2)
        if bool_updated == False:
            roi = None
            cv2.destroyAllWindows()
            continue
    
        # we are not currently account for the case when update is false
        # this happens when the object if not longer found
        # ex: object has left frame

        fps.update()
        fps.stop()

    # display frame wtracith roi
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF  # issue here is that frames are displayed for 1ms... we dont display majority of frames

    if key == 'a':
        # this is where we will add the code to add a new roi
        pass

    if key == ord('q'):
        break

cv2.destroyAllWindows()




