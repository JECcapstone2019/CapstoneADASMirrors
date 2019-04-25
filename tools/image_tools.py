import numpy as np
import cv2
import os

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

def saveNumpyAsJpeg(np_image, filePath):
    raise NotImplementedError

def loadJPEGAsNumpy(filePath):
    raise NotImplementedError