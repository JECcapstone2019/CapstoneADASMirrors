from tools import custom_exceptions

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
