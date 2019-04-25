import numpy as np
import cv2
import os


def grabNumpyImagesFromFolder(folderPath):
    np_images = {}
    for image in os.listdir(folderPath):
        path = os.path.join(folderPath, image)
        np_images[image.strip('.npy')] = np.load(path)
    return np_images

# Quick function to view color numpy images
def viewNumpyColorImage(np_image, wait=True):
    cv2.imshow('RGB', np_image)
    if wait:
        cv2.waitKey()

def saveNumpyAsJpeg(np_image, filePath):
    pass

def loadJPEGAsNumpy(filePath):
    pass