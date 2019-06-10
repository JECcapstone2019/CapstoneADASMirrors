# Arduino Definitions ##################################################################################################
########################################################################################################################

ARDUNIO_PORT = 'COM4'
ARDUINO_BAUD_RATE = 9600

TIMEOUT = 5000  # in ms
REFRESH_DELAY = 100  # in ms
MS_CONV = 0.001
SEQUENCE_COUNT_MAX = 0xff

# Message definitions ##################################################################################################
########################################################################################################################

LEN_MSG_HEADER = 3  # Number of bytes in message header
LEN_MSG_FOOTER = 1  # Number of bytes in message header

IND_HEADER_ID = 0  # Number of bytes in message header
IND_CMD_ID = 1  # Number of bytes in message header
IND_SEQ_COUNT = 1  # Number of bytes in message header
IND_SIZE = 3  # Number of bytes in message header
IND_FOOTER = -1  # Number of bytes in message header

EMPTY = []

HEADER_ID = 0x61
FOOTER_ID = 0x63

# CMD ID's
ID_COMPLETED = 0x01
ID_ACK = 0x02
ID_LIDAR_READ_REG = 0x03
ID_LIDAR_WRITE_REG = 0x04
ID_NOP = 0x05

# Return CMD ID's
ID_LIDAR_READ_DATA = 0x03


# Ack ID's
ACK_NO_ERROR = 0x00
ACK_HEADER_ERROR = 0x01
ACK_FOOTER_ERROR = 0x02
ACK_SIZE_ERROR = 0x03
ACK_TIMEOUT_ERROR = 0x04


# Completed ID's
COMPLETED_NO_ERROR = 0
COMPLETED_DATA = 1
