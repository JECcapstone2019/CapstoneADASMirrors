from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from gui.qt_designer_files import main_gui_ui, viewer_thread, lidar_reader_thread
import sys
import os
import time
import multiprocessing
from tools import time_stamping
from lidar import lidar_control
from realsense_camera import camera_control


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
                            self.simulationSelectFolder, self.simulationTextEdit, self.simulationTitle,
                            self.simulationStartSavingNew]

        self.lidar_widgets = [self.lidarEnableCheckBox, self.lidarCheckProcessButton, self.lidarSelection,
                              self.lidarTextEdit, self.lidarTitle, self.lidarGetDistanceButton,
                              self.lidarGetVelocityButton, self.lidarStreamDistance, self.lidarStreamVelocity]

        self.lidar_reader_widgets = [self.lidarReaderTitle, self.lidarReaderLabel, self.lidarReaderTextEdit]

        self.camera_widgets = [self.cameraEnableCheckBox, self.cameraCheckProcessButton, self.cameraTextEdit,
                               self.cameraSelection, self.cameraTitle]

        self.image_viewer_widgets = [self.imageViewerTitle, self.imageViewerLabel, self.imageViewerTextEdit]

        self.car_detection_widgets = [self.carDetectionSelection, self.carDetectionTitle, self.carDetectionTextEdit,
                                      self.carDetectionCheckProcessButton_2, self.carDetectionEnableCheckBox]

        self.line_widgets = [self.line, self.line_2, self.line_3, self.line_4, self.line_5, self.line_6, self.line_7,
                             self.line_8, self.line_9, self.line_10, self.line_11, self.line_12, self.line_13]

        self.option_widgets = [self.sim_widgets, self.lidar_widgets, self.lidar_reader_widgets, self.camera_widgets,
                               self.image_viewer_widgets, self.car_detection_widgets, self.line_widgets]

        ################################################################################################################

        self.lidar_reader = None
        self.gui_lidar_data_queue = None
        self.gui_lidar_cmd_queue = None
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
        self.lidarGetDistanceButton.pressed.connect(self.onLidarGetDistance)
        self.lidarGetVelocityButton.pressed.connect(self.onLidarGetVelocity)
        self.lidarStreamDistance.toggled.connect(self.onLidarStreamDistanceToggle)
        self.lidarStreamVelocity.toggled.connect(self.onLidarStreamVelocityToggle)

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
        self.startSavingSimulation.connect(self.image_viewer.startSavingSimulation)
        self.stopSavingSimulation.connect(self.image_viewer.stopSavingSimulation)
        self.image_viewer.start()

    def stopImageViewer(self):
        self.image_viewer.stop()

    # Slot for the image thread to update the main image window
    @pyqtSlot(QImage)
    def onRepaintImage(self, image):
        self.imageViewer.setPixmap(QPixmap.fromImage(image))

    ## Lidar Reader Functions ##########################################################################################
    def startLidarReader(self, dataQueue):
        self.lidar_reader = lidar_reader_thread.LidarReaderThread(dataQueue=dataQueue)
        self.lidar_reader.onUpdateLidarDistance.connect(self.onUpdateLidarDistance)
        self.lidar_reader.onUpdateLidarVelocity.connect(self.onUpdateLidarVelocity)
        self.startSavingSimulation.connect(self.lidar_reader.startSavingSimulation)
        self.stopSavingSimulation.connect(self.lidar_reader.stopSavingSimulation)
        self.lidar_reader.start()

    def stopLidarReader(self):
        self.lidar_reader.stop()

    @pyqtSlot(int)
    def onUpdateLidarDistance(self, str_distance):
        print("Lidar Distance: %s" % str_distance)

    @pyqtSlot(int)
    def onUpdateLidarVelocity(self, str_velocity):
        print("Lidar Distance: %s" % str_velocity)

    ## Lidar Functions #################################################################################################
    def onLidarEnable(self, checked):
        if checked:
            self.gui_lidar_cmd_queue = multiprocessing.Queue()
            self.gui_lidar_data_queue = multiprocessing.Queue()
            self.startLidarReader(dataQueue=self.gui_lidar_data_queue)
            self.lidar_process = lidar_control.LidarMultiproccess(dataQueue=self.gui_lidar_data_queue,
                                                                  cmdQueue=self.gui_lidar_cmd_queue,
                                                                  str_lidarStrID='alidar') # TODO: Make this selectable
            self.lidar_process.start()
            time.sleep(4)
            self.gui_lidar_cmd_queue.put(7)
            print("Lidar Enabled")
        else:
            self.lidar_process.kill()
            self.stopLidarReader()
            print("Lidar Disabled")

    def onLidarGetDistance(self):
        self.gui_lidar_cmd_queue.put(0)

    def onLidarGetVelocity(self):
        self.gui_lidar_cmd_queue.put(1)

    def onLidarStreamDistanceToggle(self, checked):
        self.gui_lidar_cmd_queue.put(2)

    def onLidarStreamVelocityToggle(self, checked):
        self.gui_lidar_cmd_queue.put(3)

    ## Camera Functions ################################################################################################
    def onCameraEnabled(self, checked):
        if checked:
            self.gui_camera_queue = multiprocessing.Queue()
            self.startImageViewer(imageQueue=self.gui_camera_queue)
            self.camera_process = camera_control.CameraMultiProcess(multiProc_queue=self.gui_camera_queue)
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
            folder_path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='Simulation')
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
