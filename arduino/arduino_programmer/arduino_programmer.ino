#include <Wire.h>
#include <String.h>

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
const int CMD_LIDAR_READ = 0x04;
//const int CMD_LIDAR_READ_REG = 0x03;
//const int CMD_LIDAR_WRITE_REG = 0x04;
const int CMD_NOP = 0x05;

// Data Return ID Definitions
const int COMPLETE_NO_ERROR = 0x00;
const int COMPLETE_UNRECOGNIZED_CMD = 0x01;
const int COMPLETE_NO_LIDAR_READ = 0x02;
const int COMPLETE_LIDAR_READ_DATA = 0x03;
const int COMPLETE_CANT_SET_LIDAR = 0x04;

// Ack Errors
const int ACK_NO_ERROR = 0x00;
const int ACK_HEADER_ERROR = 0x01;
const int ACK_FOOTER_ERROR = 0x02;
const int ACK_SIZE_ERROR = 0x03;
const int ACK_TIMEOUT_ERROR = 0x04;

// Completed Errors

// Command Functions ///////////////////////////////////////////////////////////////////////////////////////////////////


// Supporting Functions

int writeTest(byte myAddress, byte myValue, byte lidarliteAddress)
{
  Wire.beginTransmission((int)lidarliteAddress);
  Wire.write((int)myAddress); // Set register for write
  Wire.write((int)myValue); // Write myValue to register

  // A nack means the device is not responding, report the error over serial
  int nackCatcher = Wire.endTransmission();
  return nackCatcher // 0 means no error
  /*
  if(nackCatcher != 0)
  {
    //Serial.println("> NAK_A");
  } else
  {
   // Serial.println("> AK_A");
  }
`*/

  delay(2); // 1 ms delay recommended
}


// Do nothing and send a completed message with no error
void cmd_nop(){
    sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
}

void cmd_initLIDAR(){

  //Serial.begin(9600); //Initialize serial connect for display purposes
  Wire.begin();

  byte lidarliteAddress = 0x62; //98 - slave address
  //Serial.print(lidarliteAddress);
  //delay(5000);

  //SETUP DEFAULT CONFIG -
  checkA = writeTest(0x02,0x80,lidarliteAddress); // Default
  checkB = writeTest(0x04,0x08,lidarliteAddress); // Default
  checkC = writeTest(0x1c,0x00,lidarliteAddress); // Default

  checkError = checkA*checkB*checkC;
  if (checkError == 0) {
    sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
   }else{
    sendCompletedMessage(COMPLETE_CANT_SET_LIDAR, 1, EMPTY);
   }
}

void cmd_readDist(){

  int dist;
  byte recByte;

  byte lidarliteAddress = 0x62; //98 - slave address
  writeTest(0x00,0x04,lidarliteAddress);
  byte distanceArray[2] = {0x01, 0xff};
  byte myAddress = 0x8f; // location of distance information **NOTE THERE IS A VELOCITY ONE TOO
  int numOfBytes = 2;

   Wire.beginTransmission((int)lidarliteAddress);
   Wire.write((int)myAddress); // Set the register to be read

   // A nack means the device is not responding, report the error over serial
   int nackCatcher = Wire.endTransmission();


   // Request the two bytes
   Wire.requestFrom((int)lidarliteAddress, numOfBytes);
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

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Serial Functions ////////////////////////////////////////////////////////////////////////////////////////////////////
void emptySerialBuffer(){
    // Read until no more bytes in the buffer
    while (Serial.read() >= 0);
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Message Creation Functions //////////////////////////////////////////////////////////////////////////////////////////
void updateSequenceCount(){
    SEQUENCE_COUNT = (SEQUENCE_COUNT + 1);
    if(SEQUENCE_COUNT > SEQUENCE_COUNT_MAX){
        SEQUENCE_COUNT = 0;
    }
}

// Create a byte message for sending to the host and put it in the message[] buffer
void sendMessage(int cmd_id, int data_size, byte *data){
    int message_length = LEN_MSG_HEADER + data_size + LEN_MSG_FOOTER;
    byte message[message_length];
    updateSequenceCount();
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
    else if(cmd_id == CMD_LIDAR_READ){
        cmd_readDist();
    }
    else{
        // Unrecognized Command ID - Return Error
        sendCompletedMessage(COMPLETE_UNRECOGNIZED_CMD, 1, EMPTY);
    }
}

// Setup the serial communications
void setup() {
    Wire.begin();
    Serial.begin(BAUD_RATE);
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
    bool msg_completed = false;
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
                msg_completed = true;
                int cmd_id = (int) message_header[MSG_CMD_IND];
                // Check the footer
                if(message[msg_size - LEN_MSG_FOOTER] == MSG_FOOTER){
                    // Send an ack back saying we got the message
                    sendAckMessage(ACK_NO_ERROR);
                    // Remove the footer and then ship off the data to the parser
                    parseMessage(cmd_id, msg_size, message);
                    break;
                }
                else{
                    sendAckMessage(ACK_FOOTER_ERROR);
                    ack_sent = true;
                    break;
                }
            }
            // Don't have full message yet, wait until timeout
            else{
                delay(REFRESH_DELAY);
            }
        }
    }
    // Timed out without grabbing a full message
    if(data_received & (msg_completed == false) & (ack_sent == false)){
        sendAckMessage(ACK_TIMEOUT_ERROR);
    }
    // Clear the buffer
    emptySerialBuffer();
    // Wait a bit before checking again
    delay(REFRESH_DELAY);
}
