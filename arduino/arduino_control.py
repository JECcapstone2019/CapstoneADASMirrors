import serial
from tools import custom_exceptions
import time
from arduino import arduino_defs as defs


# Class that controls the arduino by sending commands and getting back data via Serial connection
class ArduinoControl:
    def __init__(self, port=defs.ARDUNIO_PORT, baudRate=defs.ARDUINO_BAUD_RATE):
        self.serial_comms = None
        self.port = port
        self.baud_rate = baudRate

    def connect(self):
        self.serial_comms = serial.Serial(self.port, self.baud_rate)  # Establish the connection on a specific port
        self.serial_comms.open()
        return self.serial_comms.isOpen()

    def isConnected(self):
        return self.serial_comms.isOpen()

    def sendCommand(self, command, *dataPackets):
        # Check the inputs and then send the message
        message = self._buildMessage(i_commandID=command, *dataPackets)
        self.serial_comms.write(message)
        # Wait for the ack
        ack = self._waitForMessage()
        if not(ack is defs.EMPTY):
            # Received ack so now lets check if it is bad or good
            completed_msg = self._waitForMessage()
            if completed_msg is defs.EMPTY:
                raise custom_exceptions.Serial_Communication_Completed_Timeout()
            return self._convertReturnedData(id=completed_msg, data=completed_msg[defs.MSG_RDY:-1])
        else:
            raise custom_exceptions.Serial_Communication_Completed_Timeout()

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
        return bytearray([defs.HEADER_ID, i_commandID, info_byte, *dataPackets, defs.FOOTER_ID])

    def _waitForMessage(self):
        # initialize the message and header to empty
        message = defs.EMPTY
        header = defs.EMPTY
        for delay in range(int(defs.TIMEOUT/defs.REFRESH_DELAY)):
            # Check to see if we have a msg header
            if header is defs.EMPTY:
                header = self._checkForHeader()
                # Once we get the header lets check its header
                if not(header is defs.EMPTY):
                    if not(header[0] is defs.HEADER_ID):
                        raise custom_exceptions.Packet_Header_Error(byteReceived=header[0],
                                                                    byteDefault=defs.HEADER_ID)
            else:
                # Now we have the header, lets check to see if we have the full message
                msg_size = header[2]
                bytes_waiting = self.serial_comms.in_waiting
                if bytes_waiting >= msg_size:
                    # we should have the whole message, check its footer before putting it all together
                    message_data = self.serial_comms.read(bytes_waiting)
                    if not(message_data[-1] is defs.FOOTER_ID):
                        raise custom_exceptions.Packet_Footer_Error(byteReceived=message_data[-1],
                                                                    byteDefault=defs.FOOTER_ID)
                    # Check to make sure that there are the correct number of data bytes in the message considering the
                    # Cmd ID
                    if not(len(message_data) == defs.DATA_LENGTHS[header[1]]):
                        raise custom_exceptions.Packet_Data_Error(byteReceived=message_data[-1],
                                                                  byteDefault=defs.DATA_LENGTHS[header[1]])
                    message = header + message_data
                    break
            # wait a little bit between each serial operation
            time.sleep(defs.REFRESH_DELAY * defs.MS_CONV)
        return message

    def _checkForHeader(self):
        header = defs.EMPTY
        bytes_waiting = self.serial_comms.in_waiting
        if bytes_waiting >= defs.MSG_RDY:
            # Read the header, check if it is correct
            header = self.serial_comms.read(defs.MSG_RDY)
        else:
            return header

    def _convertReturnedData(self, id, data):
        # Check to see if this data needs to be converted/checked for size
        try:
            conv_func = defs.DATA_CONV[id]
        except KeyError:
            return data
        return conv_func(data)
