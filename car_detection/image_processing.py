import cv2
from tools import image_tools
import multiprocessing
import queue
import time

class ImageProcessor(multiprocessing.Process):
    def __init__(self, imageQueue, roiQueue, *args, **kwargs):
        multiprocessing.Process.__init__(*args, **kwargs)
        self.car_detected = False
                            # x,  y,  h,  w
        self.car_position = [-1, -1, -1, -1]
        self.frame_timestamp = 0
        self.tracker = None

        self.threshold = 0
        self.frame = None

        self.image_queue = imageQueue
        self.roi_queue = roiQueue

        self.abort = False

        self.cascade_src = 'cars.xml'
        self.car_cascade = cv2.CascadeClassifier(self.cascade_src)

    # Put the car position and a timestamp into the queue
    def sendCarInformation(self):
        try:
            self.roi_queue.put((self.car_position_update_time, self.car_position), block=False)
        except queue.Full:
            pass

    # Constant loop that processes images as they come
    def run(self):
        while(not(self.abort)):
            # Check if data has been requested
            # do your image processing here
            self.runCarDetection()
            self.sendCarInformation()

    def runCarDetection(self):
        try:
            self.frame, self.frame_timestamp = self.image_queue.get(block=False)
            # DO CAR DETECTION HERE
            #
            #
        except queue.Empty:
            pass
        time.sleep(0.001)

    # will reset all nessasary flags
    def carLost(self):
        self.car_position = [-1, -1, -1, -1]
        self.car_detected = False

    def kill(self):
        self.abort = True

class TrackerTesting(ImageProcessor):
    def __init__(self, folderPath='C:\\Users\\e_q\\Documents\\sourcetree\\main_program\\car_detection\\saved_images_2019_6_13-17_49_52\\'):
        ImageProcessor.__init__(self, imageQueue=None, dataPipe=None)
        self.virtual_stream = image_tools.VirtualStream(numpyFolder=folderPath)
        self.frame_name = 'frame'

    def run(self):
        while True:
            if self.car_detected:
                self.runTracking()
                if self.car_detected:
                    self.trackingViewer()
            else:
                self.runCarDetection()

    def getFrame(self):
        return self.virtual_stream.grabImage()

    def runCarDetection(self):
        self.frame = self.getFrame()

        # maual placment of roi
        #roi = cv2.selectROI(self.frame_name, self.frame, fromCenter=False, showCrosshair=True)
        
        # detecting car using haar cascade 
        gray_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        roi = self.car_cascade.detectMultiScale(gray_img, 1.1, 2.0) # this could petentially return more then 1 roi

        if len(roi)>1:
            roi = self.selectROI(roi)


        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(self.frame, roi)

        self.car_position = list(roi)
        self.car_detected = True
        cv2.destroyAllWindows()

    def trackingViewer(self):
        pt1 = (self.car_position[0], self.car_position[1])
        pt2 = (self.car_position[2], self.car_position[3])
        cv2.rectangle(self.frame, pt1, pt2, (0, 255, 0), 2)
        cv2.imshow(self.frame_name, self.frame)
        cv2.waitKey(33)

    def selectROI(self, roi):
        # option 1: maybe just set bounds
        # option 2: use dominant colour -> implimentation looks kinda complicated/ computationally intensive 
        # option 3: always return first roi 
        return roi[0]



if __name__ == '__main__':
    # main_pipe, process_pipe = Pipe()
    # image_queue = Queue()
    # image_processor = ImageProcessor(imageQueue=image_queue, dataPipe=process_pipe)
    # running_process = Process(target=image_processor.run, args=(None,))
    # running_process.start()

    testing = TrackerTesting()
    testing.run()
