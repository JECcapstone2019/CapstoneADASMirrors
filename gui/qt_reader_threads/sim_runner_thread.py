from PyQt5.QtCore import QThread, pyqtSlot
import time
import csv
import os
import multiprocessing

from lidar import lidar_control
from realsense_camera import camera_control

class SimulationRunnerThread(QThread):
    def __init__(self, str_simulationFolderPath, lidarReaderQueue, imageViewerQueue, carDetectionQueue=None,
                 parent=None):

        QThread.__init__(self, parent=parent)

        self.car_detection = carDetectionQueue is not(None)
        self.car_detection_camera_queue = carDetectionQueue

        self.gui_lidar_data_queue = lidarReaderQueue
        self.gui_camera_queue = imageViewerQueue

        self.simulation_folder_path = str_simulationFolderPath

        self.camera_process = None
        self.lidar_process = None

    def parseSimulationFolder(self):
        # Check if folder exists
        return self.getTimeStartDifferenceFromFolder(simulation_folder_path=self.simulation_folder_path)

    def getTimeStartDifferenceFromFolder(self, simulation_folder_path):
        # Check if both the csv files are in there
        image_csv_file_path = os.path.join(simulation_folder_path, 'image_data.csv')
        lidar_csv_file_path = os.path.join(simulation_folder_path, 'lidar_data.csv')
        sim_lidar_time_start = 0
        sim_image_time_start = 0
        if os.path.exists(image_csv_file_path) and os.path.exists(lidar_csv_file_path):
            # Get the time delay
            with open(image_csv_file_path) as csvFile:
                csv_reader = csv.reader(csvFile)
                sim_image_time_start = int(next(csv_reader)[1])
            with open(lidar_csv_file_path) as csvFile:
                csv_reader = csv.reader(csvFile)
                sim_lidar_time_start = int(next(csv_reader)[3])
        return sim_lidar_time_start, sim_image_time_start

    def runSimulation(self, lidarStartTime, imageStartTime):
        self.camera_running = True
        self.lidar_running = True

        difference = lidarStartTime - imageStartTime
        if difference > 0:
            lidar_start_add = difference
            image_start_add = 0
        else:
            image_start_add = abs(difference)
            lidar_start_add = 0
        start_time = round(time.time() * 1000) + 100

        ## startup Camera Simulation
        if self.car_detection:
            self.camera_process = camera_control.CameraMultiProcessSimulationCarDetection(
                carDetectionQueue=self.car_detection_camera_queue,
                path_simulationFolder=self.simulation_folder_path,
                i_startTime=start_time + image_start_add,
                multiProc_queue=self.gui_camera_queue)
        else:
            self.camera_process = camera_control.CameraMultiProcessSimulation(
                path_simulationFolder=self.simulation_folder_path,
                i_startTime=start_time + image_start_add,
                multiProc_queue=self.gui_camera_queue)

        ## startup Lidar Simulation
        self.lidar_process = lidar_control.LidarMultiProcessSimulation(
            path_simulationFolder=self.simulation_folder_path,
            dataQueue=self.gui_lidar_data_queue,
            i_startTime=start_time + lidar_start_add)

        self.camera_process.start()
        self.lidar_process.start()

        while self.camera_running and self.lidar_running and self.isRunning:
            time.sleep(1)
            self.camera_running = self.camera_process.is_alive()
            time.sleep(1)
            self.lidar_running = self.lidar_process.is_alive()

    def run(self):
        sim_lidar_time_start, sim_image_time_start = self.parseSimulationFolder()
        while self.isRunning:
            self.runSimulation(lidarStartTime=sim_lidar_time_start, imageStartTime=sim_image_time_start)
        try:
            self.camera_process.kill()
            self.lidar_process.kill()
        except:
            pass
        print("Simulation Thread Exited")

    def stop(self):
        self.camera_process.kill()
        self.lidar_process.kill()
        self.isRunning = False
        self.quit()
        self.wait()

    @pyqtSlot(bool)
    def onRunSimulationToggled(self, checked):
        self.isRunning = checked
