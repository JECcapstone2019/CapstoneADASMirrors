from multiprocessing import Queue, Pipe, Process
import cv2
from tools import image_tools

class ImageProcessor:
    def __init__(self, imageQueue, dataPipe):
        self.car_detected = False
        self.car_position = [-1, -1, -1, -1]
        self.frame_name = 'frame'

        self.frame = None

        self.image_queue = imageQueue
        self.data_pipe = dataPipe

        self.abort = 0
        self.car_information_request = 1

        self.cascade_src = 'cars.xml'
        self.car_cascade = cv2.CascadeClassifier(self.cascade_src)


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
            if getFrame() != None
                self.runCarDetection()
            # maybe add an error message in the case of undetected video stream

    def runCarDetection(self):
        pass

    # will reset all nessasary flags
    def carLost(self):
        self.car_position = [-1, -1, -1, -1]
        self.car_detected = False
        self.roi_updated = 1

class TrackerTesting(ImageProcessor):
    def __init__(self, folderPath='C:\\Users\\e_q\\Documents\\sourcetree\\main_program\\car_detection\\saved_images_2019_6_13-17_49_52\\'):
        ImageProcessor.__init__(self, imageQueue=None, dataPipe=None)
        self.virtual_stream = image_tools.VirtualStream(numpyFolder=folderPath)

    def run(self):
        while True:
                self.runCarDetection()
                self.trackingViewer()

    def getFrame(self):
        return self.virtual_stream.grabImage()

    def runCarDetection(self):
        self.frame = self.getFrame()
        
        # detecting car using haar cascade 
        gray_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        roi = self.car_cascade.detectMultiScale(gray_img, 1.1, 2.0) # this could petentially return more then 1 roi

        if len(roi)>1:
            roi = self.selectROI(roi)

        self.car_position = list(roi)
        self.car_detected = True

    def trackingViewer(self):
        # we could modify this to show mutiple roi's simultaneously by making 'roi' a class variable and just adding a for loop 
        pt1 = (self.car_position[0], self.car_position[1])
        pt2 = (self.car_position[0] + self.car_position[2], self.car_position[1] + self.car_position[3])
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
