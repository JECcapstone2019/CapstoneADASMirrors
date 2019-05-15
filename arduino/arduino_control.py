import serial
from tools import custom_exceptions
import time
from arduino import arduino_defs as defs

class SerialMsg:
    def __init__(self, cmd_id=0, header_id=defs.HEADER_ID, footer_id=defs.FOOTER_ID, *dataBytes):
        self.cmd_id = self._checkIfByteSized(cmd_id)
        self.footer_id = self._checkIfByteSized(footer_id)
        self.header_id = self._checkIfByteSized(header_id)
        self.data = []
        for dataByte in dataBytes:
            self.data += self._checkIfByteSized(dataByte)
        self.size = self._checkIfByteSized(len(self.data) + 1)

    def getBytes(self):
        return bytearray([self.header, self.cmd_id, self.size, self.data, self.footer])

    def setFromByteArray(self, byteArray):
        raise NotImplementedError

    def _checkIfByteSized(self, data):
        if data > 255:
            raise custom_exceptions.Bit_OverFlow
        if data < 0:
            raise custom_exceptions.Negative_Bit_value
        return data

    def _convertReturnedData(self):
        # Check to see if this data needs to be converted/checked for size
        try:
            conv_func = defs.DATA_CONV[self.cmd_id]
        except KeyError:
            return self.data
        return conv_func(self.data)


# Class that controls the arduino by sending commands and getting back data via Serial connection
class ArduinoControl:
    def __init__(self, port=defs.ARDUNIO_PORT, baudRate=defs.ARDUINO_BAUD_RATE):
        self.serial_comms = None

        self.port = port
        self.baud_rate = baudRate

    def connect(self):
        self.serial_comms = serial.Serial(self.port, self.baud_rate)  # Establish the connection on a specific port
        self.serial_comms.timeout = 0.1
        if not self.isConnected():
            self.serial_comms.open()
        return self.serial_comms.isOpen()

    def disconnect(self):
        if self.isConnected():
            self.serial_comms.close()
        return self.isConnected()

    def isConnected(self):
        return self.serial_comms.isOpen()

    def sendCommand(self, command, arr_data):
        # Check the inputs and then send the message
        message = self._buildMessage(i_commandID=command, arr_data=arr_data)
        print(message)
        self.serial_comms.write(message)
        # Wait for the ack
        ack = self._waitForMessage()
        if not(ack is defs.EMPTY):
            # Check if ack is ok
            print(ack)
            self._checkAckMsg(ack_msg=ack)
            # Received ack so now lets check if it is bad or good
            completed_msg = self._waitForMessage()
            if not(completed_msg is defs.EMPTY):
                print(completed_msg)
                data = self._checkCompletedMsg(completed_msg=completed_msg)
            else:
                raise custom_exceptions.Serial_Communication_Completed_Timeout()
        else:
            raise custom_exceptions.Serial_Communication_Completed_Timeout()

    # Message Format [Header, commandID, Size,    Data Packets,      Footer]
    # ex.            [0x7f,    0x01,     0x05, 0xff, 0xff, 0x01, 0x01, 0xe7]
    def _buildMessage(self, i_commandID, arr_data):
        self._checkIfByteSized(data=i_commandID)
        for data_byte in arr_data:
            self._checkIfByteSized(data=data_byte)
        msg = [defs.HEADER_ID, i_commandID, len(arr_data) + 1, ] + arr_data + [defs.FOOTER_ID]
        return bytearray(msg)

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
                    if not(header[defs.HEADER_ID] is defs.HEADER_ID):
                        raise custom_exceptions.Packet_Header_Error(byteReceived=header[defs.HEADER_ID],
                                                                    byteDefault=defs.HEADER_ID)
            else:
                # Now we have the header, lets check to see if we have the full message
                msg_size = header[defs.IND_SIZE]
                bytes_waiting = self.serial_comms.in_waiting
                if bytes_waiting >= msg_size:
                    # we should have the whole message, check its footer before putting it all together
                    message_data = self.serial_comms.read(msg_size)
                    if not(message_data[defs.IND_FOOTER] is defs.FOOTER_ID):
                        raise custom_exceptions.Packet_Footer_Error(byteReceived=message_data[defs.IND_FOOTER],
                                                                    byteDefault=defs.FOOTER_ID)
                    # Check to make sure that there are the correct number of data bytes in the message considering the
                    # Cmd ID
                    if not(len(message_data) == msg_size):
                        raise custom_exceptions.Packet_Data_Error(byteReceived=message_data,
                                                                  byteDefault=defs.DATA_LENGTHS[header[defs.IND_SIZE]])
                    message = header + message_data
                    break
            # wait a little bit between each serial operation
            time.sleep(defs.REFRESH_DELAY * defs.MS_CONV)
        return message

    def _checkForHeader(self):
        header = defs.EMPTY
        bytes_waiting = self.serial_comms.in_waiting
        if bytes_waiting >= defs.LEN_MSG_HEADER:
            # Read the header, check if it is correct
            header = self.serial_comms.read(defs.LEN_MSG_HEADER)
        else:
            return header

    def _checkIfByteSized(self, data):
        if data > 255:
            raise custom_exceptions.Bit_OverFlow
        if data < 0:
            raise custom_exceptions.Negative_Bit_value
        return data

    def _checkAckMsg(self, ack_msg):
        if not(ack_msg[defs.IND_CODE] is defs.ACK_NO_ERROR):
            raise Exception

    def _checkCompletedMsg(self, completed_msg):
        if not(completed_msg[defs.IND_CODE] is defs.COMPLETED_NO_ERROR):
            raise Exception


if __name__ == '__main__':
    a_control = ArduinoControl(port='COM4')
    a_control.connect()
    a_control.sendCommand(0x05, [0x00])
    a_control.disconnect()
