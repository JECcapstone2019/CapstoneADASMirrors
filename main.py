import argparse
import configparser
from tools import custom_exceptions
from gui import main_gui

STR_LIDAR = 'LIDAR'
STR_CAMERA = 'CAMERA'
STR_DEV = 'DEV'
STR_VALUE = 'VALUE'

STR_EMPTY = ''

STR_TRUE = ['true', 'yes', 'y']
STR_FALSE = ['false', 'no', 'n']

# Grab the command line options given by the user
def parseCommandLine():
    parser = argparse.ArgumentParser(description='Determine Program Run Options')
    parser.add_argument('CfgFile')
    parser.add_argument('-CfgPath')
    parser.add_argument('-Lidar')
    parser.add_argument('-Camera')
    parser.add_argument('-Dev')
    return parser

def strToBool(strValue):
    if strValue.lower() in STR_TRUE:
        return True
    elif strValue.lower() in STR_FALSE:
        return False
    else:
        raise TypeError


# check the configuration the program is being run with,
if __name__ == '__main__':
    parser = parseCommandLine()
    lidar_used = None
    camera_used = None
    dev_mode = False

    # Check if we are using the config file or command line options
    if strToBool(parser.CFGFile):
        try:
            cfg = configparser.ConfigParser()
            cfg_data = cfg.read(parser.CfgPath)
            lidar_used = cfg_data[STR_LIDAR][STR_VALUE]
            camera_used = cfg_data[STR_CAMERA][STR_VALUE]
            dev_mode = strToBool(cfg_data[STR_DEV][STR_VALUE])
        except:
            raise custom_exceptions.Missing_Program_Parameters

    # We must grab the options manually
    else:
        try:
            # Determine type of lidar control
            lidar_used = parser.Lidar
            camera_used = parser.Camera
            dev_mode = strToBool(parser.Dev)
        except:
            raise custom_exceptions.Missing_Program_Parameters

    # Check if we were given the correct parameters
    if (camera_used is STR_EMPTY) or (lidar_used is STR_EMPTY) or (dev_mode is None):
        raise custom_exceptions.Missing_Program_Parameters

    main_gui.run_gui(lidar=lidar_used, camera=camera_used, dev=dev_mode)
