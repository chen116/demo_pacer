from pyxs import Client
import subprocess
import copy
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import sys

# # construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
ap.add_argument("-w", "--width", type=int, default=500, help="im show width")
args = vars(ap.parse_args())


# load video and create video 
vs= FileVideoStream("rollcar.3gp").start()
time.sleep(1.0)
car = np.zeros((30,144,176,3),dtype=np.uint8)
no_car = np.zeros((60,144,176,3),dtype=np.uint8)
for i in range(200):
    frame = vs.read()
    if i >= 20 and i < 50:
    	car[i-20,:,:,:]=frame
    elif i >= 140:
        no_car[i-140,:,:,:]=frame
vs.stop()   
car = np.concatenate((car, np.flipud(car)), axis=0)



# create heartbeat
import heartbeat
window_size_hr=5
sharedmem_id_for_heartbeat = 1024
buffer_depth = 100
log_name = "heartbeat.log"
min_heart_rate = 10 # not used in this demo
max_heart_rate = 100 # not used in this demo
hb = heartbeat.Heartbeat(sharedmem_id_for_heartbeat,window_size_hr,buffer_depth,log_name,min_heart_rate,max_heart_rate)

# establish communication with Dom0
import domU_comm
monitoring_items = ["heart_rate","frame_size"]
comm = domU_comm.DomU(monitoring_items)

# prepare object detation neural network
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")



with Client(xen_bus_path="/dev/xen/xenbus") as c:
	# synching with Dom0 with xenstore
	domu_id = c.read("domid".encode())
	key_path_hash_frame_number_entry=('/local/domain/'+domu_id.decode()+'/frame_number_entry').encode()
	key_path_hash_box_entry=('/local/domain/'+domu_id.decode()+'/box_entry').encode()
	print("Dom", domu_id.decode(), "waiting for Dom0...")
	while c.read(key_path_hash_frame_number_entry).decode() != "init":
		continue
	init_video_data_string = ""
	while len(init_video_data_string.split()) == 0 or init_video_data_string.split()[0] != "init":
		init_video_data_string = c.read(key_path_hash_box_entry).decode()
	# setup video sequence and frame sizes from Dom0
	init_video_data_list = init_video_data_string.split()
	heavy_workload_frame_size = int(init_video_data_list[1])
	light_workload_frame_size = int(init_video_data_list[2])
	vidarray_binary = list(map(int, init_video_data_list[3].split(',')))
	vidarray = np.zeros((1,144,176,3),dtype=np.uint8)
	for binary in vidarray_binary:
		if binary:
			vidarray = np.concatenate((vidarray,car),axis=0)
		else:
			vidarray = np.concatenate((vidarray,no_car),axis=0)
	vidarray = np.delete(vidarray, 0, 0)
	(startX, startY, endX, endY)=(0,0,0,0) 
	c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())
	c.write(key_path_hash_frame_number_entry,('ready').encode())
	print("Dom", domu_id.decode(), "synched with Dom0...")

	
	frame_number_entry = "init"
	prev_frame_num = -1
	frame_size = vidarray_binary[0]
	detect_car = vidarray_binary[0]
	prev_frame_size = 0
	
	cntt=-1
	# get frame numbers from dom0 to run object detection
	firstFrame = None
	while frame_number_entry != "done":
		frame_number_entry = c.read(key_path_hash_frame_number_entry).decode()
		try:
			frame_num = int(frame_number_entry)
		except:
			frame_num = -1
		if frame_num > -1 and frame_num > prev_frame_num:
			frame = vidarray[frame_num]
			if detect_car == 1:
				frame_size = 1000#heavy_workload_frame_size
			else:
				frame_size = 1000#light_workload_frame_size
			frame = imutils.resize(frame, width=1000)#frame_size
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			if firstFrame is None:
				firstFrame = gray
				continue
			frameDelta = cv2.absdiff(firstFrame, gray)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			contours = contours[0] if imutils.is_cv2() else contours[1]
			# loop over the contours
			(startX, startY, endX, endY)=(0,0,0,0) 
			for contour in contours:
				# if the contour is too small, ignore it
				if cv2.contourArea(contour) > args["min_area"]:
					(startX, startY, endX, endY)= cv2.boundingRect(contour)

			if sum((startX, startY, endX, endY)) > 0 :
				detect_car = 1
			else:
				detect_car = 0
			c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())

			# record a heartbeat
			hb.heartbeat_beat()
			cntt+=1
			# send heartrate to Pacer monitor in Dom0
			comm.write("heart_rate", hb.get_instant_heartrate())
			# send change of framze sixe to Pacer monitor in Dom0
			if prev_frame_size != frame_size:
				prev_frame_size = frame_size
				comm.write("frame_size",frame_size)
			prev_frame_num = frame_num





hb.heartbeat_finish()
comm.write("heart_rate", "done")
print("done")



