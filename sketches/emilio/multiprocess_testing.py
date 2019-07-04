import multiprocessing
import time
from tools import image_tools

class testProcess(multiprocessing.Process):
    def __init__(self, pipe, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self.pipe = pipe
        self.daemon = True
        self.alive = True

    def run(self):
        while self.alive:
            self.pipe.send("hello from other process")
            time.sleep(.5)

    def kill(self):
        self.alive = False


class testImageQueueProcess(multiprocessing.Process):
    def __init__(self, multiProc_queue, numpy_imageDict=None, frameRate=30, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self.queue = multiProc_queue
        if numpy_imageDict is None:
            self.image_dict = image_tools.createNumpyColorImagePatternDict(i_numImages=frameRate*5,
                                                                           tup_frameSize=(640, 480))
        else:
            self.image_dict = numpy_imageDict
        self.frame_sleep = 1.0/float(frameRate)
        self.num_images = len(self.image_dict)
        self.alive = True
        self.daemon = True


    def run(self):
        count = 0
        while self.alive:
            time.sleep(self.frame_sleep)
            self.queue.put(self.image_dict[count])
            count += 1
            if count >= self.num_images:
                count = 0
        print("Image Putter Done")

    def kill(self):
        self.alive = False


if __name__ == '__main__':
    p1, p2 = multiprocessing.Pipe()
    proc = testProcess(p2)
    proc.start()
    for i in range(0, 6*3):
        time.sleep(.25)
        if p1.poll():
            print(p1.recv())
    proc.kill()
