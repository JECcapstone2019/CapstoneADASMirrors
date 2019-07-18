from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time
import csv
import os
import queue

class CarDetectionThread(QThread):
    update_roi = pyqtSignal(tuple)

    def __init__(self, roiQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.parent_widget = parent
        self.isRunning = True
        self.roi_queue = roiQueue

    def run(self):
        while self.isRunning:
            try:
                roi = self.roi_queue.get(block=False)
                if len(roi[1]) >= 1:
                    self.update_roi.emit(roi)
            except queue.Empty:
                pass
            time.sleep(.01)
        print("Car Detection Thread exited")

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
