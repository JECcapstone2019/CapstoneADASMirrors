from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
import datetime

class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeLabel = pyqtSignal(str)

    def __init__(self, imageQueue, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.image_queue = imageQueue

    def grabFrame(self):
        # TODO: fix
        try:
            self.image_queue.get()
        except:
            pass

    def run(self):
        while self.isRunning:
            frame = self.grabFrame()
            #color_frame = frames.get_color_frame()
            #rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgbImage = frame
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            now = datetime.datetime.now()
            sec = now.second
            self.changeLabel.emit(str(sec))

    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()