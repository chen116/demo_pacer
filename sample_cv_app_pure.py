import imutils
import cv2
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time


vs= FileVideoStream("rollcar.3gp").start()
time.sleep(1)

while vs.more():
	frame = vs.read()
	frame = imutils.resize(frame, width=300)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)			
	net.setInput(blob)
	detections = net.forward()
	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > 0.5:
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			print('car')


