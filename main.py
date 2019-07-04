import argparse
import configparser
import os
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
    return parser.parse_args()

def strToBool(strValue):
    if strValue.lower() in STR_TRUE:
        return True
    elif strValue.lower() in STR_FALSE:
        return False
    else:
        raise TypeError


# check the configuration the program is being run with,
if __name__ == '__main__':
    args = parseCommandLine()
    lidar_used = None
    camera_used = None
    dev_mode = False

    # Check if we are using the config file or command line options
    if strToBool(args.CfgFile):
        try:
            cfg = configparser.ConfigParser()
            cfg_file_path = os.path.join(os.getcwd(), args.CfgPath)
            cfg.read(cfg_file_path)
            lidar_used = cfg[STR_LIDAR][STR_VALUE]
            camera_used = cfg[STR_CAMERA][STR_VALUE]
            dev_mode = strToBool(cfg[STR_DEV][STR_VALUE])
        except:
            raise custom_exceptions.Missing_Program_Parameters

    # We must grab the options manually
    else:
        try:
            # Determine type of lidar control
            lidar_used = args.Lidar
            camera_used = args.Camera
            dev_mode = strToBool(args.Dev)
        except:
            raise custom_exceptions.Missing_Program_Parameters

    # Check if we were given the correct parameters
    if (camera_used is STR_EMPTY) or (lidar_used is STR_EMPTY) or (dev_mode is None):
        raise custom_exceptions.Missing_Program_Parameters

    main_gui.run_gui(lidar=lidar_used, camera=camera_used, dev=dev_mode)
