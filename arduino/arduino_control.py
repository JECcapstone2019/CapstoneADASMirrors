import serial
from tools import custom_exceptions


# Class that controls the arduino by sending commands and getting back data via Serial connection
class ArduinoControl:

    ARDUNIO_PORT = ''
    ARDUINO_BAUD_RATE = 9600

    ERROR = -1
    NO_ERROR = 0

    HEADER_ID = 0x7F
    FOOTER_ID = 0xa5

    def __init__(self):
        self.serial_comms = None

    def connect(self):
        self.serial_comms = serial.Serial(self.ARDUNIO_PORT, self.ARDUINO_BAUD_RATE)  # Establish the connection on a specific port
        self.serial_comms.open()
        return self.serial_comms.isOpen()

    def isConnected(self):
        return self.serial_comms.isOpen()

    def sendCommand(self, command, *dataPackets):
        # Check the inputs and then send the message
        message = self._buildMessage(i_commandID=command, *dataPackets)
        self.serial_comms.write(message)
        # Wait for the ack
        ack = self.serial_comms.read(1)
        if(ack is self.NO_ERROR):
            # ack was good so now read the message
            self.serial_comms.read(1)
        else:
            pass

    def _checkIfByteSized(self, data):
        if data > 255:
            raise custom_exceptions.Bit_OverFlow
        if data < 0:
            raise custom_exceptions.Negative_Bit_value

    # Message Format [Header, commandID, Size,    Data Packets,      Footer]
    # ex.           [0x7f,    0x01,     0x05, 0xff, 0xff, 0x01, 0x01, 0xe7]
    def _buildMessage(self, i_commandID, *dataPackets):
        info_byte = len(dataPackets) + 1
        self._checkIfByteSized(i_commandID)
        self._checkIfByteSized(info_byte)
        for packet in dataPackets:
            self._checkIfByteSized(packet)
        return bytearray([self.HEADER_ID, i_commandID, info_byte, *dataPackets, self.FOOTER_ID])