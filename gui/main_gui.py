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
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        # Define widget groups for hiding and disabling ################################################################
        self.sim_widgets = [self.simulationRunSimulation, self.simulationFolderSelectedTextEdit,
                            self.simulationSelectFolder, self.simulationTextEdit, self.simulationTitle]

        self.lidar_widgets = [self.lidarEnableCheckBox, self.lidarCheckProcessButton, self.lidarSelection,
                              self.lidarTextEdit, self.lidarTitle]

        self.camera_widgets = [self.cameraEnableCheckBox, self.cameraCheckProcessButton, self.cameraTextEdit,
                               self.cameraSelection, self.cameraTitle]

        self.image_viewer_widgets = [self.imageViewerTitle, self.imageViewerLabel, self.imageViewerTextEdit]

        self.car_detection_widgets = [self.carDetectionSelection, self.carDetectionTitle, self.carDetectionTextEdit,
                                      self.carDetectionCheckProcessButton_2, self.carDetectionEnableCheckBox]

        self.line_widgets = [self.line, self.line_2, self.line_3, self.line_4, self.line_5, self.line_6, self.line_7,
                             self.line_8, self.line_9, self.line_10, self.line_11]

        self.option_widgets = [self.sim_widgets, self.lidar_widgets, self.camera_widgets, self.image_viewer_widgets,
                               self.car_detection_widgets, self.line_widgets]

        ################################################################################################################

        self.image_viewer = None
        self.simulation_folder_path = ''

        self.connectObjectFunctions()

    # connect all the buttons ect to their respective functions
    def connectObjectFunctions(self):

        ## Lidar Functions ##
        self.lidarEnableCheckBox.clicked.connect(self.onLidarEnable)

        ## Camera Functions ##
        self.cameraEnableCheckBox.clicked.connect(self.onCameraEnabled)

        ## Car Detection Functions ##
        self.carDetectionEnableCheckBox.clicked.connect(self.onCarDetectionEnabled)

        ## Simulation Functions ##
        self.simulationSelectFolder.pressed.connect(self.onSelectSimulationFolder)

        ## Menu Bar Functions ##
        self.actionHide_Options.triggered.connect(self.onHideRunOptions)
        self.actionShow_Options.triggered.connect(self.onShowRunOptions)

    def closeApplication(self):
        pass

    def hideWidgetArray(self, arr_widgets, show=False):
        for widget in arr_widgets:
            widget.setVisible(show)

    def onHideRunOptions(self):
        print("Hiding Options")
        for widget_arr in self.option_widgets:
            self.hideWidgetArray(arr_widgets=widget_arr, show=False)

    def onShowRunOptions(self):
        print("Showing Options")
        for widget_arr in self.option_widgets:
            self.hideWidgetArray(arr_widgets=widget_arr, show=True)

    ## Image Viewer Functions ##########################################################################################
    def startImageViewer(self, imageQueue):
        if self.image_viewer is None:
            try:
                self.image_viewer = viewer_thread.ImageViewingThread(imageQueue=imageQueue, parent=self.imageViewer)
                self.image_viewer.update_image.connect(self.onRepaintImage)
                self.image_viewer.start()
                return 0
            except:
                return -2
        else:
            self.stopImageViewer()
            return -1

    def stopImageViewer(self):
        pass

    # Slot for the image thread to update the main image window
    @pyqtSlot(QImage)
    def onRepaintImage(self, image):
        self.imageViewer.setPixmap(QPixmap.fromImage(image))


    ## Lidar Functions #################################################################################################
    def onLidarEnable(self, checked):
        if checked:
            print("Lidar Enabled")
        else:
            print("Lidar Disabled")


    ## Camera Functions ################################################################################################
    def onCameraEnabled(self, checked):
        if checked:
            print("Camera Enabled")
        else:
            print("Camera Disabled")


    ## Car Detection Functions #########################################################################################
    def onCarDetectionEnabled(self, checked):
        if checked:
            print("Car Detection Enabled")
        else:
            print("Car Detection Disabled")


    ## Simulation Functions ############################################################################################
    def onSelectSimulationFolder(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(dialog.Directory)
        self.simulation_folder_path = dialog.getExistingDirectory(options=QtWidgets.QFileDialog.DontUseNativeDialog)
        # Check folder #
        # TODO: Load Simulation
        self.simulationFolderSelectedTextEdit.setText(self.simulation_folder_path)


def run_gui(lidar, camera, dev):
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    # shared_image_queue = Queue()
    #
    # # Grab the images from the folder
    # folder_path = os.path.join(os.getcwd(), 'saved_images_testing')
    # image_dict = image_tools.VirtualStream(numpyFolder=folder_path).np_images
    # for image, path in image_dict.items():
    #     image_dict[image] = np.load(path)
    #
    # # startup the sender
    # image_sender = multiprocess_testing.testImageQueueProcess(multiProc_queue=shared_image_queue,
    #                                                           numpy_imageDict=image_dict)
    # image_sender = multiprocess_testing.TestCameraProcess(multiProc_queue=shared_image_queue)
    #
    # image_sender.start()

    form = runnerWindow() # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app
    # image_sender.kill()


if __name__ == '__main__':
    run_gui('VLidar', 'VCamera', True)
