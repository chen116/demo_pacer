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




ap = argparse.ArgumentParser()
ap.add_argument("-w", "--window", type=int, default=2, help="window size")
args = vars(ap.parse_args())


vs= FileVideoStream("rollcar.3gp").start()
time.sleep(1.0)
car = np.zeros((30,144,176,3),dtype=np.uint8)
blank = np.zeros((60,144,176,3),dtype=np.uint8)
for i in range(200):#blank_len+car_len):
    frame = vs.read()
    if i >= 20 and i < 50:
    	car[i-20,:,:,:]=frame
    elif i >= 140:
        blank[i-140,:,:,:]=frame
vs.stop()   

car = np.concatenate((car, np.flipud(car)), axis=0)
vidarray_binary = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1]
vidarray = np.zeros((1,144,176,3),dtype=np.uint8)
for binary in vidarray_binary:
	if binary:
		vidarray = np.concatenate((vidarray,car),axis=0)
	else:
		vidarray = np.concatenate((vidarray,blank),axis=0)
vidarray = np.delete(vidarray, 0, 0)

net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")


import heartbeat
import host_guest_comm

window_size_hr=5#
hb = heartbeat.Heartbeat(1024,window_size_hr,100,"vic.log",10,100)
monitoring_items = ["heart_rate","sampling_period"]
comm = host_guest_comm.DomU(monitoring_items)
with Client(xen_bus_path="/dev/xen/xenbus") as c:
	domu_id = c.read("domid".encode())
	key_path_hash_frame_number_entry=('/local/domain/'+domu_id.decode()+'/frame_number_entry').encode()
	key_path_hash_box_entry=('/local/domain/'+domu_id.decode()+'/box_entry').encode()
	print("Dom", domu_id.decode(), "waiting for dom0...")
	while c.read(key_path_hash_frame_number_entry).decode() != "init":
		continue
	(startX, startY, endX, endY)=(0,0,0,0) 
	c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())
	c.write(key_path_hash_frame_number_entry,('ready').encode())
	frame_number_entry = "init"
	prev_frame = -1
	self_cnt = 0
	sampling_period = int(window_size_hr/2)
	detect_car = 1
	prev_detect_car = detect_car
	prev_sampling_period = sampling_period
	print("Dom", domu_id.decode(), "start...")
	while frame_number_entry != "done":
		frame_number_entry = c.read(key_path_hash_frame_number_entry).decode()
		try:
			frame_num = int(frame_number_entry)
		except:
			frame_num = -1
		if frame_num > -1 and frame_num>prev_frame:
			frame = vidarray[frame_num]
			if detect_car == 1:
				frame_size = 300
			else:
				frame_size = int(300/2)
			frame = imutils.resize(frame, width=frame_size)

			(startX, startY, endX, endY)=(0,0,0,0) 
			if True:
				(startX, startY, endX, endY)=(0,0,0,0) 
				(h, w) = frame.shape[:2]
				blob = cv2.dnn.blobFromImage(cv2.resize(frame, (frame_size, frame_size)),0.007843, (frame_size, frame_size), 127.5)			
				net.setInput(blob)
				detections = net.forward()
				for i in np.arange(0, detections.shape[2]):
					confidence = detections[0, 0, i, 2]
					if confidence > 0.5:
						box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")



				# if sum((startX, startY, endX, endY)) > 0 :
				# 	detect_car = 1
				# else:
				# 	detect_car = 0
				# if prev_detect_car!=detect_car and self_cnt%window_size_hr==0:
				# 	if detect_car:
				# 		sampling_period = int(window_size_hr/2)
				# 	else:
				# 		sampling_period = window_size_hr
				# 	prev_detect_car=detect_car
				# 	print("detect car:" ,detect_car)
				# 	comm.write("frame_size",sampling_period)


				if sum((startX, startY, endX, endY)) > 0 :
					sampling_period = int(window_size_hr/2)
					detect_car = 1
				else:
					detect_car = 0
					sampling_period = int(window_size_hr/2)
					
				c.write(key_path_hash_box_entry,(str(startX)+" "+str(startY)+" "+str(endX)+" "+str(endY)).encode())
			prev_frame = frame_num

			hb.heartbeat_beat()
			# if self_cnt%sampling_period==0 and self_cnt>window_size_hr:
			comm.write("heart_rate", hb.get_instant_heartrate())
			if prev_sampling_period!=sampling_period and self_cnt%sampling_period==0 :
				prev_sampling_period=sampling_period
				comm.write("sampling_period",sampling_period)
			self_cnt+=1




hb.heartbeat_finish()
comm.write("heart_rate", "done")
print("done")





# with Client(xen_bus_path="/dev/xen/xenbus") as c:
# 	domu_ids=[]
# 	keys=['vid']
# 	if domu_ids==[]:
# 		for x in c.list('/local/domain'.encode()):
# 			domu_ids.append(x.decode())
# 		domu_ids.pop(0)
# 	not_ready_domUs = copy.deepcopy(domu_ids)
# 	for domuid in domu_ids:
# 		permissions = []
# 		permissions.append(('b'+'0').encode())
# 		permissions.append(('b'+domuid).encode())
# 		for key in keys:
# 			tmp_key_path = ('/local/domain'+'/'+domuid+'/'+key).encode()
# 			tmp_val = ('init').encode()
# 			c.write(tmp_key_path,tmp_val)
# 			c.set_perms(tmp_key_path,permissions)
# 			print('created',key,'for dom',domuid)

# 	print('waiting for domUs getting ready...')
# 	while len(not_ready_domUs)>0:
# 		ready_domUs = []
# 		for domuid in not_ready_domUs:
# 			key_path_hash=('/local/domain/'+domu_id+'/vid').encode()
# 			if c.read(key_path_hash).decode() == "ready":
# 				ready_domUs.append(domu_id)
# 		for domuid in ready_domUs:
# 			not_ready_domUs.remove(domuid)
# 			print("dom",domu_id,"ready")

# 	print("applcation start...")
# 	print(vidarray)





