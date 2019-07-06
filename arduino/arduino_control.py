import serial
from tools import custom_exceptions
import time
from arduino import arduino_defs as defs


# Class that controls the arduino by sending commands and getting back data via Serial connection
class ArduinoControl:
    def __init__(self, port='auto', baudRate=defs.ARDUINO_BAUD_RATE):
        self.serial_comms = None

        self.port = port
        self.baud_rate = baudRate

        self.sequence_count = 0

    def _connectToPort(self, port):
        self.serial_comms = serial.Serial(port, self.baud_rate)  # Establish the connection on a specific port
        self.serial_comms.timeout = 0.1
        if not self.isConnected():
            self.serial_comms.open()
        self.serial_comms.read_all()
        self.port = port
        connected = self.serial_comms.isOpen()
        if not(connected):
            self.serial_comms.close()
            self.serial_comms = None
        return self.serial_comms.isOpen()

    def connect(self):
        if self.port is 'auto':
            for port in defs.COMMON_PORTS:
                try:
                    connected = self._connectToPort(port=port)
                    if connected:
                        break
                except:
                    connected = False
        else:
            connected = self._connectToPort(port=self.port)
        return connected

    def disconnect(self):
        if self.isConnected():
            self.serial_comms.close()
        return not(self.isConnected())

    def isConnected(self):
        return self.serial_comms.isOpen()

    def sendCommand(self, command, arr_data):
        # Check the inputs and then send the message
        message = self._buildMessage(i_commandID=command, arr_data=arr_data)
        self.serial_comms.write(message)
        time.sleep(0.1)
        # Wait for the ack
        ack = self._waitForMessage()
        if not(ack is defs.EMPTY):
            print("ack - %s" % str(list(ack)))
            # Check if ack is ok
            self._checkSequenceCount(count=ack[defs.IND_SEQ_COUNT])
            self._checkAckMsg(ack_msg=ack)
            # Received ack so now lets check if it is bad or good
            completed_msg = self._waitForMessage()
            if not(completed_msg is defs.EMPTY):
                print("comp - %s" % str(list(completed_msg)))
                print("")
                self._checkSequenceCount(count=completed_msg[defs.IND_SEQ_COUNT])
                self._checkCompletedMsg(completed_msg=completed_msg)
                return list(completed_msg)
            else:
                raise custom_exceptions.Serial_Communication_Completed_Timeout()
        else:
            raise custom_exceptions.Serial_Communication_Ack_Timeout()

    # Message Format [Header, commandID, Sequence Count, Size,    Data Packets(4),   Footer]
    # ex.            [0x7f,    0x01,           0x10,     0x05, 0xff, 0xff, 0x01, 0x01, 0xe7]
    def _buildMessage(self, i_commandID, arr_data):
        self._checkIfByteSized(data=i_commandID)
        for data_byte in arr_data:
            self._checkIfByteSized(data=data_byte)
        msg = [defs.HEADER_ID, i_commandID, self._getSequenceCount(), len(arr_data) + 1, ] + arr_data + [defs.FOOTER_ID]
        return bytearray(msg)

    def _waitForMessage(self):
        # initialize the message and header to empty
        message = defs.EMPTY
        header = defs.EMPTY
        # Check to see if we have a msg header
        header, time_remaining = self._waitForBytes(numBytes=defs.LEN_MSG_HEADER, timeout=defs.TIMEOUT)
        # Should have the header lets check it
        if not(header[defs.IND_HEADER_ID] is defs.HEADER_ID):
            raise custom_exceptions.Packet_Header_Error(byteReceived=header[defs.HEADER_ID],
                                                        byteDefault=defs.HEADER_ID)
        # Now we have the header, lets check to see if we have the full message
        msg_size = header[defs.IND_SIZE]
        message_data, time_remaining = self._waitForBytes(numBytes=msg_size, timeout=time_remaining)
        if not(message_data[defs.IND_FOOTER] is defs.FOOTER_ID):
            raise custom_exceptions.Packet_Footer_Error(byteReceived=message_data[defs.IND_FOOTER],
                                                        byteDefault=defs.FOOTER_ID)
        # Check to make sure that there are the correct number of data bytes in the message considering the
        # Cmd ID
        if not(len(message_data) == msg_size):
            raise custom_exceptions.Packet_Data_Error(byteReceived=message_data,
                                                      byteDefault=defs.DATA_LENGTHS[header[defs.IND_SIZE]])
        # wait a little bit between each serial operation
        return header + message_data

    def _checkIfByteSized(self, data):
        if data > 255:
            raise custom_exceptions.Bit_OverFlow
        if data < 0:
            raise custom_exceptions.Negative_Bit_value
        return data

    def _checkAckMsg(self, ack_msg):
        # TODO: finish
        pass

    def _checkCompletedMsg(self, completed_msg):
        # TODO: Finish
        pass

    def _getSequenceCount(self):
        self.sequence_count = (self.sequence_count + 1) & defs.SEQUENCE_COUNT_MAX
        return self.sequence_count

    def _checkSequenceCount(self, count):
        seq = self._getSequenceCount()
        if count != seq:
            print("got %i - wanted %i" % (count, seq))
            raise custom_exceptions.Sequence_Count_Error(countExpected=self.sequence_count, countGiven=count)

    def _waitForBytes(self, numBytes, timeout):
        empty_arr = defs.EMPTY
        for delay in range(int(timeout / defs.REFRESH_DELAY)):
            bytes_waiting = self.serial_comms.in_waiting
            if bytes_waiting >= numBytes:
                # Read the header, check if it is correct
                empty_arr = self.serial_comms.read(numBytes)
                break
            time.sleep(defs.REFRESH_DELAY * defs.MS_CONV)
        return empty_arr, timeout - delay


if __name__ == '__main__':
    a_control = ArduinoControl(port='COM5') #port='/dev/cu.usbmodem14101'
    a_control.connect()
    time.sleep(2)
    print(list(a_control.sendCommand(0x05, [0x00])))

    print(list(a_control.sendCommand(0x03, [0x00])))

    print(list(a_control.sendCommand(0x05, [0x00])))
    print(list(a_control.sendCommand(0x05, [0x00])))
    print(list(a_control.sendCommand(0x05, [0x00])))
    print(list(a_control.sendCommand(0x05, [0x00])))
    print(list(a_control.sendCommand(0x05, [0x00])))
    a_control.disconnect()
