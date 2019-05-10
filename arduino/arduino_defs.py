# Arduino Definitions ##################################################################################################
########################################################################################################################

ARDUNIO_PORT = ''
ARDUINO_BAUD_RATE = 9600

TIMEOUT = 50  # in ms
REFRESH_DELAY = 5  # in ms
MS_CONV = 0.001

# Message definitions ##################################################################################################
########################################################################################################################

MSG_RDY = 3  # Number of bytes in message header
EMPTY = []

HEADER_ID = 0x7F
FOOTER_ID = 0xa5

# CMD ID's
ID_COMPLETED = 0x01
ID_ACK = 0x02
ID_LIDAR_READ_REG = 0x03
ID_LIDAR_WRITE_REG = 0x04

# Return CMD ID's
ID_LIDAR_READ_DATA = 0x03


# Ack ID's
ACK_NO_ERROR = 0

# Completed ID's
COMPLETED_NO_ERROR = 0
COMPLETED_DATA = 1

# Message Data Lengths
DATA_LENGTHS = {}
DATA_LENGTHS[ID_COMPLETED] = 1
DATA_LENGTHS[ID_ACK] = 1
DATA_LENGTHS[ID_LIDAR_READ_REG] = 1
DATA_LENGTHS[ID_LIDAR_READ_DATA] = 1
DATA_LENGTHS[ID_LIDAR_WRITE_REG] = 2

DATA_CONV = {}
DATA_CONV[ID_COMPLETED] = int
DATA_CONV[ID_ACK] = int
DATA_CONV[ID_LIDAR_READ_REG] = int
DATA_CONV[ID_LIDAR_READ_DATA] = int