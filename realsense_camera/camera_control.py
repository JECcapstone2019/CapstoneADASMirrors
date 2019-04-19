import pyrealsense2 as rs

class RealsenseCameraControl():
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

class RealsenseCamera(RealsenseCameraControl):
    def __init__(self):
        RealsenseCameraControl.__init__(self)

        # Connection Values
        self.pipe = None
        self.profile = None

    def connect(self):
        self.pipe = rs.pipeline()
        self.profile = self.pipe.start()

    def disconnect(self):
        self.pipe.stop()
        self.pipe = None
        self.profile = None


pipe = rs.pipeline()
profile = pipe.start()
try:
  for i in range(0, 100):
    frames = pipe.wait_for_frames()
    for f in frames:
      print(f.profile)
finally:
    pipe.stop()