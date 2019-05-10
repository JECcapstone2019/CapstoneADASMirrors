#include <Wire.h>
#include <String.h>

const int BAUD_RATE = 9600;
const int REFRESH_DELAY = 5; // in ms
const int TIMEOUT = 50; // in ms
const int MSG_READY = 3; // This will contain the msg header, cmdID, and size

// Communication with Python constants
const byte MSG_HEADER = 0x7f;
const byte MSG_FOOTER = 0xa5;

const int MSG_HEADER_IND = 0;
const int MSG_CMD_IND = 1;
const int MSG_SIZE_IND = 2;

// Command Definitions
const int CMD_COMPLETED = 0x01;
const int CMD_ACK = 0x02;
const int CMD_LIDAR_READ_REG = 0x03;
const int CMD_LIDAR_WRITE_REG = 0x04;

// Data Return Definitions
const int CMD_LIDAR_READ_DATA = 0x01;

// Ack Errors
const int ACK_NO_ERROR = 0x00;
const int ACK_HEADER_ERROR = 0x01;
const int ACK_FOOTER_ERROR = 0x02;
const int ACK_SIZE_ERROR = 0x03;
const int ACK_TIMEOUT_ERROR = 0x04;

// Completed Errors

// Command Functions


// Serial Functions
void emptySerialBuffer(){
    // Read until no more bytes in the buffer
    while (Serial.read() >= 0);
}

byte* createMessage(int cmd_id, byte *data){
    int data_length = sizeof(data) + 1;
    int message_length = MSG_READY + data_length;
    byte message[message_length];
    message[0] = MSG_HEADER;
    message[1] = byte(cmd_id);
    message[2] = data_length;
    message[message_length - 1] = MSG_FOOTER;
    for(int data_ind = 0; data_ind < sizeof(data); data_ind++){
            message[data_ind + MSG_READY] = data[data_ind];
    }
    byte *msg_handle = message;
    return msg_handle;
}

byte* createAckMessage(int rCode){
    byte* code = byte(rCode);
    return createMessage(CMD_ACK, code);
}

byte* createCompletedMessage(int rCode, byte* data){
    int data_length = sizeof(data);
    byte code = byte(rCode);
    byte new_data[data_length + 1];
    new_data[0] = code;
    for(int i=0; i< data_length; i++){
        new_data[i + 1] = data[i];
    }
    byte *data_handle = new_data;
    return createMessage(CMD_COMPLETED, new_data);
}

// Parse the message to see what it wants us to do
byte* parseMessage(int cmd_id, byte *message_data){
    byte *completed_msg;
    if(cmd_id == CMD_LIDAR_READ_REG){
    }
    else if(cmd_id == CMD_LIDAR_WRITE_REG){
    }
    else{
        // Unrecognized Command ID - Return Error
        completed_msg = &MSG_FOOTER;
    }
    return completed_msg;
}

byte* removeFooter(byte* message_data){
    int data_length = sizeof(message_data);
    byte new_data[data_length - 1];
    for(int i=0; i < data_length - 1; i++){
        new_data[i] = message_data[i];
    }
    byte *data_handle = new_data;
    return data_handle;
}

void setup() {
    Wire.begin();
    Serial.begin(BAUD_RATE);
}

void loop() {
    byte *message;
    // Check if there is a full instruction set available
    int bytes_available = Serial.available();
    if(bytes_available >= MSG_READY){
        bool msg_completed = false;
        // Received a message - lets check its parameters and see what we need
        Serial.readBytes(message, MSG_READY);
        if(message[MSG_HEADER_IND] != MSG_HEADER){
            // Invalid termination, something is wrong with this message
            byte* ack_msg = createAckMessage(ACK_HEADER_ERROR);
            Serial.write(*ack_msg);
            // Clear the buffer
            emptySerialBuffer();
        }
        else{
            // Check how many bytes we need for a full message
            byte *message_data;
            int msg_size = (int) message[MSG_SIZE_IND];
            // Timeout at 50ms
            for(int delay_wait = 0; delay_wait < (TIMEOUT/REFRESH_DELAY); delay_wait++){
                // check if we have the full message now
                bytes_available = Serial.available();
                if(bytes_available == msg_size){
                    // All the bytes should be here now
                    Serial.readBytes(message_data, bytes_available);
                    msg_completed = true;
                    int cmd_id = (int) message[MSG_CMD_IND];
                    // Check the footer
                    if(message[MSG_READY + msg_size - 1] == MSG_FOOTER){
                        // Send an ack back saying we got the message
                        byte* ack_msg = createAckMessage(ACK_NO_ERROR);
                        Serial.write(*ack_msg);
                        // Remove the footer and then ship off the data to the parser
                        message_data = removeFooter(message_data);
                        byte *completed_msg = parseMessage(cmd_id, message_data);
                        Serial.write(*completed_msg);
                        break;
                    }
                    else{
                        byte* ack_msg = createAckMessage(ACK_FOOTER_ERROR);
                        Serial.write(*ack_msg);
                    }
                }
                // Don't have full message yet, wait until timeout
                else{
                    delay(REFRESH_DELAY);
                }
            }
            if(msg_completed == false){
                byte* ack_msg = createAckMessage(ACK_TIMEOUT_ERROR);
                Serial.write(*ack_msg);
            }
            // Clear the buffer
            emptySerialBuffer();
        }
    }
    // Wait a bit before checking again
    delay(REFRESH_DELAY);
}
