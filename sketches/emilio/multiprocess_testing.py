import multiprocessing
import time

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


if __name__ == '__main__':
    p1, p2 = multiprocessing.Pipe()
    proc = testProcess(p2)
    proc.start()
    for i in range(0, 6*3):
        time.sleep(.25)
        if p1.poll():
            print(p1.recv())
    proc.kill()
