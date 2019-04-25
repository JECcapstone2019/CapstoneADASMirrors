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

class Camera_Not_Connected(Exception):
    pass

class Stream_Not_Implemented(Exception):
    pass