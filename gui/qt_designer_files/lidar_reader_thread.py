from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time, csv

class LidarReaderThread(QThread):
    onUpdateLidarDistance = pyqtSignal(str)
    onUpdateLidarVelocity = pyqtSignal(str)

    def __init__(self, dataQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.data_queue = dataQueue

        self.saving = False
        self.save_file = None
        self.csv_writer = None

    def run(self):
        while self.isRunning:
            try:
                data_type, data, timestamp = self.data_queue.get(timeout=1)
                if data_type is 0:
                    self.onUpdateLidarDistance.emit(data)
                elif data_type is 1:
                    self.onUpdateLidarVelocity.emit(data)
                if self.saving:
                    self.csv_writer.writerow([data_type, data, timestamp])
            except:
                pass
            time.sleep(.001)

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()

    @pyqtSlot(str)
    def startSavingSimulation(self, filePath):
        self.save_file = open(filePath, 'w')
        self.csv_writer = csv.writer(self.save_file)
        self.saving = True

    @pyqtSlot()
    def stopSavingSimulation(self):
        if self.save_file is None:
            pass
        else:
            self.csv_writer = None
            self.save_file.close()
        self.saving = False
