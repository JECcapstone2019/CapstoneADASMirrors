import argparse
from tools import custom_exceptions

# Grab the command line options given by the user
def parseCommandLine():
    parser = argparse.ArgumentParser(description='Determine Program Run Options')
    parser.add_argument('CfgFile')
    parser.add_argument('-CfgPath')
    parser.add_argument('-Lidar')
    parser.add_argument('-Camera')
    parser.add_argument('-Dev')
    return parser

# Parse the config file for the options needed
def parseConfigFile(pathToFile):
    pass

if __name__ == '__main__':
    parser = parseCommandLine()
    lidar_used = None
    camera_used = None
    dev_mode = False

    # Check if we are using the config file or command line options
    if parser.CFGFile:
        parseConfigFile(pathToFile=parser.CFGPath)

    # We must grab the options manually
    else:
        # Determine type of lidar control
        if parser.Lidar is "VLidar":
            lidar_used
        elif parser.Lidar is "RLidar":
            lidar_used
        elif parser.Lidar is "ALidar":
            lidar_used

        # Determine type of camera control
        if parser.Camera is "VCamera":
            camera_used
        elif parser.Camera is "RCamera":
            camera_used
        if parser.Dev:
            dev_mode = True

    # Check if we were given the correct parameters
    if (camera_used is None) or (lidar_used is None):
        raise custom_exceptions.Missing_Program_Parameters