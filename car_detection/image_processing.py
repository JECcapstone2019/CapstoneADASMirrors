from multiprocessing import Queue, Pipe, Process

class ImageProcessor:
    def __init__(self, imageQueue, dataPipe):
        self.car_detected = False
        self.car_tracking = False
        self.car_position = (-1, -1)

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
        pass

    def runCarDetection(self):
        pass


if __name__ == '__main__':
    main_pipe, process_pipe = Pipe()
    image_queue = Queue()
    image_processor = ImageProcessor(imageQueue=image_queue, dataPipe=process_pipe)
    running_process = Process(target=image_processor.run, args=(None,))
    running_process.start()
