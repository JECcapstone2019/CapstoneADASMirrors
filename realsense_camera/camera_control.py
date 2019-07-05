import pyrealsense2 as rs
import numpy as np
from tools import custom_exceptions, time_stamping, class_factory
import time
import os
import cv2

D435_SERIAL_NUM = 831612073489

DEPTH = 'DEPTH'
COLOR = 'COLOR'
INFRARED = 'INFRARED'

TYPE = 0
FORMAT = 1

STREAMS = {}
STREAMS[DEPTH] = {}
STREAMS[DEPTH][TYPE] = rs.stream.depth
STREAMS[DEPTH][FORMAT] = rs.format.z16
STREAMS[COLOR] = {}
STREAMS[COLOR][TYPE] = rs.stream.color
STREAMS[COLOR][FORMAT] = rs.format.bgr8
STREAMS[INFRARED] = {}
STREAMS[INFRARED][TYPE] = rs.stream.infrared
STREAMS[INFRARED][FORMAT] = rs.format.y8

class RealsenseCameraControl:
    def __init__(self, tup_frameSize, i_frameRate, *args, **kwargs):
        # Input Parameters
        self.frame_size = tup_frameSize
        self.frame_rate = i_frameRate

        # Connection Flags
        self.connected = False
        self.running = False

        # Streams
        self.stream_count = 0

    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        raise NotImplementedError

    def start(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self, *args, **kwargs):
        raise NotImplementedError

    def addColorStream(self, *args, **kwargs):
        self._addStream(str_type=COLOR)

    def addDepthStream(self, *args, **kwargs):
        self._addStream(str_type=DEPTH)

    def addInfraredStream(self, *args, **kwargs):
        self._addStream(str_type=INFRARED)

    def getFrames(self, *args, **kwargs):
        raise NotImplementedError

    def addCustomStream(self, *args, **kwargs):
        raise NotImplementedError

    def _addStream(self, str_type, *args, **kwargs):
        if self.connected and not self.running:
            stream_type = STREAMS[str_type][TYPE]
            stream_format = STREAMS[str_type][FORMAT]
            if str_type in STREAMS:
                self._ovr_addStream(streamType=stream_type, streamFormat=stream_format)
                self.stream_count += 1
            else:
                raise custom_exceptions.Stream_Not_Implemented
        elif self.running:
            raise custom_exceptions.Unable_To_Configure_While_Camera_Running
        else:
            raise custom_exceptions.Camera_Not_Connected

    def _ovr_addStream(self, streamType, streamFormat):
        raise NotImplementedError


class VirtualRealsenseCamera(RealsenseCameraControl):
    def __init__(self, tup_frameSize, i_frameRate):
        RealsenseCameraControl.__init__(self, tup_frameSize, i_frameRate)

        # Connection Values
        self.pipe = None
        self.profile = None
        self.config = None

        # Streams
        self.stream_count = 0

    def connect(self):
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.connected = True

    def start(self):
        self.pipe.start(self.config)
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
        self.stream_count = 0

    def addColorStream(self):
        self._addStream(str_type=COLOR)

    def addDepthStream(self):
        self._addStream(str_type=DEPTH)

    def addInfraredStream(self):
        self._addStream(str_type=INFRARED)

    def addCustomStream(self, streamType, tup_frameSize, streamFormat, i_frameRate):
        if self.connected and not self.running:
            self.config.enable_stream(streamType, *tup_frameSize, streamFormat, i_frameRate)
        elif self.running:
            raise custom_exceptions.Unable_To_Configure_While_Camera_Running
        else:
            raise custom_exceptions.Camera_Not_Connected

    def getFrames(self):
        return self.pipe.wait_for_frames()


class D435RealSenseCamera(RealsenseCameraControl):
    def __init__(self, tup_frameSize, i_frameRate):
        RealsenseCameraControl.__init__(self, tup_frameSize, i_frameRate)

        # Input Parameters
        self.frame_size = tup_frameSize
        self.frame_rate = i_frameRate

        # Connection Values
        self.pipe = None
        self.profile = None
        self.config = None

        #connection Flags
        self.running = False
        self.connected = False

    def connect(self):
        self.pipe = rs.pipeline()
        self.config = rs.config()
        self.connected = True

    def start(self):
        self.pipe.start(self.config)
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
        self.stream_count = 0

    def addCustomStream(self, streamType, tup_frameSize, streamFormat, i_frameRate):
        if self.connected and not self.running:
            self.config.enable_stream(streamType, *tup_frameSize, streamFormat, i_frameRate)
        elif self.running:
            raise custom_exceptions.Unable_To_Configure_While_Camera_Running
        else:
            raise custom_exceptions.Camera_Not_Connected

    def getFrames(self):
        return self.pipe.wait_for_frames()

    def _ovr_addStream(self, streamType, streamFormat):
        self.config.enable_stream(streamType, self.stream_count, *self.frame_size, streamFormat, self.frame_rate)


CAMERA_CLASSES = {}
CAMERA_CLASSES['VCAMERA'] = VirtualRealsenseCamera
CAMERA_CLASSES['CAMERA'] = D435RealSenseCamera

class CameraFactory(class_factory.ClassFactory):
    def __init__(self):
        self.registerCustomClass(CAMERA_CLASSES)

# Quick function to grab some images and save them as numpies
def saveXImages(xImages, folderPath='', rate=1.0):
    path = folderPath
    if path is '':
        path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='saved_images')
    camera = D435RealSenseCamera((640, 480), 30)
    camera.disconnect()
    camera.connect()
    camera.addColorStream()
    camera.start()
    for image in range(xImages):
        time.sleep(1/rate)
        frames = camera.getFrames()
        color_frame = frames.get_color_frame()
        np_color_image = np.asanyarray(color_frame.get_data())
        image_path = os.path.join(path, time_stamping.getTimeStampedString() + '_image.npy')
        np.save(image_path, np_color_image)
    camera.disconnect()
    return path

# Quick Viewing function
def quickViewer(save=False):
    camera = D435RealSenseCamera((640, 480), 30)
    camera.disconnect()
    camera.connect()
    camera.addColorStream()
    camera.start()
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    if save:
        path = time_stamping.createTimeStampedFolder(pathToFolder=os.getcwd(), str_Prefix='saved_images')
    count = 0
    for i in range(30*5):
        frames = camera.getFrames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            print("image not found")
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        if save:
            image_path = os.path.join(path, 'image_%i.npy' % count)
            np.save(image_path, color_image)
            print("Save")
            count += 1

        # Show images
        cv2.imshow('RealSense', color_image)
        cv2.waitKey(33)



if __name__ == '__main__':
    # camera = D435RealSenseCamera((480, 640), 30)
    # camera.disconnect()
    # camera.connect()
    # camera.start()
    # frame = camera.getFrames()
    # camera.disconnect()
    # color_frame = frame.get_color_frame()
    # np_color_image = np.asanyarray(color_frame.get_data())
    # time.sleep(1)
    # test = rs.context.devices
    ##########33
    # saveXImages(30, rate=15.0)
    quickViewer()
