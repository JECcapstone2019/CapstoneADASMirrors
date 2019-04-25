from datetime import datetime
import os


# Returns a nice formatted timestamp for using in filenames
def getTimeStampedString():
    now = datetime.now()
    time_stamp = "%i_%i_%i-%i_%i_%i" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return time_stamp

def createTimeStampedFolder(pathToFolder, str_Prefix='', str_Suffix=''):
    folder_name = '%s_%s_%s' % (str_Prefix, getTimeStampedString(), str_Suffix)
    path = os.path.join(pathToFolder, folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return path