from tools import custom_exceptions

class ClassFactory:
    _custom_classes = {}

    # used to pass a dict and register all the known subclasses to a particular string
    # also normalize so capitalization doesn't matter
    def registerCustomClass(self, classesDict):
        for name, classMethod in classesDict.items():
            self._custom_classes[name.lower()] = classMethod

    # Used to create an instance of the correct subclass
    def create(self, customClassName, *args, **kwargs):
        try:
            return self._custom_classes[customClassName.lower()](*args, **kwargs)
        except KeyError:
            raise custom_exceptions.Sub_Class_Not_Found
        except Exception as e:
            raise e
