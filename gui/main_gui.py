from PyQt5 import QtCore, QtGui, QtWidgets
from gui.qt_designer_files import main_gui_ui, viewer_thread
import sys

# Short overriding class for running the application
class runnerWindow(QtWidgets.QMainWindow, main_gui_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.connectObjectFunctions()
        self.image_thread = viewer_thread.ImageViewingThread(imageQueue=None, parent=self.imageViewer)
        self.image_thread.start()

    # connect all the buttons ect to their respective functions
    def connectObjectFunctions(self):
        self.enableCamera.clicked.connect(self.onEnableCamera)

    def closeApplication(self):
        pass

    def onEnableCamera(self):
        if self.enableCamera.isChecked():
            print("Camera Enabled")
        else:
            print("Camera Disabled")

def run_gui(lidar, camera, dev):
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = runnerWindow()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app

if __name__ == '__main__':
    run_gui('VLidar', 'VCamera', True)
