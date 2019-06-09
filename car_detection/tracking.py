import cv2
import time
import sys
from imutils.video import FPS


# get video source
def getVideo():
    try:
        vs = cv2.VideoCapture(sys.argv[1])
    except:
        print("ERROR: Path to video missing from arugument")
        sys.exit()
    return vs


tracker = cv2.TrackerKCF_create()  # openCV tracker api to track objects (specifically KCF tracker)
roi = None                         # initilize box used to hi-light objects
fps = None                         # inizilize fps of video

videoStream = getVideo()

while True:
    # grab new frame
    bool_result, frame = videoStream.read()

    if bool_result == None: # No more frames
        break

    if roi == None: # initilize roi
        roi = cv2.selectROI("Frame", frame, fromCenter = False, showCrosshair = True)
        test = tracker.init(frame, roi)
        print('roi initilize correctly:',test)
        fps = FPS().start()
    else:             # update roi
        bool_updated, box = tracker.update(frame)
        if bool_updated == True:
            (x, y, w, h) = [int(i) for i in box] # box holds new roi coordinates
            pt1 = (x,y)
            pt2 = (x+w, y+h)
            cv2.rectangle(frame, pt1, pt2, (0,255,0), 2)
        # we are not currently account for the case when update is false
        # this happens when the object if not longer found
        # ex: object has left frame

        fps.update()
        fps.stop()

    # display frame with roi
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF  # issue here is that frames are displayed for 1ms... we dont display majority of frames

    if key == 'a':
        # this is where we will add the code to add a new roi
        pass

    if key == ord('q'):
        break

cv2.destroyAllWindows()




