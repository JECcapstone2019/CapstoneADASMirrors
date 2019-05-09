#include <Wire.h>
#include <String.h>

const int BAUD_RATE = 9600;
const int REFRESH_DELAY = 5; // in ms

// Communication with Python constants
const byte TERMINATOR = 0xa5;
const byte MSG_ACK = 0xf0;
const byte MSG_COMPLETED = 0x0f;
const byte MSG_ERROR = 0xaf;
const int MSG_SIZE = 4;

// Command Definitions
const byte CMD_READ_REG = 0x00;
const byte CMD_WRITE_REG = 0x01;

// Parse the message to see what it wants us to do
byte* parseMessage(byte message[MSG_SIZE]){
    byte cmd_id = message[0];
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
    byte message[MSG_SIZE];
    // Check if there is a full instruction set available
    if(Serial.available() == MSG_SIZE){
        // Received a full message - grab the data and send an ack
        Serial.readBytes(message, MSG_SIZE);
        if(message[MSG_SIZE - 1] != TERMINATOR){
            // Invalid termination, something is wrong with this message
            Serial.write(MSG_ERROR);
        }
        else{
            // Received a good message, now do what the message says and send the completed message
            Serial.write(MSG_ACK);
            byte *completed_msg = parseMessage(message);
            Serial.write(*completed_msg);
        }

    }
    // Check to see if we missed an instruction set - if more than one message lets discard and restart
    else if(Serial.available() > MSG_SIZE){
        emptySerialBuffer();
        serial.print(ERROR_MSG)
    }
    // Wait a bit before checking again
    delay(REFRESH_DELAY);



}
