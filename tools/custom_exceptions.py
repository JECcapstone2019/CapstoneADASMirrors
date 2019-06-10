# Miscellaneous ########################################################################################################
########################################################################################################################

class NonStringKey_RegisterMap(Exception):
    pass

class NonIntValue_RegisterMap(Exception):
    pass

class Read_Only_Register(Exception):
    pass

class Write_Only_Register(Exception):
    pass

class Bit_OverFlow(Exception):
    pass

class Negative_Bit_value(Exception):
    pass

class Missing_Program_Parameters(Exception):
    pass

# Camera ###############################################################################################################
########################################################################################################################

class Camera_Not_Connected(Exception):
    pass

class Stream_Not_Implemented(Exception):
    pass

class Unable_To_Configure_While_Camera_Running(Exception):
    pass

# Arduino Communication ################################################################################################
########################################################################################################################

class Packet_byte_Error(Exception):
    def __init__(self, byteReceived, byteDefault):
        self.byte_received = byteReceived
        self.byte_default = byteDefault
        # TODO: Add a custom message to this

class Packet_Header_Error(Packet_byte_Error):
    pass

class Packet_Footer_Error(Packet_byte_Error):
    pass

class Packet_Data_Error(Packet_byte_Error):
    pass

class Serial_Communication_Ack_Timeout(Exception):
    pass

class Serial_Communication_Completed_Timeout(Exception):
    pass

class Sequence_Count_Error(Exception):
    def __init__(self, countExpected, CountGiven):
        # TODO: Add a custom message for this
        pass
