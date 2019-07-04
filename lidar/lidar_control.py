import time
from lidar import lidar_register_map
from tools import custom_exceptions, class_factory
from tools.register_map import BitRegisterMap
from arduino import arduino_defs as defs
from arduino import arduino_control


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

    def connect(self): # SETUP DEFAULT CONFGURATION (OVERIDE METHOD)
        return_msg = self.arduino_comms.sendCommand(defs.ID_LIDAR_SETUP, [0x00])

    def getDistance(self):
        messagereturn = self.arduino_comms.sendCommand(defs.ID_LIDAR_READ, [0x00])
        # Shift and add
        distance = (messagereturn[5] << 8) + messagereturn[6]
        return distance

    def readFromRegister(self, address, numBytes=1):
        returnMsg = self.arduino_comms.sendCommand(0x06, [0x62, address, numBytes])
        return returnMsg

    def writeToRegister(self, address, values):
        if type(values) is list:
            valueArray = [0x62, address] + values
        else:
            valueArray = [0x62, address, values]
        return self.arduino_comms.sendCommand(0x07, valueArray)


#
# FOR LATER
#
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


# Virtual Lidar interface used for testing
class LidarVirtual(LidarControl):
    def __init__(self):
        LidarControl.__init__(self)
        self.registers = BitRegisterMap(address_bits=8, data_bits=8)

    def connect(self, debug_error=False):
        if debug_error:
            return self.ERROR
        else:
            return self.NO_ERROR

    def disconnect(self, debug_error=False):
        if debug_error:
            return self.ERROR
        else:
            return self.NO_ERROR

    def writeToRegister(self, register, value, debug_error=False):
        if debug_error:
            return self.ERROR
        else:
            self._registerWriteable(register=register)
            self.registers[register] = value
            return self.NO_ERROR

    def readFromRegister(self, register, debug_error=False):
        if debug_error:
            return self.ERROR
        else:
            self._registerReadable(register=register)
            try:
                return self.registers[register]
            except KeyError:
                self.registers[register] = 0
                return self.registers[register]


LIDAR_CLASSES = {}
LIDAR_CLASSES['VLIDAR'] = LidarVirtual
LIDAR_CLASSES['ALIDAR'] = LidarArdunio
LIDAR_CLASSES['LIDAR'] = Lidar

class LidarFactory(class_factory.ClassFactory):
    def __init__(self):
        self.registerCustomClass(classesDict=LIDAR_CLASSES)



if __name__ == '__main__':
    arduino_comms = arduino_control.ArduinoControl(port='COM6')
    cTest = LidarFactory().create(customClassName='ALIDAR', arduinoControl=arduino_comms)
    cTest.connect()
    distanceRet = cTest.getDistance()
