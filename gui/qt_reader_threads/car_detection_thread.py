from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time
import csv
import os
import queue

class CarDetectionThread(QThread):
    update_roi = pyqtSignal(int, int, int, int)

    def __init__(self, roiQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.parent_widget = parent
        self.isRunning = True
        self.roi_queue = roiQueue

    def run(self):
        while self.isRunning:
            try:
                roi = self.roi_queue.get(block=False)
                self.update_roi.emit(*roi)
            except queue.Empty:
                pass
            time.sleep(.001)
        print("Car Detection Thread exited")

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

    @pyqtSlot(str)
    def startSavingSimulation(self, folderPath):
        self.save_folder = folderPath
        file_path = os.path.join(folderPath, self.SAVE_FILE_NAME)
        self.save_file = open(file_path, 'w')
        self.csv_writer = csv.writer(self.save_file)
        self.saving = True
        self.count = 0
        print("Started Saving Camera Data")

    @pyqtSlot()
    def stopSavingSimulation(self):
        if self.save_file is None:
            pass
        else:
            self.csv_writer = None
            self.save_file.close()
        self.saving = False
        print("Stopped Saving Camera Data")