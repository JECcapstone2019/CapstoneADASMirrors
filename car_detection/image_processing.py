from multiprocessing import Queue, Pipe, Process
import

class ImageProcessor:
    def __init__(self, imageQueue, dataPipe):
        self.car_detected = False
        self.car_tracking = False
        self.roi_updated = 1 # lets us know if there was enough of a change in the roi to display
        self.car_position [-1, -1, -1, -1]
        self.tracker = None

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
        threshold = 0 # chnage after we experiment a bit
        # update tracker
        bool_updated, box = tracker.update(frame)
        # check to see if new roi was found
        if bool_updated == True:
            # car was found
            (x, y, w, h) = [int(i) for i in box] # box holds new roi coordinates
            # check to see if change in roi is greater then theshold
            delta = abs(car_position[0] - x) + abs(car_position[1] - y)
            if delta > threshold:
                self.roi_updated = 1
            else:
                self.roi_updated = -1
            self.car_position = [x,y,x+w,y+w]
        else:
            # car was not found
            carLost()



    def runCarDetection(self):
        if self.car_detected:
            self.tracker = cv2.TrackerKCF_create()
            self.tracker.init(getFrame(), car_position)
        pass

    # will reset all nessasary flags
    def carLost(self):
        self.car_position = [-1, -1, -1, -1]
        self.car_detected = False
        self.car_tracking = False
        self.roi_updated = 1
        self.tracker = None




if __name__ == '__main__':
    main_pipe, process_pipe = Pipe()
    image_queue = Queue()
    image_processor = ImageProcessor(imageQueue=image_queue, dataPipe=process_pipe)
    running_process = Process(target=image_processor.run, args=(None,))
    running_process.start()
