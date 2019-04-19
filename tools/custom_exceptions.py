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