import smbus
import time
from lidar import lidar_register_map
from tools import custom_exceptions

LIDAR_I2C_ADDRESS = 0x62

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

    def writeToRegister(self, *args, **kwargs):
        raise NotImplementedError

    def readFromRegister(self, *args, **kwargs):
        raise NotImplementedError

    def getDistance(self, *args, **kwargs):
        raise NotImplementedError

    def getVelocity(self, *args, **kwargs):
        raise NotImplementedError


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


class VirtualLidar(LidarControl):
    def __init__(self):
        LidarControl.__init__(self)