from tools import custom_exceptions
import random

class RegisterMap(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        if type(key) != str:
            raise custom_exceptions.NonStringKey_RegisterMap
        if type(value) != int:
            raise custom_exceptions.NonIntValue_RegisterMap
        else:
            dict.__setitem__(self, key, value)
            dict.__setitem__(self, value, key)


# Same as RegisterMap but sets a random value instead of key errors
class VirtualRegisterMap(RegisterMap):
    def __init__(self, value_bits):
        RegisterMap.__init__(self)
        self.max_value = pow(2, value_bits) - 1

    def __getitem__(self, item):
        try:
            return RegisterMap.__getitem__(self, item)
        except KeyError:
            value = random.randint(0, self.max_value)
            self.__setitem__(item, value)
            return value



class BitRegisterMap(dict):
    def __init__(self, address_bits, data_bits, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.address_max = pow(2, address_bits) - 1
        self.data_max = pow(2, data_bits) - 1

    def __setitem__(self, key, value):
        if type(key) != int:
            raise custom_exceptions.NonIntValue_RegisterMap
        if type(value) != int:
            raise custom_exceptions.NonIntValue_RegisterMap
        else:
            self._checkAddress(address=key)
            self._checkValue(value=value)
            dict.__setitem__(self, key, value)

    def _checkAddress(self, address):
        if address > self.address_max:
            raise custom_exceptions.Bit_OverFlow
        if address < 0:
            raise custom_exceptions.Negative_Bit_value

    def _checkValue(self, value):
        if value > self.address_max:
            raise custom_exceptions.Bit_OverFlow
        if value < 0:
            raise custom_exceptions.Negative_Bit_value