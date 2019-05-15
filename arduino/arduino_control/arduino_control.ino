#include <Wire.h>
#include <String.h>

const int BAUD_RATE = 9600;
const int REFRESH_DELAY = 5; // in ms
const int TIMEOUT = 50; // in ms

// Message Length Definitions
const int LEN_MSG_HEADER = 3;
const int LEN_MSG_FOOTER = 1;

// Other Message Definitions
const byte MSG_HEADER = 0x7f;
const byte MSG_FOOTER = 0xa5;

const byte EMPTY = 0x00;

// Message Index Definitions
const int MSG_HEADER_IND = 0;
const int MSG_CMD_IND = 1;
const int MSG_SIZE_IND = 2;

// Command ID Definitions
const int CMD_COMPLETED = 0x01;
const int CMD_ACK = 0x02;
const int CMD_LIDAR_READ_REG = 0x03;
const int CMD_LIDAR_WRITE_REG = 0x04;
const int CMD_NOP = 0x05;

// Data Return ID Definitions
const int COMPLETE_NO_ERROR = 0x00;
const int COMPLETE_UNRECOGNIZED_CMD = 0x01;
const int COMPLETE_LIDAR_READ_DATA = 0x03;

// Ack Errors
const int ACK_NO_ERROR = 0x00;
const int ACK_HEADER_ERROR = 0x01;
const int ACK_FOOTER_ERROR = 0x02;
const int ACK_SIZE_ERROR = 0x03;
const int ACK_TIMEOUT_ERROR = 0x04;

// Completed Errors

// Command Functions ///////////////////////////////////////////////////////////////////////////////////////////////////

// Do nothing and send a completed message with no error
void cmd_nop(int data_footer_size, byte *message_data_footer){
    sendCompletedMessage(COMPLETE_NO_ERROR, 1, EMPTY);
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
    message[0] = MSG_HEADER;
    message[1] = byte(cmd_id);
    message[2] = data_length;
    message[message_length - LEN_MSG_FOOTER] = MSG_FOOTER;
    for(int data_ind = 0; data_ind < sizeof(data); data_ind++){
            message[data_ind + LEN_MSG_HEADER] = data[data_ind];
    }
    Serial.write(message, message_length);
    return;
}

// Create an ack message by giving it the code
void sendAckMessage(int rCode){
    byte* code = byte(rCode);
    sendMessage(CMD_ACK, 1, code);
    return;
}

// Create a completed message by giving it the code and data associated if any
void sendCompletedMessage(int rCode, int data_length, byte* data){
    byte code = byte(rCode);
    byte new_data[1 + data_length];
    new_data[0] = code;
    for(int i=0; i< data_length; i++){
        new_data[i + 1] = data[i];
    }
    byte *data_handle = new_data;
    createMessage(CMD_COMPLETED, data_length, data_handle);
    return;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Parse the message to see what it wants us to do
void parseMessage(int cmd_id, int data_footer_size, byte *message_data_footer){
    if(cmd_id == CMD_LIDAR_READ_REG){
    }
    else if(cmd_id == CMD_LIDAR_WRITE_REG){
    }
    else if(cmd_id == CMD_NOP){
        cmd_nop();
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
    Serial.write('0');
    int msg_send_length;
    byte* ack_msg;

    // Check if there is a full instruction set available
    int bytes_available = Serial.available();
    if(bytes_available >= LEN_MSG_HEADER){
        bool msg_completed = false;
        // Received a message - lets check its parameters and see what we need
        Serial.readBytes(message_header, LEN_MSG_HEADER);
        if(message_header[MSG_HEADER_IND] != MSG_HEADER){
            // Invalid termination, something is wrong with this message
            Serial.write('1');
            ack_msg = createAckMessage(ACK_HEADER_ERROR);
            msg_send_length = LEN_MSG_HEADER + ack_msg[MSG_SIZE_IND];
            Serial.write(*ack_msg, msg_send_length);
            // Clear the buffer
            emptySerialBuffer();
        }
        else{
            // Check how many bytes we need for a full message
            int msg_size = (int) message[MSG_SIZE_IND];
            // Timeout at 50ms
            for(int delay_wait = 0; delay_wait < (TIMEOUT/REFRESH_DELAY); delay_wait++){
                Serial.write('2');
                // check if we have the full message now
                bytes_available = Serial.available();
                if(bytes_available == msg_size){
                    // All the bytes should be here now
                    byte message_data_footer[msg_size];
                    Serial.readBytes(message_data_footer, msg_size);
                    message &= message_data_footer;
                    msg_completed = true;
                    int cmd_id = (int) message_header[MSG_CMD_IND];
                    // Check the footer
                    if(message[msg_size - LEN_MSG_FOOTER] == MSG_FOOTER){
                        // Send an ack back saying we got the message
                        ack_msg = createAckMessage(ACK_NO_ERROR);
                        msg_send_length = LEN_MSG_HEADER + ack_msg[MSG_SIZE_IND];
                        Serial.write(*ack_msg);
                        // Remove the footer and then ship off the data to the parser
                        parseMessage(cmd_id, msg_size, message);
                        break;
                    }
                    else{
                        ack_msg = createAckMessage(ACK_FOOTER_ERROR);
                        msg_send_length = LEN_MSG_HEADER + ack_msg[MSG_SIZE_IND];
                        Serial.write(*ack_msg);
                    }
                }
                // Don't have full message yet, wait until timeout
                else{
                    delay(REFRESH_DELAY);
                }
            }
            if(msg_completed == false){
                ack_msg = createAckMessage(ACK_TIMEOUT_ERROR);
                msg_send_length = LEN_MSG_HEADER + ack_msg[MSG_SIZE_IND];
                Serial.write(*ack_msg);
            }
            // Clear the buffer
            emptySerialBuffer();
        }
    }
    // Wait a bit before checking again
    delay(REFRESH_DELAY);
}
