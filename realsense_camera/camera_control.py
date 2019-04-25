import pyrealsense2 as rs
import numpy as np
from tools import custom_exceptions

class RealsenseCameraControl:
    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        raise NotImplementedError

    def getFrame(self, *args, **kwargs):
        raise NotImplementedError

class VirtualRealsenseCamera(RealsenseCameraControl):
    pass

class D435RealSenseCamera(RealsenseCameraControl):

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
        self.pipe.stop()
        self.running = False

    def disconnect(self):
        self.stop()
        self.pipe = None
        self.profile = None
        self.config = None

    def addStream(self, str_type):
        if self.connected and not self.running:
            stream_type = self.STREAMS[str_type][self.TYPE]
            stream_format = self.STREAMS[str_type][self.FORMAT]
            if str_type in self.STREAMS:
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


if __name__ == '__main__':
    # pipe = rs.pipeline()
    # profile = pipe.start()
    # try:
    #   for i in range(0, 100):
    #     frames = pipe.wait_for_frames()
    #     for f in frames:
    #       print(f.profile)
    # finally:
    #     pipe.stop()
    pass
