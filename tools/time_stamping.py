from datetime import datetime


# Returns a nice formatted timestamp for using in filenames
def getTimeStampedString():
    now = datetime.now()
    time_stamp = "%i_%i_%i-%i_%i_%i" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return time_stamp
