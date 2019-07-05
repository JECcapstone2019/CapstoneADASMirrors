from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
import datetime
import time

class ImageViewingThread(QThread):
    update_image = pyqtSignal(QImage)

    def __init__(self, imageQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.image_queue = imageQueue

    def grabFrame(self):
        # TODO: fix
        try:
            return self.image_queue.get(timeout=1)
        except:
            return None

    def run(self):
        while self.isRunning:
            try:
                rgbImage = self.grabFrame()
                if rgbImage is None:
                    print("Image Issue")
                    continue
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.update_image.emit(convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio))
            except:
                pass
            print("Running...")
            time.sleep(.001)
        print("Thread exited")

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
