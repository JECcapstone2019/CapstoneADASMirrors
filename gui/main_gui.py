from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from gui.qt_designer_files import main_gui_ui, viewer_thread, lidar_reader_thread
import sys
import multiprocessing
from tools import time_stamping

from sketches.emilio import multiprocess_testing

# Short overriding class for running the application
class runnerWindow(QtWidgets.QMainWindow, main_gui_ui.Ui_MainWindow):
    startSavingSimulation = pyqtSignal(str)
    stopSavingSimulation = pyqtSignal()

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

        self.lidar_viewer = None
        self.gui_lidar_queue = None
        self.lidar_process = None

        self.image_viewer = None
        self.gui_camera_queue = None
        self.camera_process = None

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
        self.simulationStartSavingNew.toggled.connect(self.onSimulationCheckboxToggled)

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
        self.image_viewer = viewer_thread.ImageViewingThread(imageQueue=imageQueue, parent=self.imageViewer)
        self.image_viewer.update_image.connect(self.onRepaintImage)
        self.image_viewer.start()

    def stopImageViewer(self):
        self.image_viewer.stop()

    # Slot for the image thread to update the main image window
    @pyqtSlot(QImage)
    def onRepaintImage(self, image):
        self.imageViewer.setPixmap(QPixmap.fromImage(image))

    ## Lidar Reader Functions ##########################################################################################
    def startLidarREader(self, dataQueue):
        self.lidar_viewer = lidar_reader_thread.LidarReaderThread(dataQueue=dataQueue)
        self.lidar_viewer.onUpdateLidarDistance.connect(self.onUpdateLidarDistance)
        self.lidar_viewer.onUpdateLidarVelocity.connect(self.onUpdateLidarVelocity)
        self.lidar_viewer.startSavingSimulation.connect(self.startSavingSimulation)
        self.lidar_viewer.stopSavingSimulation.connect(self.stopSavingSimulation)
        self.lidar_viewer.start()

    def stopLidarReader(self):
        self.lidar_viewer.stop()

    @pyqtSlot(str)
    def onUpdateLidarDistance(self, str_distance):
        print("Lidar Distance: %s" % str_distance)

    @pyqtSlot(str)
    def onUpdateLidarVelocity(self, str_velocity):
        print("Lidar Distance: %s" % str_velocity)

    ## Lidar Functions #################################################################################################
    def onLidarEnable(self, checked):
        if checked:
            print("Lidar Enabled")
        else:
            print("Lidar Disabled")


    ## Camera Functions ################################################################################################
    def onCameraEnabled(self, checked):
        if checked:
            self.gui_camera_queue = multiprocessing.Queue()
            self.startImageViewer(imageQueue=self.gui_camera_queue)
            self.camera_process = multiprocess_testing.TestCameraProcess(multiProc_queue=self.gui_camera_queue)
            self.camera_process.start()
            print("Camera Enabled")
        else:
            self.camera_process.kill()
            self.stopImageViewer()
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
        self.simulationFolderSelectedTextEdit.setText(self.simulation_folder_path)

    def onSimulationCheckboxToggled(self, checked):
        if checked:
            folder_path = time_stamping.createTimeStampedFolder(str_Prefix='Simulation')
            self.startSavingSimulation.emit(folder_path)
        else:
            self.stopSavingSimulation.emit()


def run_gui(lidar, camera, dev):
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = runnerWindow() # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':
    run_gui('VLidar', 'VCamera', True)
