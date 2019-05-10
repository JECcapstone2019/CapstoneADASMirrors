#include <Wire.h>
#include <String.h>

const int BAUD_RATE = 9600;
const int REFRESH_DELAY = 5; // in ms
const int TIMEOUT = 50; // in ms
const int MSG_READY = 3 // This will contain the msg header, cmdID, and size

// Communication with Python constants
const byte MSG_HEADER = 0x7f
const byte MSG_FOOTER = 0xa5;

const int MSG_HEADER_IND = 0;
const int MSG_CMD_IND = 1;
const int MSG_SIZE_IND = 2;

const byte MSG_ACK = 0xf0;
const byte MSG_COMPLETED = 0x0f;
const byte MSG_ERROR = 0xaf;

// Command Definitions
const byte CMD_READ_REG = 0x00;
const byte CMD_WRITE_REG = 0x01;

// Parse the message to see what it wants us to do
byte* parseMessage(int cmd_id, byte *message_data){
    byte *completed_msg;
    if(cmd_id == CMD_READ_REG){
    }
    else if(cmd_id == CMD_WRITE_REG){
    }
    else{
        // Unrecognized Command ID - Return Error
        completed_msg = &MSG_ERROR;
    }
    return completed_msg;
}

void emptySerialBuffer(){
    // Read until no more bytes in the buffer
    while (Serial.read() >= 0);
}

void setup() {
    Wire.begin();
    Serial.begin(BAUD_RATE);
}

void loop() {
    byte *message;
    // Check if there is a full instruction set available
    int bytes_available = Serial.available()
    if(bytes_available >= MSG_READY){
        // Received a message - lets check its parameters and see what we need
        Serial.readBytes(message, MSG_READY);
        if(message[MSG_HEADER_IND] != MSG_HEADER){
            // Invalid termination, something is wrong with this message
            Serial.write(MSG_ERROR);
            // Clear the buffer
            emptySerialBuffer();
        }
        else{
            // Check how many bytes we need for a full message
            byte *message_data;
            int msg_size = message[MSG_SIZE_IND];
            // Timeout at 50ms
            for(int delay_wait = 0; delay_wait < (TIMEOUT/REFRESH_DELAY); delay_wait++;){
                // check if we have the full message now
                bytes_available = Serial.available();
                if(bytes_available == msg_size){
                    Serial.readBytes(message_data, bytes_available);
                    int cmd_id = (int) message[MSG_CMD_IND];
                    Serial.write(MSG_ACK);
                    byte *completed_msg = parseMessage(cmd_id, message_data);
                    Serial.write(*completed_msg);
                    break;
                    }
                // Don't have full message yet, wait until timeout
                else{
                    delay(REFRESH_DELAY);
                }
            }
            // Clear the buffer
            emptySerialBuffer();
        }
    }
    // Wait a bit before checking again
    delay(REFRESH_DELAY);
}
