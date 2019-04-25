import pyrealsense2 as rs
import numpy as np
from tools import custom_exceptions, time_stamping, image_tools
import time
import os


DEPTH = 'DEPTH'
COLOUR = 'COLOUR'
INFRARED = 'INFRARED'

TYPE = 0
FORMAT = 1

STREAMS = {}
STREAMS[DEPTH] = {}
STREAMS[DEPTH][TYPE] = rs.stream.depth
STREAMS[DEPTH][FORMAT] = rs.format.z16
STREAMS[COLOUR] = {}
STREAMS[COLOUR][TYPE] = rs.stream.color
STREAMS[COLOUR][FORMAT] = rs.format.bgr8
STREAMS[INFRARED] = {}
STREAMS[INFRARED][TYPE] = rs.stream.infrared
STREAMS[INFRARED][FORMAT] = rs.format.y8

class RealsenseCameraControl:
    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        raise NotImplementedError

    def getFrames(self, *args, **kwargs):
        raise NotImplementedError

class VirtualRealsenseCamera(RealsenseCameraControl):
    pass

class D435RealSenseCamera(RealsenseCameraControl):
    def __init__(self, tup_frameSize, i_frameRate):
        RealsenseCameraControl.__init__(self)

        # Connection Values
        self.pipe = None
        self.profile = None
        self.config = None
        self.connected = False
        self.frame_size = tup_frameSize
        self.frame_rate = i_frameRate
        self.running = False

        # Streams
        self.s_depth = None
        self.s_colour = None
        self.s_infrared = None

    def connect(self):
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.connected = True

    def start(self):
        self.pipe.start()
        self.running = True

    def stop(self):
        if self.pipe != None:
            self.pipe.stop()
        self.running = False

    def disconnect(self):
        self.stop()
        self.pipe = None
        self.profile = None
        self.config = None

    def addStream(self, str_type):
        if self.connected and not self.running:
            stream_type = STREAMS[str_type][TYPE]
            stream_format = STREAMS[str_type][FORMAT]
            if str_type in STREAMS:
                self.config.enable_stream(stream_type, *self.frame_size, stream_format, self.frame_rate)
            else:
                raise custom_exceptions.Stream_Not_Implemented
        else:
            raise custom_exceptions.Camera_Not_Connected

    def _addCustomStream(self, streamType, tup_frameSize, streamFormat, i_frameRate):
        if self.connected and not self.running:
            self.config.enable_stream(streamType, *tup_frameSize, streamFormat, i_frameRate)
        else:
            raise custom_exceptions.Camera_Not_Connected

    def getFrames(self):
        return self.pipe.wait_for_frames()

    def getArrFrames(self):
        frames = self.pipe.wait_for_frames()
        arr_frames = []
        for frame in frames:
            arr_frames.append(frame)
        return arr_frames

# Quick function to grab some images and save them as numpies
def saveXImages(xImages, folderPath=''):
    path = folderPath
    if path is '':
        path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='saved_images')
    camera = D435RealSenseCamera((480, 640), 30)
    camera.disconnect()
    camera.connect()
    camera.addStream(str_type=COLOUR)
    camera.start()
    for image in range(xImages):
        time.sleep(1)
        frames = camera.getArrFrames()
        for frame in frames:
            color_frame = frame.get_color_frame()
            np_color_image = np.asanyarray(color_frame.get_data())
            image_path = os.path.join(path, time_stamping.getTimeStampedString() + '_image.npy')
            np.save(image_path, np_color_image)
    camera.disconnect()
    return path

def quickViewer():
    camera = D435RealSenseCamera((480, 640), 30)
    camera.disconnect()
    camera.connect()
    camera.addStream(str_type=COLOUR)
    camera.start()
    try:
        while(True):
            frames = camera.getFrames()
            colour_images = frames.get_color_frame()
            np_color_image = np.asanyarray(colour_images.get_data())
            image_tools.viewNumpyColorImage(np_color_image)
    except KeyboardInterrupt:
        camera.disconnect()
        return



if __name__ == '__main__':
    camera = D435RealSenseCamera((480, 640), 30)
    camera.disconnect()
    camera.connect()
    camera.addStream(str_type=COLOUR)
    camera.start()
    frame = camera.getFrames()
    camera.disconnect()
    color_frame = frame.get_color_frame()
    np_color_image = np.asanyarray(color_frame.get_data())
    time.sleep(1)
