from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage
import time
import csv
import os
import numpy as np

class ImageViewingThread(QThread):
    update_image = pyqtSignal(QImage)

    SAVE_FILE_NAME = 'image_data.csv'

    def __init__(self, imageQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.parent_widget = parent
        self.isRunning = True
        self.image_queue = imageQueue

        self.save_folder = ''
        self.saving = False
        self.save_file = None
        self.csv_writer = None
        self.count = 0

    def grabFrame(self):
        # TODO: fix
        try:
            return self.image_queue.get(block=False)
        except:
            return (None, None)

    def run(self):
        while self.isRunning:
            try:
                rgbImage, image_timestamp = self.grabFrame()
                if rgbImage is None:
                    continue
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                # parent_size = self.parent_widget.size()
                # self.update_image.emit(convertToQtFormat.scaled(parent_size.height(), parent_size.width(),
                #                                                 Qt.KeepAspectRatio))
                self.update_image.emit(convertToQtFormat.scaled(h, w, Qt.KeepAspectRatio))
                if self.save_file:
                    np.save(os.path.join(self.save_folder, 'image_%i.npy' % self.count), rgbImage)
                    self.csv_writer.writerow([self.count, image_timestamp])
                    self.count += 1
            except:
                pass
            time.sleep(.001)
        print("Image Thread exited")

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
