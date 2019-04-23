# This file is for installing all of the python modules required using pip install

import os
import sys
import platform
import pkg_resources
from tools import time_stamping

# Grab the path to this file, minus the file name itself
FOLDER_PATH = os.path.split(os.path.realpath(__file__))[0]

OS_SUPPORTED = ['win32', 'win64']
PYTHON_VERSION_REQUIRED = "3.6.8"
PATH_TO_REQUIREMENTS = '_requirements.txt'
INSTALL_LOG_FOLDER = 'install_logs'
PATH_TO_INSTALL_LOG = 'install_log'
LOG_FILE_TYPE = '.txt'
PATH_TO_VIRTENV = "virtenv\Scripts\python.exe"

# Gives the list of required modules by passing it a text file
def getRequirementsList(pathToRequirements):
    list_requirements = []
    with open(pathToRequirements, 'r') as reqFile:
        list_requirements = reqFile.readlines()
    list_requirements = [req.rstrip('\n') for req in list_requirements]
    return list_requirements

def getInstalledPackages():
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    formatted_package_list = []
    for package in installed_packages:
        formatted_package_list.append("%s==%s" % (package[0], package[1]))
    return formatted_package_list


if __name__ == '__main__':
    install_success = True
    log_folder_path = os.path.join(FOLDER_PATH, INSTALL_LOG_FOLDER)
    log_file_path = "%s_%s_%s" % (PATH_TO_INSTALL_LOG, time_stamping.getTimeStampedString(), LOG_FILE_TYPE)
    if not os.path.exists(log_folder_path):
        os.mkdir(log_folder_path)
    with open(os.path.join(log_folder_path, log_file_path), 'w') as logFile:
        # first check if the OS is supported
        os_type = sys.platform
        logFile.write("%s is supported %s\n" % (os_type, str(OS_SUPPORTED)))
        if os_type not in OS_SUPPORTED:
            install_success = False
            logFile.write("INSTALL FAILED - wrong OS\n")

        # Check if correct version of python
        version = platform.python_version()
        logFile.write("Correct Version of Python used %s==%s\n" % (version, PYTHON_VERSION_REQUIRED))
        if version != PYTHON_VERSION_REQUIRED:
            install_success = False
            logFile.write("INSTALL FAILED - wrong Python version\n")

        # Check to see that we are using the virtual environment
        logFile.write("Using Correct Virtual Environment\n")
        if sys.executable != os.path.join(FOLDER_PATH, PATH_TO_VIRTENV):
            install_success = False
            logFile.write("INSTALL FAILED - wrong Python %s\n" % sys.executable)

        # Check to see that all modules are installed correctly
        required_modules = getRequirementsList(os.path.join(FOLDER_PATH, PATH_TO_REQUIREMENTS))
        installed_packages = getInstalledPackages()
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
            logFile.write("Something went wrong... Read the rest of this file\nInstall FAILED")
