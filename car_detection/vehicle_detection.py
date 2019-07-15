# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import re
print(cv2.__version__)

class VirtualStream:
    def __init__(self, numpyFolder):
        self.folder = numpyFolder
        self.np_images = {}
        for image in os.listdir(self.folder):
            if '.npy' in image:
                path = os.path.join(self.folder, image)
                self.np_images[int(re.search(r'\d+', image).group())] = path
        self.count = 200
        self.end = len(self.np_images) - 1
    
    def grabImage(self):
        image = np.load(self.np_images[self.count])
        self.count += 1
        if self.count >= self.end:
            self.reset()
        return image
    
    def reset(self):
        self.count = 0

cascade_src = 'cars.xml'

cap = VirtualStream('/Users/user/Desktop/saved_images_2019_6_13-17_49_52')
car_cascade = cv2.CascadeClassifier(cascade_src)

while True:
    img = cap.grabImage()
    if (type(img) == type(None)):
        break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cars = car_cascade.detectMultiScale(gray, 1.1, 2,0)

    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)      
    
    cv2.imshow('video', img)
    
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
