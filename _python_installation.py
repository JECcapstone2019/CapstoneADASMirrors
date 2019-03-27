# This file is for installing all of the python modules required using pip install
# This will create a virtual enviornment in the /virtenv directory

import os
import sys
import pip

FOLDER_PATH = os.getcwd()

OS_SUPPORTED = []
PYTHON_VERSION_REQUIRED = ""
PATH_TO_REQUIREMENTS = '_requirements.txt'
PATH_TO_INSTALL_LOG = 'install_log.txt'
PATH_TO_VIRTENV = "virtenv"

# Gives the list of required modules by passing it a text file
def getRequirementsList(path_to_requirements):
    list_requirements = []
    with open(path_to_requirements, 'r') as reqFile:
        pass
    return list_requirements

if __name__ == '__main__':
    install_success = True
    with open(os.path.join(FOLDER_PATH, PATH_TO_INSTALL_LOG), 'wb') as logFile:
        # first check if the OS is supported
        platform = sys.platform
        logFile.write("%s is supported %s\n" % (platform, str(OS_SUPPORTED)))
        if platform not in OS_SUPPORTED:
            install_success = False
            logFile.write("INSTALL FAILED - wrong OS\n")

        # Check if correct version of python
        version = sys.version
        logFile.write("Correct Version of Python used %s==%s\n" % (version, PYTHON_VERSION_REQUIRED))
        if version != PYTHON_VERSION_REQUIRED:
            install_success = False
            logFile.write("INSTALL FAILED - wrong Python version\n")

        # Check to see that we are using the virtual environment
        logFile.write("Using Correct Virtual Environment\n")
        if sys.excutable != os.path.join(FOLDER_PATH, PATH_TO_VIRTENV):
            install_success = False
            logFile.write("INSTALL FAILED - wrong Python %s\n" % sys.executable)

        # Check to see that all modules are installed correctly
        required_modules = getRequirementsList(os.path.join(FOLDER_PATH, PATH_TO_REQUIREMENTS))
        installed_packages = pip.get_installed_distributions()
        for module in required_modules:
            if module not in installed_packages:
                install_success = False
                logFile.write("INSTALL FAILED - Module Missing/Wrong Version %s\n" % module)
            else:
                logFile.write("Module Found: %s\n" % module)

        # All done, print a nice message
        if install_success:
            logFile.write("Wow! We did it! - Install Success")
        else:
            logFile.write("Something went wrong... Read the rest of this file - Install FAILED")
