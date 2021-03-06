import numpy as np
import cv2
import os
import re

# returns a dict of filename - .npy as the keys to the images
def grabNumpyImagesFromFolder(folderPath):
    np_images = {}
    for image in os.listdir(folderPath):
        if '.npy' in image:
            path = os.path.join(folderPath, image)
            np_images[image.strip('.npy')] = np.load(path)
    return np_images


# Quick function to view color numpy images
def viewNumpyColorImage(np_image, wait=True):
    cv2.imshow('RGB', np_image)
    if wait:
        cv2.waitKey()


def viewNumpyImageFolder(folderPath):
    images = grabNumpyImagesFromFolder(folderPath=folderPath)
    for image in images:
        viewNumpyColorImage(np_image=images[image])


def colorImage(np_image):
    if len(np_image.shape) == 3:
        return True
    else:
        return False


class VirtualStream:
    def __init__(self, numpyFolder):
        self.folder = numpyFolder
        self.np_images = {}
        for image in os.listdir(self.folder):
            if '.npy' in image:
                path = os.path.join(self.folder, image)
                self.np_images[int(re.search(r'\d+', image).group())] = path
        self.count = 0
        self.end = len(self.np_images) - 1

    def grabImage(self):
        image = np.load(self.np_images[self.count])
        self.count += 1
        if self.count >= self.end:
            self.reset()
        return image

    def reset(self):
        self.count = 0


def saveNumpyAsJpeg(np_image, filePath):
    cv2.imwrite(filePath, np_image)


def loadJPEGAsNumpy(filePath):
    raise NotImplementedError


def createNumpyColorImagePattern(tup_frameSize, i_bitsPerPixel=255, seed=0):
    w = tup_frameSize[0]
    h = tup_frameSize[1]
    oned = (np.arange(seed, w*h + seed) & i_bitsPerPixel) / float(i_bitsPerPixel)
    oned = np.reshape(oned, tup_frameSize)
    return np.dstack((oned, oned, oned))


def createNumpyColorImagePatternDict(i_numImages, tup_frameSize, i_bitsPerPixel=255):
    image_dict = {}
    for i in range(i_numImages):
        image_dict[i] = createNumpyColorImagePattern(tup_frameSize=tup_frameSize, i_bitsPerPixel=i_bitsPerPixel, seed=i)
    return image_dict
