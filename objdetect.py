from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())


# COLORS=np.array([[5,200,250]])
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


vs = FileVideoStream("walkman.mp4").start()

time.sleep(1.0)



vid_len = 150
vidarray = np.zeros((vid_len,360,640,3),dtype=np.uint8)
vs= FileVideoStream(args["video"]).start()
time.sleep(1.0)
for i in range(vid_len):
    frame = vs.read()
    vidarray[i,:,:,:]=frame
vs.stop()   


for frame in vidarray:

# while vs.more():
	timer = cv2.getTickCount()
	# frame = vs.read()
	frame = imutils.resize(frame, width=300)
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
	net.setInput(blob)
	detections = net.forward()
	for i in np.arange(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		idx2 = int(detections[0,0,i,1])

		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		label = "{}: {:.2f}%".format(CLASSES[idx],
			confidence * 100)
		cv2.rectangle(frame, (startX, startY), (endX, endY),
			COLORS[idx], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(frame, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	cv2.imshow("Frame", frame)
	print(cv2.getTickFrequency() / (cv2.getTickCount() - timer))
	key = cv2.waitKey(1) & 0xFF
vs.stop() #if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
