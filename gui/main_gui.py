import multiprocessing
import os
import sys
import time
from tools import time_stamping
import csv
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor, QFont

from gui.qt_designer_files import main_gui_ui
from gui.qt_reader_threads import lidar_reader_thread, viewer_thread, car_detection_thread, sim_runner_thread

from lidar import lidar_control
from realsense_camera import camera_control
from car_detection import image_processing


class runnerWindow(QtWidgets.QMainWindow, main_gui_ui.Ui_MainWindow):

    # Thread Signals
    startSavingSimulation = pyqtSignal(str)
    stopSavingSimulation = pyqtSignal()
    runSimulationToggled = pyqtSignal(bool)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        # Define widget groups for hiding and disabling ################################################################
        self.sim_widgets = [self.simulationRunSimulation, self.simulationSelectFolder, self.simulationTitle,
                            self.simulationStartSavingNew, self.simulationFolderSelectedTextEdit]

        self.lidar_widgets = [self.lidarEnableCheckBox, self.lidarSelection, self.lidarTitle, self.lidarSetupButton,
                              self.lidarGetDistanceButton, self.lidarGetVelocityButton, self.lidarStreamDistance,
                              self.lidarStreamVelocity]

        self.camera_widgets = [self.cameraEnableCheckBox, self.cameraSelection, self.cameraTitle]

        self.car_detection_widgets = [self.carDetectionSelection, self.carDetectionTitle,
                                      self.carDetectionEnableCheckBox]

        self.line_widgets = [self.line, self.line_2, self.line_3, self.line_4, self.line_5, self.line_6, self.line_7,
                             self.line_8, self.line_9, self.line_10, self.line_11, self.line_12, self.line_13]

        self.option_widgets = [self.sim_widgets, self.lidar_widgets, self.camera_widgets, self.car_detection_widgets,
                               self.line_widgets]

        ################################################################################################################

        self.lidar_reader = None
        self.gui_lidar_data_queue = None
        self.gui_lidar_cmd_queue = None
        self.lidar_process = None

        self.image_viewer = None
        self.gui_camera_queue = None
        self.camera_process = None

        self.car_detection_roi_thread = None
        self.car_detection_process = None
        self.car_detection_camera_queue = None
        self.car_detection_roi_queue = None
        self.car_detected = False
        self.car_detection_roi = []
        self.car_detection_color = QColor(0, 0, 255)

        self.simulation_folder_path = ''
        self.sim_image_time_start = 0
        self.sim_lidar_time_start = 0
        self.simulation_runner_thread = None

        self.lidar_distance = 0
        self.lidar_velocity = 0

        self.last_non_zero_lidar_distance = 0
        self.last_non_zero_lidar_velocity = 0

        ## ROI calc and filtering
        self.expected_width_min = 0
        self.expected_width_max = 0

        ##
        self.expected_center_min = 0
        self.expected_center_max = 300

        self.calc_a_width = 0.00008
        self.calc_b_width = -0.1422
        self.calc_c_width = 225.83

        self.calc_m_width_center = 0.0162
        self.calc_b_width_center = 233.216
        self.expected_center = 0

        self.pixel_leeway = 60

        self.warning_8_m = 800 # 8m warning in cm

        ## Conversion
        self.m_p_s_to_k_p_h = 3.6 # 1m/s = 3.6km/h
        self.warning_30km_p_h = 8.3333 # 30km/h in m/s
        self.warning_msg = False

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
        self.simulationRunSimulation.toggled.connect(self.onSimulationRunToggled)

        ## Menu Bar Functions ##
        self.actionHide_Options.triggered.connect(self.onHideRunOptions)
        self.actionShow_Options.triggered.connect(self.onShowRunOptions)

    def closeApplication(self):
        pass

    def enableWidgetArray(self, arr_widgets, enable=True):
        for widget in arr_widgets:
            widget.setEnabled(enable)

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
    def onUpdateLidarDistance(self, i_distance):
        self.lidar_distance = i_distance
        self.distance_warning = i_distance / float(4000)
        self.updateExpectedROI()
        self.updateROIColor()
        if i_distance > 0:
            self.last_non_zero_lidar_distance = time.time()

    @pyqtSlot(float)
    def onUpdateLidarVelocity(self, f_velocity):
        self.lidar_velocity = f_velocity
        self.updateROIColor()
        if f_velocity != 0:
            self.last_non_zero_lidar_distance = time.time()

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
        self.makeSimulationStartAvailable()

    def onLidarGetDistance(self):
        self.gui_lidar_cmd_queue.put(0)

    def onLidarGetVelocity(self):
        self.gui_lidar_cmd_queue.put(1)

    def onLidarStreamDistanceToggle(self, checked):
        self.gui_lidar_cmd_queue.put(2)

    def onLidarStreamVelocityToggle(self, checked):
        self.gui_lidar_cmd_queue.put(3)

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
    @pyqtSlot(QImage, int, int)
    def onRepaintImage(self, image, h, w):
        pixmap = QPixmap.fromImage(image)
        pixmap = self.paintImage(pixmap=pixmap)
        image.scaled(h, w, Qt.KeepAspectRatio)
        self.imageViewer.setPixmap(pixmap)

    def paintImage(self, pixmap):
        painter = QPainter(pixmap)
        pen = QPen(self.car_detection_color) # TODO: Fix coloring
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setFont(QFont('Decorative', 10))
        if self.warning_msg:
            painter.drawText(0, 20, "Distance: %i.%im, Velocity:%f" % (self.lidar_distance/100, self.lidar_distance % 100,
                                                                   self.lidar_velocity))
            painter.drawText(0, 60, "WARNING!")
        if self.car_detected:
            for square in range(len(self.ROIs)):
                roi = self.ROIs[square]
                painter.drawRect(roi[0], roi[1], roi[2], roi[3])
                painter.drawText(roi[0], roi[1], "ROI:%i" % square)
        del pen
        del painter
        return pixmap

    ## Camera Functions ################################################################################################
    def onCameraEnabled(self, checked):
        if checked:
            self.carDetectionEnableCheckBox.setEnabled(False)
            self.gui_camera_queue = multiprocessing.Queue()
            self.startImageViewer(imageQueue=self.gui_camera_queue)
            if self.carDetectionEnableCheckBox.isChecked():
                self.camera_process = camera_control.CameraMultiProcess_CarDetection(carDetectionQueue=self.car_detection_camera_queue,
                                                                                     multiProc_queue=self.gui_camera_queue)
            else:
                self.camera_process = camera_control.CameraMultiProcess(multiProc_queue=self.gui_camera_queue)
            self.camera_process.start()
            print("Camera Enabled")
        else:
            self.carDetectionEnableCheckBox.setEnabled(True)
            self.camera_process.kill()
            self.stopImageViewer()
            print("Camera Disabled")
        self.makeSimulationStartAvailable()

    ## Car Detection Functions #########################################################################################
    def onCarDetectionEnabled(self, checked):
        if checked:
            self.startCarDetection()
            print("Car Detection Enabled")

        else:
            self.stopCarDetection()
            print("Car Detection Disabled")

    def startCarDetection(self):
        self.car_detection_roi_queue = multiprocessing.Queue()
        self.car_detection_camera_queue = multiprocessing.Queue()
        self.car_detection_roi_thread = car_detection_thread.CarDetectionThread(roiQueue=self.car_detection_roi_queue)
        self.car_detection_roi_thread.update_roi.connect(self.onROIUpdated)
        self.car_detection_process = image_processing.ImageProcessor(imageQueue=self.car_detection_camera_queue,
                                                                     roiQueue=self.car_detection_roi_queue)
        self.car_detection_roi_thread.start()
        self.car_detection_process.start()

    def stopCarDetection(self):
        self.car_detection_roi_thread.stop()
        self.car_detection_process.kill()

    @pyqtSlot(tuple)
    def onROIUpdated(self, roiData):
        self.ROIs = roiData[1]
        self.ROI_timestamp = roiData[0]
        self.checkROIsIntegration()
        # self.checkROIsIntegration()
        if len(self.ROIs) > 0:
            self.car_detected = True
        else:
            self.car_detected = False

    ## Simulation Functions ############################################################################################
    def onSelectSimulationFolder(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(dialog.Directory)
        self.simulation_folder_path = dialog.getExistingDirectory(options=QtWidgets.QFileDialog.DontUseNativeDialog)
        # Check if folder exists
        multiple_simulations = False
        image_csv_file_path = ''
        lidar_csv_file_path = ''
        if os.path.exists(self.simulation_folder_path):
            for file in os.listdir(self.simulation_folder_path):
                if file == 'sim_runner.txt':
                    multiple_simulations = True
                elif file == 'image_data.csv':
                    image_csv_file_path = os.path.join(self.simulation_folder_path, file)
                elif file == 'lidar_data.csv':
                    lidar_csv_file_path = os.path.join(self.simulation_folder_path, file)
        if not(multiple_simulations) and ((image_csv_file_path == '') and (lidar_csv_file_path == '')):
            self.simulation_folder_path = ''
        else:
            self.simulationSelectFolder.setText(self.simulation_folder_path)
        self.makeSimulationStartAvailable()

    def onSimulationCheckboxToggled(self, checked):
        if checked:
            folder_path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='Simulation')
            self.startSavingSimulation.emit(folder_path)
        else:
            self.stopSavingSimulation.emit()
        self.makeSimulationStartAvailable()

    def onSimulationRunToggled(self, checked):
        if checked:
            self.gui_lidar_data_queue = multiprocessing.Queue()
            self.gui_camera_queue = multiprocessing.Queue()

            self.startLidarReader(dataQueue=self.gui_lidar_data_queue)
            self.startImageViewer(imageQueue=self.gui_camera_queue)

            self.simulation_runner_thread = sim_runner_thread.SimulationRunnerThread(str_simulationFolderPath=self.simulation_folder_path,
                                                                                     lidarReaderQueue=self.gui_lidar_data_queue,
                                                                                     imageViewerQueue=self.gui_camera_queue,
                                                                                     carDetectionQueue=self.car_detection_camera_queue)
            self.simulationRunSimulation.toggled.connect(self.simulation_runner_thread.onRunSimulationToggled)
            self.simulation_runner_thread.start()
        else:
            # Stop Camera
            self.stopImageViewer()

            # Stop Lidar
            self.stopLidarReader()

        self.enableWidgtsOnSimulation(enable=not(checked))
        self.runSimulationToggled.emit(checked)

    # Used to check if we are able to startup a simulation viewing
    def makeSimulationStartAvailable(self):
        if self.cameraEnableCheckBox.isChecked() or self.lidarEnableCheckBox.isChecked() or \
                self.simulationStartSavingNew.isChecked() or (self.simulation_folder_path == ''):
            enable_sim_start = False
        else:
            enable_sim_start = True
        self.simulationRunSimulation.setEnabled(enable_sim_start)

    def enableWidgtsOnSimulation(self, enable):
        self.enableWidgetArray(arr_widgets=self.lidar_widgets, enable=enable)
        self.enableWidgetArray(arr_widgets=self.camera_widgets, enable=enable)

    ## Sensor Integration ##############################################################################################
    def updateExpectedROI(self):
        expected_width = (self.calc_a_width * self.lidar_distance*self.lidar_distance) + \
                         (self.calc_b_width * self.lidar_distance) + self.calc_c_width
        self.expected_width_min = expected_width - self.pixel_leeway
        self.expected_width_max = expected_width + self.pixel_leeway
        self.expected_center = (self.calc_m_width_center * self.lidar_distance) + self.calc_b_width_center

    def checkROIsIntegration(self):
        # Check if the lidar was updated at a good time
        check_lidar = (self.last_non_zero_lidar_distance - time.time()) < 0.4
        removes = []
        for roi in range(len(self.ROIs)):
            x, y, w, h = self.ROIs[roi]
            roi_center = x + (w / 2)
            # Check for ROI's that are on the own car door
            if self.expected_center_min > roi_center or roi_center > self.expected_center_max:
                removes.append(roi)
            elif check_lidar:
                # Check for ROI's that are too big or small
                if (self.expected_width_min > w) or (w > self.expected_width_max):
                    removes.append(roi)
                elif (self.expected_center - roi_center) > self.pixel_leeway:
                    removes.append(roi)
        self.ROIs = np.delete(self.ROIs, removes, axis=0)

    def updateROIColor(self):
        # Check if the lidar distance/velocity measurements are worth looking at
        if abs(self.lidar_velocity) < 1:
            self.lidar_velocity = 0
        if self.lidar_distance < 50:
            self.lidar_distance = 0
        if self.lidar_velocity < -self.warning_30km_p_h:
            self.warning_msg = True
        if self.lidar_distance < self.warning_8_m:
            self.warning_msg = True
        colors = (0, 0, 255)
        distance_updated_right = ((self.last_non_zero_lidar_distance - time.time()) < 0.4)
        velocity_updated_right = ((self.last_non_zero_lidar_velocity - time.time()) < 0.4)
        # No lidar data, make the square green
        if self.lidar_distance == self.lidar_velocity == 0:
            self.warning_msg = False
        # No lidar distance, only velocity useful
        elif (self.lidar_distance == 0) and distance_updated_right:
            if self.lidar_velocity > 0:
                # Car moving away, don't care
                colors = (0, 255, 0)
            else:
                ratio = min(abs(self.lidar_velocity / self.warning_30km_p_h), 1)
                colors = (round(ratio * 255), round((1 - ratio) * 255), 0)
        # no lidar velocity, only distance useful
        elif (self.lidar_velocity == 0) and velocity_updated_right:
            ratio = min(abs(((self.lidar_distance * 0.01) / 25.0)), 1)
            colors = (round((1 - ratio) * 255), round(ratio * 255), 0)
        # Use both lidar measurements
        elif distance_updated_right and velocity_updated_right:
            if self.lidar_velocity > 0:
                # Car moving away, don't care
                colors = (0, 255, 0)
            else:
                ratio_distance = min(abs(((self.lidar_distance * 0.01) / 40.0)), 1)
                ratio_velocity = min(abs(self.lidar_velocity / self.warning_30km_p_h), 1)
                ratio = (0.25 * (1 - ratio_velocity)) + (0.75 * ratio_distance)
                colors = (round((1 - ratio) * 255), round(ratio * 255), 0)
        else:
            self.warning_msg = False

        self.car_detection_color = QColor(*colors)


def run_gui(lidar, camera, dev):
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = runnerWindow() # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':
    run_gui('VLidar', 'VCamera', True)
