from multiprocessing import Queue, Pipe, Process
import cv2
from tools import image_tools

class ImageProcessor:
    def __init__(self, imageQueue, dataPipe):
        self.car_detected = False
        self.car_tracking = False
        self.roi_updated = 1 # lets us know if there was enough of a change in the roi to display
        self.car_position = [-1, -1, -1, -1]
        self.tracker = None

        self.threshold = 0
        self.frame = None

        self.image_queue = imageQueue
        self.data_pipe = dataPipe

        self.abort = 0
        self.car_information_request = 1

    # Grabs a frame for the image processor to use
    def getFrame(self):
        try:
            return self.image_queue.get()
        except:
            return None

    # Returns a 3 int array of car_detected, and car_position
    def sendCarInformation(self):
        self.data_pipe.send([self.car_detected, self.car_position[0], self.car_position[1]])

    # Constant loop that processes images as they come
    def run(self):
        while(True):
            # Check if data has been requested
            if self.data_pipe.poll():
                data_from_main = self.data_pipe.recv()
                if data_from_main is self.abort:
                    return
                elif data_from_main is self.car_information_request:
                    self.sendCarInformation()
            # do your image processing here
            if self.car_detected:
                self.runTracking()
            else:
                self.runCarDetection()

    def runTracking(self):
        # update tracker
        self.frame = self.getFrame()
        bool_updated, box = self.tracker.update(self.frame)
        # check to see if new roi was found
        if bool_updated == True:
            # car was found
            (x, y, w, h) = [int(i) for i in box] # box holds new roi coordinates
            # check to see if change in roi is greater then theshold
            delta = abs(self.car_position[0] - x) + abs(self.car_position[1] - y)
            if delta > self.threshold:
                self.roi_updated = 1
            else:
                self.roi_updated = -1
            self.car_position = [x,y,x+w,y+w]
        else:
            # car was not found
            self.carLost()

    def runCarDetection(self):
        if self.car_detected:
            self.tracker = cv2.TrackerKCF_create()
            self.tracker.init(self.getFrame(), self.car_position)
        pass

    # will reset all nessasary flags
    def carLost(self):
        self.car_position = [-1, -1, -1, -1]
        self.car_detected = False
        self.car_tracking = False
        self.roi_updated = 1
        self.tracker = None

class TrackerTesting(ImageProcessor):
    def __init__(self, folderPath='C:\\Users\\e_q\\Documents\\source_tree\\main_program\\realsense_camera\\saved_images_2019_6_13-17_48_25\\'):
        ImageProcessor.__init__(self, imageQueue=None, dataPipe=None)
        self.virtual_stream = image_tools.VirtualStream(numpyFolder=folderPath)

    def run(self):
        if self.car_detected:
            self.runTracking()
        else:
            self.runCarDetection()
        cv2.imshow("frame", self.frame)

    def getFrame(self):
        return self.virtual_stream.grabImage()

    def runCarDetection(self):
        self.frame = self.getFrame()
        roi = cv2.selectROI("Frame", self.frame, fromCenter=False, showCrosshair=True)
        self.tracker = cv2.TrackerKCF_create()
        cv2.cv2
        self.tracker = self.tracker.init(self.frame, roi)
        self.car_detected = True


if __name__ == '__main__':
    # main_pipe, process_pipe = Pipe()
    # image_queue = Queue()
    # image_processor = ImageProcessor(imageQueue=image_queue, dataPipe=process_pipe)
    # running_process = Process(target=image_processor.run, args=(None,))
    # running_process.start()

    testing = TrackerTesting()
    testing.run()
