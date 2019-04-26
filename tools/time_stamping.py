from datetime import datetime
import os


# Returns a nice formatted timestamp for using in filenames
def getTimeStampedString():
    now = datetime.now()
    time_stamp = "%i_%i_%i-%i_%i_%i" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return time_stamp

# Easy method for creating a time stamped folder somewhere - will not overwrite previous folders
def createTimeStampedFolder(pathToFolder, str_Prefix='', str_Suffix=''):
    folder_name = ''
    if not(str_Prefix is ''):
        folder_name = '%s_' % (str_Prefix)
    folder_name += getTimeStampedString()
    if not(str_Suffix is ''):
        folder_name += '_%s' % str_Suffix
    path = os.path.join(pathToFolder, folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path