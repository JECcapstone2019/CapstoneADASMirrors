from tools import custom_exceptions

class ClassFactory:
    def __init__(self, *args, **kwargs):
        self._custom_classes = {}

    # used to pass a dict and register all the known subclasses to a particular string
    # also normalize so capitalization doesn't matter
    def registerCustomClass(self, classesDict):
        for name, classMethod in classesDict:
            self._custom_classes[name] = classMethod.lower()

    # Used to create an instance of the correct subclass
    def create(self, customClassName, *args, **kwargs):
        try:
            return self._custom_classes[customClassName](*args, **kwargs)
        except KeyError:
            raise custom_exceptions.Sub_Class_Not_Found
        except Exception as e:
            raise e
