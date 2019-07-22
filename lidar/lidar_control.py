import time
from lidar import lidar_register_map
from tools import custom_exceptions, class_factory
from tools.register_map import BitRegisterMap
from arduino import arduino_defs as defs
from arduino import arduino_control
from multiprocessing import Process
import os
import csv


# Base control class
class LidarControl:
    # Error and no error for functions that don't return a value
    ERROR = -1
    NO_ERROR = 0

    def __init__(self, *args, **kwargs):
        # Grab all the register maps
        self._register_map = lidar_register_map.lidar_registers
        self._rw_register_map = lidar_register_map.lidar_rw_registers
        self._read_only = lidar_register_map.READ_ONLY
        self._write_only = lidar_register_map.WRITE_ONLY
        self._read_write = lidar_register_map.READ_WRITE

    def _registerReadable(self, register):
        if self._rw_register_map[register] is self._write_only:
            raise custom_exceptions.Write_Only_Register

    def _registerWriteable(self, register):
        if self._rw_register_map[register] is self._read_only:
            raise custom_exceptions.Read_Only_Register

    def _convertSignedInt(self, value):
        if value > 127:
            return (256-value) * (-1)
        else:
            return value

    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def setup(self, *args, **kwargs):
        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        raise NotImplementedError

    def writeToRegister(self, *args, **kwargs):
        raise NotImplementedError

    def readFromRegister(self, *args, **kwargs):
        raise NotImplementedError

    def getDistance(self, *args, **kwargs):
        raise NotImplementedError

    def getVelocity(self, *args, **kwargs):
        raise NotImplementedError

# Used to interface with the lidar if it is connected through a Arduino
class LidarArdunio(LidarControl):
    i2c_address = defs.LIDAR_I2C_ADDRESS

    def __init__(self, arduinoControl):
        LidarControl.__init__(self)
        self.arduino_comms = arduinoControl #Class variable
        self.last_timestamp = 0
        self.time_difference = 0

    def connect(self): # SETUP DEFAULT CONFGURATION (OVERIDE METHOD)
        self.arduino_comms.connect()

    def setup(self):
        self.arduino_comms.sendCommand(defs.ID_LIDAR_SETUP, [0x00])

    def disconnect(self):
        self.arduino_comms.disconnect()

    def getDistance(self):
        messagereturn = self.arduino_comms.sendCommand(defs.ID_LIDAR_READ, [0x00])
        # Shift and add
        distance = (messagereturn[5] << 8) + messagereturn[6]
        self._onReceivedDistanceTimestamp(message=messagereturn)

        return distance

    def getVelocity(self):
        distance = self.getDistance()
        return (distance * 0.01) / (self.time_difference)

    def _onReceivedDistanceTimestamp(self, message):
        time = 0
        time += message[7] << 24
        time += message[8] << 16
        time += message[9] << 8
        time += message[10]
        self.time_difference = (time - self.last_timestamp) * 0.001
        self.last_timestamp = time

    def readFromRegister(self, address, numBytes=1):
        returnMsg = self.arduino_comms.sendCommand(0x06, [0x62, address, numBytes])
        return returnMsg

    def writeToRegister(self, address, values):
        if type(values) is list:
            valueArray = [0x62, address] + values
        else:
            valueArray = [0x62, address, values]
        return self.arduino_comms.sendCommand(0x07, valueArray)


# Used to interface with the lidar if it is directly connected to the cpu
class Lidar(LidarControl):
    def __init__(self):
        try:
            import smbus2
        except ImportError:
            print("Uh Oh! Looks like you don't have smbus installed")
            print("please install with >pip install smbus2")

        LidarControl.__init__(self)

        self.bus = None

        self.address = 0x62
        self.distWriteReg = 0x00
        self.distWriteVal = 0x04
        self.distReadReg1 = 0x8f
        self.distReadReg2 = 0x10
        self.velWriteReg = 0x04
        self.velWriteVal = 0x08
        self.velReadReg = 0x09

    def connect(self, bus):
        try:
            self.bus = smbus2.SMBus(bus)
            time.sleep(0.5)
            return 0
        except:
            return -1

    def writeToRegister(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
        time.sleep(0.02)

    def readFromRegister(self, register):
        res = self.bus.read_byte_data(self.address, register)
        time.sleep(0.02)
        return res

    def getDistance(self):
        self.writeToRegister(self.distWriteReg, self.distWriteVal)
        dist1 = self.readFromRegister(self.distReadReg1)
        dist2 = self.readFromRegister(self.distReadReg2)
        return (dist1 << 8) + dist2

    def getVelocity(self):
        self.writeToRegister(self.distWriteReg, self.distWriteVal)
        self.writeToRegister(self.velWriteReg, self.velWriteVal)
        vel = self.readFromRegister(self.velReadReg)
        return self._convertSignedInt(vel)


LIDAR_CLASSES = {}
LIDAR_CLASSES['ALIDAR'] = LidarArdunio
LIDAR_CLASSES['LIDAR'] = Lidar

class LidarFactory(class_factory.ClassFactory):
    def __init__(self):
        self.registerCustomClass(classesDict=LIDAR_CLASSES)


class LidarMultiproccess(Process):
    CMD_DISTANCE_MEASURE = 0
    CMD_VELOCITY_MEASURE = 1
    CMD_DISTANCE_STREAM = 2
    CMD_VELOCITY_STREAM = 3
    CMD_STOP = 4
    CMD_ABORT = 5
    CMD_NONE = 6
    CMD_START = 7

    ID_DISTANCE = 0
    ID_VELOCITY = 1

    def __init__(self, dataQueue, cmdQueue, str_lidarStrID, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)

        # Communication Channels
        self.data_queue = dataQueue
        self.cmd_queue = cmdQueue

        self.lidar_type = str_lidarStrID
        self.lidar = None
        self.alive = True
        self.daemon = True

        # Streaming flags
        self.streaming_distance = False
        self.streaming_velocity = False

    def kill(self):
        self.alive = False

    def connect(self, **kwargs):
        if self.lidar_type.lower() == 'alidar':
            self.arduino_control = arduino_control.ArduinoControl()
        self.lidar = LidarFactory().create(customClassName=self.lidar_type, arduinoControl=self.arduino_control,
                                           **kwargs)
        self.lidar.connect()

    def disconnect(self):
        self.lidar.disconnect()
        self.lidar = None

    def run(self):
        # connect and wait to start
        self.connect()
        print("CONNECTED")
        while self.alive:
            try:
                cmd_id = self.cmd_queue.get(block=False)
            except:
                cmd_id = self.CMD_NONE
            if cmd_id is self.CMD_START:
                print("STARTED")
                self.lidar.setup()
                break
            time.sleep(.001)
        # Start actually taking measurements
        while self.alive:
            # Check to see if we have a new command
            try:
                cmd_id = self.cmd_queue.get(block=False)
            except:
                cmd_id = self.CMD_NONE
            if cmd_id is self.CMD_DISTANCE_STREAM:
                self.streaming_distance = not(self.streaming_distance)
            elif cmd_id is self.CMD_VELOCITY_STREAM:
                self.streaming_velocity = not(self.streaming_velocity)
            elif cmd_id is self.CMD_STOP:
                self.streaming_distance = False
                self.streaming_velocity = False
            elif cmd_id is self.CMD_ABORT:
                self.kill()
                continue

            # Do whatever the command says, or nothing
            if self.streaming_distance or (cmd_id is self.CMD_DISTANCE_MEASURE):
                self.data_queue.put((self.ID_DISTANCE, self.lidar.getDistance(), round(time.time() * 1000)))
            if self.streaming_velocity or (cmd_id is self.CMD_VELOCITY_MEASURE):
                self.data_queue.put((self.ID_VELOCITY, self.lidar.getVelocity(), round(time.time() * 1000)))
            time.sleep(.001)
        self.disconnect()
        print("Lidar Process Done")


class LidarMultiProcessSimulation(LidarMultiproccess):
    def __init__(self, path_simulationFolder, dataQueue, i_startTime, i_leewayms=2, *args, **kwargs):
        LidarMultiproccess.__init__(self, dataQueue, None, None, *args, *kwargs)
        self.sim_folder = path_simulationFolder

        self.start_time = i_startTime
        self.sleep_times = {}
        self.data_packs = {}

        self.leeway_ms = i_leewayms
        self.wait_time = (float(self.leeway_ms)/1000.0)/4.0
        self.count = 0
        self.max_count = 0
        self.last_data_sent = i_startTime
        self.parseSimulationFile()
        self.ms_conversion = 0.001

    def parseSimulationFile(self):
        file_path = os.path.join(self.sim_folder, 'lidar_data.csv')
        with open(file_path, 'r') as simFile:
            reader = csv.reader(simFile)
            last_time = 0
            for row in reader:
                if len(row) > 0:
                    if last_time == 0:
                        last_time = int(row[3])
                    self.sleep_times[int(row[0])] = int(row[3]) - last_time
                    self.data_packs[int(row[0])] = (int(row[1]), int(row[2]), int(row[3]))
                    last_time = int(row[3])
            self.max_count = len(self.data_packs)

    def run(self):
        self.count = 0
        while ((self.start_time - (time.time() * 1000)) > 2):
            time.sleep(0.001)
        while self.alive:
            self.sendData()
            self.count += 1
            if self.count >= self.max_count:
                self.count = 0
            time.sleep(self.ms_conversion * self.sleep_times[self.count])
        print("Lidar Process Done")

    def sendData(self):
        self.data_queue.put(self.data_packs[self.count])


if __name__ == '__main__':
    arduino_comms = arduino_control.ArduinoControl(port='auto')
    cTest = LidarFactory().create(customClassName='alidar', arduinoControl=arduino_comms)
    cTest.connect()
    time.sleep(2)
    cTest.setup()
    for i in range(10):
        distanceRet = cTest.getDistance()
        print(distanceRet)
