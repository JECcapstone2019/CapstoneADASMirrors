import smbus
import time
import serial
from lidar import lidar_register_map
from tools import custom_exceptions
from tools.register_map import BitRegisterMap


# Base control class
class LidarControl:
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


# Used to interface with the lidar if it is directly connected to the cpu
class Lidar(LidarControl):
    def __init__(self):
        LidarControl.__init__(self)

        self.bus = None
        self.address = LIDAR_I2C_ADDRESS

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
            self.bus = smbus.SMBus(bus)
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


# Used to interface with the lidar if it is connected through a Arduino
class LidarArdunio(LidarControl):
    def __init__(self, arduinoControl):
        LidarControl.__init__(self)



# Virtual Lidar interface used for testing
class LidarVirtual(LidarControl):
    def __init__(self):
        LidarControl.__init__(self)
        self.registers = BitRegisterMap(address_bits=8, data_bits=8)

    def connect(self, debug_error=False):
        if debug_error:
            return ERROR
        else:
            return NO_ERROR

    def disconnect(self, debug_error=False):
        if debug_error:
            return ERROR
        else:
            return NO_ERROR

    def writeToRegister(self, register, value, debug_error=False):
        if debug_error:
            return ERROR
        else:
            self._registerWriteable(register=register)
            self.registers[register] = value
            return NO_ERROR

    def readFromRegister(self, register, debug_error=False):
        if debug_error:
            return ERROR
        else:
            self._registerReadable(register=register)
            try:
                return self.registers[register]
            except KeyError:
                self.registers[register] = 0
                return self.registers[register]
