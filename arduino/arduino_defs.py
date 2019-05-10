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
LIDAR_READ_REG = 0x00
LIDAR_WRITE_REG = 0x01

# Message Data Lengths
DATA_LENGTHS = {}
DATA_LENGTHS[LIDAR_READ_REG] = 1
DATA_LENGTHS[LIDAR_WRITE_REG] = 2

DATA_CONV = {}
DATA_CONV[0] = int
DATA_CONV[1] = int