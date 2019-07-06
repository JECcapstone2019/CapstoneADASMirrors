from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time
import csv
import os
import queue

class LidarReaderThread(QThread):
    onUpdateLidarDistance = pyqtSignal(int)
    onUpdateLidarVelocity = pyqtSignal(int)

    SAVE_FILE_NAME = 'lidar_data.csv'

    def __init__(self, dataQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.data_queue = dataQueue

        self.saving = False
        self.save_file = None
        self.csv_writer = None
        self.count = 0

    def run(self):
        while self.isRunning:
            try:
                data_type, data, timestamp = self.data_queue.get(block=False)
                if data_type is 0:
                    self.onUpdateLidarDistance.emit(data)
                elif data_type is 1:
                    self.onUpdateLidarVelocity.emit(data)
                if self.saving:
                    self.csv_writer.writerow([self.count, data_type, data, timestamp])
                    self.count += 1
            except queue.Empty:
                pass
            time.sleep(.001)

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

    @pyqtSlot(str)
    def startSavingSimulation(self, folderPath):
        file_path = os.path.join(folderPath, self.SAVE_FILE_NAME)
        self.save_file = open(file_path, 'w')
        self.csv_writer = csv.writer(self.save_file)
        self.count = 0
        self.saving = True
        print("Started Saving Lidar Data")

    @pyqtSlot()
    def stopSavingSimulation(self):
        if self.save_file is None:
            pass
        else:
            self.csv_writer = None
            self.save_file.close()
        self.saving = False
        print("Stopped Saving Lidar Data")
