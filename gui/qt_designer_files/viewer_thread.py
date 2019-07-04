from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
import datetime
import time

class ImageViewingThread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeLabel = pyqtSignal(str)

    def __init__(self, imageQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.image_queue = imageQueue

    def grabFrame(self):
        # TODO: fix
        try:
            self.image_queue.get(timeout=1)
        except:
            print("Image Issue")
            return None

    def run(self):
        while self.isRunning:
            try:
                rgbImage = self.grabFrame()
                if rgbImage is None:
                    print("Running...")
                    continue
                #color_frame = frames.get_color_frame()
                #rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                now = datetime.datetime.now()
                sec = now.second
                self.changeLabel.emit(str(sec))
            except:
                pass
            print("Running...")
            time.sleep(.001)
        print("Thread exited")

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
