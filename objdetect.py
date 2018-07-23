from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

COLORS = np.random.uniform(0, 255, size=(1, 3))

a = [[20,220,84]]


# net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

aa=np.array(a)
print(COLORS)
print(aa)