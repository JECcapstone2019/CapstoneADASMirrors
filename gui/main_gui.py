from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from gui.qt_designer_files import main_gui_ui, viewer_thread
import sys, os
from sketches.emilio import multiprocess_testing
from multiprocessing import Queue

from tools import image_tools
import numpy as np

# Short overriding class for running the application
class runnerWindow(QtWidgets.QMainWindow, main_gui_ui.Ui_MainWindow):
    def __init__(self, imageQueue):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.image_thread = viewer_thread.ImageViewingThread(imageQueue=imageQueue, parent=self.imageViewer)
        self.connectObjectFunctions()
        self.image_thread.start()

    # connect all the buttons ect to their respective functions
    def connectObjectFunctions(self):
        self.enableCamera.clicked.connect(self.onEnableCamera)
        self.image_thread.update_image.connect(self.onRepaintImage)

    def closeApplication(self):
        pass

    @pyqtSlot(QImage)
    def onRepaintImage(self, image):
        self.imageViewer.setPixmap(QPixmap.fromImage(image))

    def onEnableCamera(self):
        if self.enableCamera.isChecked():
            print("Camera Enabled")
        else:
            print("Camera Disabled")


def run_gui(lidar, camera, dev):
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    shared_image_queue = Queue()

    # Grab the images from the folder
    folder_path = os.path.join(os.getcwd(), 'saved_images_testing')
    image_dict = image_tools.VirtualStream(numpyFolder=folder_path).np_images
    for image, path in image_dict.items():
        image_dict[image] = np.load(path)

    # startup the sender
    image_sender = multiprocess_testing.testImageQueueProcess(multiProc_queue=shared_image_queue,
                                                              numpy_imageDict=image_dict)
    image_sender.start()
    form = runnerWindow(imageQueue=shared_image_queue) # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app
    image_sender.kill()


if __name__ == '__main__':
    run_gui('VLidar', 'VCamera', True)
