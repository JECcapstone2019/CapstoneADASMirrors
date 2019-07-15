#include <Wire.h>
#include <String.h>
#define FAST_I2C


const int BAUD_RATE = 9600;
const int REFRESH_DELAY = 100; // in ms
const int TIMEOUT = 5000; // in ms
const int LOOP_TIMEOUT = TIMEOUT/REFRESH_DELAY;
const int SEQUENCE_COUNT_MAX = 255;

// Message Length Definitions
const int LEN_MSG_HEADER = 4;
const int LEN_MSG_FOOTER = 1;

// Other Message Definitions
const byte MSG_HEADER = 0x61;
const byte MSG_FOOTER = 0x63;

const byte EMPTY[1] = {0x00};

// Message Index Definitions
const int MSG_HEADER_IND = 0;
const int MSG_CMD_IND = 1;
const int MSG_SEQ_IND = 2;
const int MSG_SIZE_IND = 3;

int SEQUENCE_COUNT = 0;

// Command ID Definitions
const int CMD_COMPLETED = 0x01;
const int CMD_ACK = 0x02;
const int CMD_LIDAR_SETUP = 0x03;
const int CMD_LIDAR_DISTANCE = 0x04;
const int CMD_NOP = 0x05;
const int CMD_I2C_READ = 0x06;
const int CMD_I2C_WRITE = 0x07;

// Data Return ID Definitions
const int COMPLETE_NO_ERROR = 0x00;
const int COMPLETE_UNRECOGNIZED_CMD = 0x01;
const int COMPLETE_NO_LIDAR_READ = 0x02;
const int COMPLETE_LIDAR_READ_DATA = 0x03;
const int COMPLETE_CANT_SET_LIDAR = 0x04;
const int COMPLETE_WRONG_CMD_LENGTH = 0x05;
const int COMPLETE_I2C_READ_ERROR = 0x06;
const int COMPLETE_I2C_TIMEOUT = 0x07;

// Ack Errors
const int ACK_NO_ERROR = 0x00;
const int ACK_HEADER_ERROR = 0x01;
const int ACK_FOOTER_ERROR = 0x02;
const int ACK_SIZE_ERROR = 0x03;
const int ACK_TIMEOUT_ERROR = 0x04;

// Completed Errors

// LIDAR Definitions
const int LIDAR_I2C_ADDRESS = 0x62;

// Supporting Functions

int I2CWriteByte(byte registerAddress, byte myValue, byte deviceAddress)
{
  Wire.beginTransmission((int)deviceAddress);
  Wire.write((int)registerAddress); // Set register for write
  Wire.write((int)myValue); // Write myValue to register

  // A nack means the device is not responding, report the error over serial
  int nackCatcher = Wire.endTransmission();
  delay(1); // 1 ms delay recommended
  return nackCatcher; // 0 means no error
  /*
  if(nackCatcher != 0)
  {
    //Serial.println("> NAK_A");
  } else
  {
   // Serial.println("> AK_A");
  }
`*/
}

int I2CWriteByteArray(byte deviceAddress, byte firstRegisterAddress, int numBytes, byte *writeArray){
    // TODO: if needed
}

// Command Functions ///////////////////////////////////////////////////////////////////////////////////////////////////

// Do nothing and send a completed message with no error
void cmd_nop(){
    sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
}

void cmd_initLIDAR(){

  //Serial.begin(9600); //Initialize serial connect for display purposes
  Wire.begin();

  //Serial.print(LIDAR_I2C_ADDRESS);
  //delay(5000);

  //SETUP DEFAULT CONFIG -
  int checkA = I2CWriteByte(0x02,0x80,LIDAR_I2C_ADDRESS); // Default
  int checkB = I2CWriteByte(0x04,0x08,LIDAR_I2C_ADDRESS); // Default
  int checkC = I2CWriteByte(0x1c,0x00,LIDAR_I2C_ADDRESS); // Default

  int checkError = checkA*checkB*checkC;
  if (checkError == 0) {
    sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
   }else{
    sendCompletedMessage(COMPLETE_CANT_SET_LIDAR, 1, EMPTY);
   }
}

void cmd_readDist(){

  int dist;
  byte recByte;

  I2CWriteByte(0x00,0x04,LIDAR_I2C_ADDRESS);
  byte distanceArray[2] = {0x01, 0xff};
  byte myAddress = 0x8f; // location of distance information **NOTE THERE IS A VELOCITY ONE TOO
  int numOfBytes = 2;

   Wire.beginTransmission((int)LIDAR_I2C_ADDRESS);
   Wire.write((int)myAddress); // Set the register to be read

   // A nack means the device is not responding, report the error over serial
   int nackCatcher = Wire.endTransmission();
   delay(1);


   // Request the two bytes
   Wire.requestFrom((int)LIDAR_I2C_ADDRESS, numOfBytes);
   int i = 0;
   if(numOfBytes <= Wire.available())
   {
      while(i < numOfBytes)
      {
        distanceArray[i] = Wire.read();
        i++;
      }
   }

  // Shift and add
  //int distance = (distanceArray[0] << 8) + distanceArray[1];
  //Serial.println(distance);

  //delay(1000);

   if(nackCatcher != 0)
   {
        sendCompletedMessage(COMPLETE_NO_LIDAR_READ, 1, EMPTY);
     //Serial.println("> nack");
   }else{
        sendCompletedMessage(COMPLETE_LIDAR_READ_DATA, 3, distanceArray);
   }

}

const int LEN_I2C_CMD = 3; // Proper length of I2C Commands

// message data received should be in [I2C address, register address, numBytes to read, footer]
void cmd_I2CReadByteArray(int data_footer_size, byte *message_data_footer){
    // check if data is the correct size
    if(data_footer_size < LEN_I2C_CMD){
        sendCompletedMessage(COMPLETE_WRONG_CMD_LENGTH, 1, EMPTY);
        return;
    }
    int deviceAddress = message_data_footer[0];
    int registerAddress = message_data_footer[1];
    int numOfBytes = message_data_footer[2];
    Wire.beginTransmission(deviceAddress);
    Wire.requestFrom(registerAddress, numOfBytes);
    bool msg_received = false;
    byte valueBuffer[numOfBytes];

    // wait about 5ms for each byte
    for(int delay_wait = 0; delay_wait < (5 * numOfBytes); delay_wait++){
        // check if the correct num of bytes are ready
        if(Wire.available() >= numOfBytes){
            // read bytes into buffer, say msg received
            for(int value = 0; value  < numOfBytes; value++){
                valueBuffer[value] = Wire.read();
                msg_received = true;
            }
        }
        else{
            delay(1);
        }
    }
    if(Wire.endTransmission() != 0){
        sendCompletedMessage(COMPLETE_I2C_READ_ERROR, 1, EMPTY);
    }
    else if(msg_received != true){
        sendCompletedMessage(COMPLETE_I2C_TIMEOUT, 1, EMPTY);
    }
    else{
        sendCompletedMessage(COMPLETE_NO_ERROR, numOfBytes, valueBuffer);
    }
    return;
}

// message data received should be in [I2C address, register address, writeByte1, writeByte2, ..., writeByteN, footer]
void cmd_I2CWriteByteArray(int data_footer_size, byte *message_data_footer){
    // check if data is the correct size
    if(data_footer_size < LEN_I2C_CMD){
        sendCompletedMessage(COMPLETE_WRONG_CMD_LENGTH, 1, EMPTY);
        return;
    }
    int deviceAddress = message_data_footer[0];
    int registerAddress = message_data_footer[1];
    int numOfBytes = data_footer_size - LEN_I2C_CMD + 1;

    // grab the subsection of the array
    byte writeArray[numOfBytes];
    for(int i = 0; i < numOfBytes; i++){
        writeArray[i] = message_data_footer[i+LEN_I2C_CMD];
    }

    Wire.beginTransmission(deviceAddress);
    Wire.write(writeArray, numOfBytes);

    if(Wire.endTransmission() != 0){
        sendCompletedMessage(COMPLETE_I2C_READ_ERROR, 1, EMPTY);
    }
    else{
        sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
    }
    return;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Serial Functions ////////////////////////////////////////////////////////////////////////////////////////////////////
void emptySerialBuffer(){
    // Read until no more bytes in the buffer
    while (Serial.read() >= 0);
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Message Creation Functions //////////////////////////////////////////////////////////////////////////////////////////

// Create a byte message for sending to the host and put it in the message[] buffer
void sendMessage(int cmd_id, int data_size, byte *data){
    int message_length = LEN_MSG_HEADER + data_size + LEN_MSG_FOOTER;
    byte message[message_length];
    SEQUENCE_COUNT = SEQUENCE_COUNT + 1;
    SEQUENCE_COUNT = SEQUENCE_COUNT & SEQUENCE_COUNT_MAX;
    message[MSG_HEADER_IND] = MSG_HEADER;
    message[MSG_CMD_IND] = byte(cmd_id);
    message[MSG_SEQ_IND] = byte(SEQUENCE_COUNT);
    message[MSG_SIZE_IND] = byte(data_size + LEN_MSG_FOOTER);
    message[message_length - LEN_MSG_FOOTER] = MSG_FOOTER;
    for(int data_ind = 0; data_ind < data_size; data_ind++){
            message[data_ind + LEN_MSG_HEADER] = data[data_ind];
    }
    Serial.write(message, message_length);
    return;
}

// Create an ack message by giving it the code
void sendAckMessage(int rCode){
    byte code[1] = {byte(rCode)};
    sendMessage(CMD_ACK, 1, code);
    return;
}

// Create a completed message by giving it the code and data associated if any
void sendCompletedMessage(int rCode, int data_length, byte* data){
    byte new_data[1 + data_length];
    new_data[0] = byte(rCode);
    for(int i=0; i< data_length; i++){
        new_data[i + 1] = data[i];
    }
    sendMessage(CMD_COMPLETED, data_length, new_data);
    return;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Parse the message to see what it wants us to do
void parseMessage(int cmd_id, int data_footer_size, byte *message_data_footer){
    if(cmd_id == CMD_NOP){
        cmd_nop();
    }
    else if(cmd_id == CMD_LIDAR_SETUP){
        cmd_initLIDAR();
    }
    else if(cmd_id == CMD_LIDAR_DISTANCE){
        cmd_readDist();
    }
    else if(cmd_id == CMD_I2C_READ){
        cmd_I2CReadByteArray(data_footer_size, message_data_footer);
    }
    else if(cmd_id == CMD_I2C_WRITE){
        cmd_I2CWriteByteArray(data_footer_size, message_data_footer);
    }
    else{
        // Unrecognized Command ID - Return Error
        sendCompletedMessage(COMPLETE_UNRECOGNIZED_CMD, 1, EMPTY);
    }
}

// Setup the serial communications
void setup() {
    Serial.begin(BAUD_RATE);
    // Initialize Arduino I2C (for communication to LidarLite)
    Wire.begin();
    #ifdef FAST_I2C
        #if ARDUINO >= 157
            Wire.setClock(400000UL); // Set I2C frequency to 400kHz (for Arduino Due)
        #else
            TWBR = ((F_CPU / 400000UL) - 16) / 2; // Set I2C frequency to 400kHz
        #endif
    #endif
}

void loop() {
    // byte array for containing the message header
    byte message_header[LEN_MSG_HEADER];
    // Pointer to the array containing the rest of the data
    byte *message;
    int msg_send_length;
    int bytes_available = 0;
    int msg_size = 0;
    bool data_received = false;
    bool header_received = false;
    bool ack_sent = false;
    // Timeout at 50ms
    for(int delay_wait = 0; delay_wait < LOOP_TIMEOUT; delay_wait++){
        // check how many bytes we have
        bytes_available = Serial.available();
        if(bytes_available > 0){
            data_received = true;
        }
        if(header_received == false){
            if(bytes_available >= LEN_MSG_HEADER){
                // Received a message - lets check its parameters and see what we need
                Serial.readBytes(message_header, LEN_MSG_HEADER);
                if(message_header[MSG_HEADER_IND] != MSG_HEADER){
                    // Invalid termination, something is wrong with this message
                    sendAckMessage(ACK_HEADER_ERROR);
                    // Clear the buffer
                    emptySerialBuffer();
                    ack_sent = true;
                    break;
                }
                else{
                // Message Header is good
                // Grab the correct message size and let the loop know we have the header
                msg_size = (int) message_header[MSG_SIZE_IND];
                // Grab the messages sequence count as well
                SEQUENCE_COUNT = (int) message_header[MSG_SEQ_IND];
                header_received = true;
                }
            }
        }
        else{
            // We have the header, lets see if the rest of the data is here
            if(bytes_available == msg_size){
                // All the bytes should be here now
                byte message_data_footer[msg_size];
                Serial.readBytes(message_data_footer, msg_size);
                message = message_data_footer;
                int cmd_id = (int) message_header[MSG_CMD_IND];
                // Check the footer
                if(message[msg_size - LEN_MSG_FOOTER] == MSG_FOOTER){
                    // Send an ack back saying we got the message
                    sendAckMessage(ACK_NO_ERROR);
                    // Remove the footer and then ship off the data to the parser
                    parseMessage(cmd_id, msg_size, message);
                    ack_sent = true;
                    break;
                }
                else{
                    sendAckMessage(ACK_FOOTER_ERROR);
                    ack_sent = true;
                    break;
                }
            }
        }
        // Don't have full message yet, wait until timeout
        delay(REFRESH_DELAY);
    }
    // Timed out without grabbing a full message
    if((ack_sent == false) & (data_received)){
        // Clear the buffer
        emptySerialBuffer();
        sendAckMessage(ACK_TIMEOUT_ERROR);
    }
    // Wait a bit before checking again
    delay(REFRESH_DELAY);
}
